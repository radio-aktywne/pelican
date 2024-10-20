import asyncio
from collections.abc import Generator
from contextlib import contextmanager
from enum import StrEnum

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

    def _map_object(self, object: Object) -> m.Object:
        return m.Object(
            name=object.object_name,
            modified=object.last_modified,
            size=object.size,
            metadata=object.metadata,
            type=object.content_type,
        )

    @contextmanager
    def _handle_errors(self) -> Generator[None]:
        try:
            yield
        except MinioException as ex:
            raise e.ServiceError(str(ex)) from ex

    @contextmanager
    def _handle_not_found(self, name: str) -> Generator[None]:
        try:
            yield
        except S3Error as ex:
            if ex.code == ErrorCodes.NOT_FOUND:
                raise e.NotFoundError(name) from ex

    async def list(self, request: m.ListRequest) -> m.ListResponse:
        """List objects."""

        bucket = self._bucket
        prefix = request.prefix
        recursive = request.recursive

        with self._handle_errors():
            objects = await asyncio.to_thread(
                self._client.list_objects,
                bucket_name=bucket,
                prefix=prefix,
                recursive=recursive,
            )

        objects = (self._map_object(object) for object in objects)
        objects = asyncify.iterator(objects)

        return m.ListResponse(
            objects=objects,
        )

    async def upload(self, request: m.UploadRequest) -> m.UploadResponse:
        """Upload an object."""

        bucket = self._bucket
        name = request.name
        data = ReadableIterator(syncify.iterator(request.content.data))
        length = -1
        type = request.content.type
        chunk = request.chunk

        with self._handle_errors():
            await asyncio.to_thread(
                self._client.put_object,
                bucket_name=bucket,
                object_name=name,
                data=data,
                length=length,
                content_type=type,
                part_size=chunk,
            )

        req = m.GetRequest(
            name=name,
        )

        res = await self.get(req)

        object = res.object

        return m.UploadResponse(
            object=object,
        )

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get an object."""

        bucket = self._bucket
        name = request.name

        with self._handle_errors():
            with self._handle_not_found(name):
                object = await asyncio.to_thread(
                    self._client.stat_object,
                    bucket_name=bucket,
                    object_name=name,
                )

        object = self._map_object(object)

        return m.GetResponse(
            object=object,
        )

    async def download(self, request: m.DownloadRequest) -> m.DownloadResponse:
        """Download an object."""

        bucket = self._bucket
        name = request.name

        with self._handle_errors():
            with self._handle_not_found(name):
                res = await asyncio.to_thread(
                    self._client.get_object,
                    bucket_name=bucket,
                    object_name=name,
                )

        def _data(res: BaseHTTPResponse, chunk: int) -> Generator[bytes]:
            try:
                yield from res.stream(chunk)
            finally:
                res.close()
                res.release_conn()

        type = res.headers["Content-Type"]
        size = int(res.headers["Content-Length"])
        tag = res.headers["ETag"]
        modified = httpparse(res.headers["Last-Modified"])

        chunk = request.chunk
        data = asyncify.iterator(_data(res, chunk))

        content = m.DownloadContent(
            type=type,
            size=size,
            tag=tag,
            modified=modified,
            data=data,
        )
        return m.DownloadResponse(
            content=content,
        )

    async def copy(self, request: m.CopyRequest) -> m.CopyResponse:
        """Copy an object."""

        bucket = self._bucket
        source = request.source
        destination = request.destination

        with self._handle_errors():
            with self._handle_not_found(source):
                await asyncio.to_thread(
                    self._client.copy_object,
                    bucket_name=bucket,
                    object_name=destination,
                    source=CopySource(
                        bucket_name=bucket,
                        object_name=source,
                    ),
                )

        req = m.GetRequest(
            name=destination,
        )

        res = await self.get(req)

        object = res.object

        return m.CopyResponse(
            object=object,
        )

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete an object."""

        bucket = self._bucket
        name = request.name

        req = m.GetRequest(
            name=name,
        )

        res = await self.get(req)

        object = res.object

        if object is None:
            raise e.NotFoundError(name)

        with self._handle_errors():
            with self._handle_not_found(name):
                await asyncio.to_thread(
                    self._client.remove_object,
                    bucket_name=bucket,
                    object_name=name,
                )

        return m.DeleteResponse(
            object=object,
        )
