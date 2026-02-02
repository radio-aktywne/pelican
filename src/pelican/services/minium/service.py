import asyncio
from collections.abc import Generator
from contextlib import contextmanager
from enum import StrEnum
from typing import BinaryIO, cast

from minio import Minio
from minio.commonconfig import CopySource
from minio.datatypes import Object
from minio.error import MinioException, S3Error
from urllib3 import BaseHTTPResponse

from pelican.config.models import MiniumConfig
from pelican.services.minium import errors as e
from pelican.services.minium import models as m
from pelican.utils import asyncify, syncify
from pelican.utils.read import ReadableIterator
from pelican.utils.time import httpparse


class ErrorCodes(StrEnum):
    """Error codes."""

    NOT_FOUND = "NoSuchKey"


class MiniumService:
    """Service for minium database."""

    def __init__(self, config: MiniumConfig) -> None:
        self._client = Minio(
            endpoint=config.s3.endpoint,
            access_key=config.s3.user,
            secret_key=config.s3.password,
            secure=config.s3.secure,
            cert_check=False,
        )
        self._bucket = config.s3.bucket

    def _map_object(self, obj: Object) -> m.Object:
        return m.Object(
            name=str(obj.object_name),
            modified=obj.last_modified,
            size=obj.size,
            metadata=dict(obj.metadata) if obj.metadata else None,
            type=obj.content_type,
        )

    @contextmanager
    def _handle_errors(self) -> Generator[None]:
        try:
            yield
        except MinioException as ex:
            raise e.ServiceError from ex

    @contextmanager
    def _handle_not_found(self, name: str) -> Generator[None]:
        try:
            yield
        except S3Error as ex:
            if ex.code == ErrorCodes.NOT_FOUND:
                raise e.NotFoundError(name) from ex

    async def list(self, request: m.ListRequest) -> m.ListResponse:
        """List objects."""
        with self._handle_errors():
            objects = await asyncio.to_thread(
                self._client.list_objects,
                bucket_name=self._bucket,
                prefix=request.prefix,
                recursive=request.recursive,
            )

        objects = asyncify.iterator(self._map_object(obj) for obj in objects)

        return m.ListResponse(objects=objects)

    async def upload(self, request: m.UploadRequest) -> m.UploadResponse:
        """Upload an object."""
        with self._handle_errors():
            await asyncio.to_thread(
                self._client.put_object,
                bucket_name=self._bucket,
                object_name=request.name,
                data=cast(
                    "BinaryIO", ReadableIterator(syncify.iterator(request.content.data))
                ),
                length=-1,
                content_type=request.content.type,
                part_size=request.chunk,
            )

        get_request = m.GetRequest(name=request.name)
        get_response = await self.get(get_request)

        return m.UploadResponse(object=get_response.object)

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get an object."""
        with self._handle_errors(), self._handle_not_found(request.name):
            obj = await asyncio.to_thread(
                self._client.stat_object,
                bucket_name=self._bucket,
                object_name=request.name,
            )

        return m.GetResponse(object=self._map_object(obj))

    async def download(self, request: m.DownloadRequest) -> m.DownloadResponse:
        """Download an object."""
        with self._handle_errors(), self._handle_not_found(request.name):
            get_object_response = await asyncio.to_thread(
                self._client.get_object,
                bucket_name=self._bucket,
                object_name=request.name,
            )

        def _data(res: BaseHTTPResponse, chunk: int) -> Generator[bytes]:
            try:
                yield from res.stream(chunk)
            finally:
                res.close()
                res.release_conn()

        return m.DownloadResponse(
            content=m.DownloadContent(
                type=get_object_response.headers["Content-Type"],
                size=int(get_object_response.headers["Content-Length"]),
                tag=get_object_response.headers["ETag"],
                modified=httpparse(get_object_response.headers["Last-Modified"]),
                data=asyncify.iterator(_data(get_object_response, request.chunk)),
            )
        )

    async def copy(self, request: m.CopyRequest) -> m.CopyResponse:
        """Copy an object."""
        with self._handle_errors(), self._handle_not_found(request.source):
            await asyncio.to_thread(
                self._client.copy_object,
                bucket_name=self._bucket,
                object_name=request.destination,
                source=CopySource(bucket_name=self._bucket, object_name=request.source),
            )

        get_request = m.GetRequest(name=request.destination)
        get_response = await self.get(get_request)

        return m.CopyResponse(object=get_response.object)

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete an object."""
        get_request = m.GetRequest(name=request.name)
        get_response = await self.get(get_request)

        if get_response.object is None:
            raise e.NotFoundError(request.name)

        with self._handle_errors(), self._handle_not_found(request.name):
            await asyncio.to_thread(
                self._client.remove_object,
                bucket_name=self._bucket,
                object_name=request.name,
            )

        return m.DeleteResponse(object=get_response.object)
