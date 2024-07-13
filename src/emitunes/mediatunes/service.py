import asyncio
from collections.abc import Generator
from enum import StrEnum

from minio import Minio
from minio.commonconfig import CopySource
from minio.datatypes import Object
from minio.error import MinioException, S3Error
from urllib3 import BaseHTTPResponse

from emitunes.config.models import MediatunesConfig
from emitunes.mediatunes import errors as e
from emitunes.mediatunes import models as m
from emitunes.utils import asyncify, syncify
from emitunes.utils.read import ReadableIterator


class ErrorCodes(StrEnum):
    """Error codes."""

    NOT_FOUND = "NoSuchKey"


class MediatunesService:
    """Service for mediatunes database."""

    def __init__(self, config: MediatunesConfig) -> None:
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

    async def list(self, request: m.ListRequest) -> m.ListResponse:
        """List objects."""

        bucket = self._bucket
        prefix = request.prefix
        recursive = request.recursive

        try:
            objects = await asyncio.to_thread(
                self._client.list_objects,
                bucket_name=bucket,
                prefix=prefix,
                recursive=recursive,
            )
        except MinioException as ex:
            raise e.MediatunesError(str(ex)) from ex

        objects = (self._map_object(object) for object in objects)
        objects = asyncify.iterable(objects)
        return m.ListResponse(objects=objects)

    async def upload(self, request: m.UploadRequest) -> m.UploadResponse:
        """Upload an object."""

        bucket = self._bucket
        name = request.name
        data = ReadableIterator(iter(syncify.iterable(request.data)))
        length = -1
        type = request.type
        chunk = request.chunk

        try:
            await asyncio.to_thread(
                self._client.put_object,
                bucket_name=bucket,
                object_name=name,
                data=data,
                length=length,
                content_type=type,
                part_size=chunk,
            )
        except MinioException as ex:
            raise e.MediatunesError(str(ex)) from ex

        req = m.GetRequest(name=name)
        res = await self.get(req)
        return m.UploadResponse(object=res.object)

    async def get(self, request: m.GetRequest) -> m.GetResponse:
        """Get an object."""

        bucket = self._bucket
        name = request.name

        try:
            object = await asyncio.to_thread(
                self._client.stat_object,
                bucket_name=bucket,
                object_name=name,
            )
        except S3Error as ex:
            if ex.code == ErrorCodes.NOT_FOUND:
                raise e.NotFoundError(name) from ex

            raise e.MediatunesError(str(ex)) from ex
        except MinioException as ex:
            raise e.MediatunesError(str(ex)) from ex

        object = self._map_object(object)
        return m.GetResponse(object=object)

    async def download(self, request: m.DownloadRequest) -> m.DownloadResponse:
        """Download an object."""

        bucket = self._bucket
        name = request.name

        try:
            response = await asyncio.to_thread(
                self._client.get_object,
                bucket_name=bucket,
                object_name=name,
            )
        except S3Error as ex:
            if ex.code == ErrorCodes.NOT_FOUND:
                raise e.NotFoundError(name) from ex

            raise e.MediatunesError(str(ex)) from ex
        except MinioException as ex:
            raise e.MediatunesError(str(ex)) from ex

        def _data(
            response: BaseHTTPResponse, chunk: int
        ) -> Generator[bytes, None, None]:
            try:
                yield from response.stream(chunk)
            finally:
                response.close()
                response.release_conn()

        chunk = request.chunk
        data = asyncify.iterable(_data(response, chunk))
        return m.DownloadResponse(data=data)

    async def copy(self, request: m.CopyRequest) -> m.CopyResponse:
        """Copy an object."""

        bucket = self._bucket
        source = request.source
        destination = request.destination

        try:
            await asyncio.to_thread(
                self._client.copy_object,
                bucket_name=bucket,
                object_name=destination,
                source=CopySource(bucket_name=bucket, object_name=source),
            )
        except S3Error as ex:
            if ex.code == ErrorCodes.NOT_FOUND:
                raise e.NotFoundError(source) from ex

            raise e.MediatunesError(str(ex)) from ex
        except MinioException as ex:
            raise e.MediatunesError(str(ex)) from ex

        req = m.GetRequest(name=destination)
        res = await self.get(req)
        return m.CopyResponse(object=res.object)

    async def delete(self, request: m.DeleteRequest) -> m.DeleteResponse:
        """Delete an object."""

        bucket = self._bucket
        name = request.name

        req = m.GetRequest(name=name)
        res = await self.get(req)

        object = res.object

        if object is None:
            raise e.NotFoundError(name)

        try:
            await asyncio.to_thread(
                self._client.remove_object,
                bucket_name=bucket,
                object_name=name,
            )
        except S3Error as ex:
            if ex.code == ErrorCodes.NOT_FOUND:
                raise e.NotFoundError(name) from ex

            raise e.MediatunesError(str(ex)) from ex
        except MinioException as ex:
            raise e.MediatunesError(str(ex)) from ex

        return m.DeleteResponse(object=object)
