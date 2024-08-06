---
slug: /usage
title: Usage
---

## Managing media, playlists and bindings

You can manage media, playlists and bindings using
the `/media`, `/playlists` and `/bindings` endpoints.
The API follows RESTful conventions,
so you can use the following HTTP methods:

- `GET` to retrieve a resource or a list of resources
- `POST` to create a new resource
- `PATCH` to update an existing resource
- `DELETE` to delete an existing resource

For example, to create a new media,
you can use [`curl`](https://curl.se)
to send a `POST` request to the `/media` endpoint:

```sh
curl \
    --request POST \
    --header "Content-Type: application/json" \
    --data '{"name": "My Media"}' \
    http://localhost:42000/media
```

## Uploading and downloading media content

You can upload and download media content
using the `/media/:id/content` endpoint.
To upload media content, you can use
[`curl`](https://curl.se) to send a `PUT` request
streaming the content from a file:

```sh
curl \
    --request PUT \
    --header "Content-Type: audio/mpeg" \
    --header "Transfer-Encoding: chunked" \
    --upload-file my-media.mp3 \
    http://localhost:42000/media/d06997da-6072-4a06-b7d4-6dd46cbbf716/content
```

To download media content, you can use
[`curl`](https://curl.se) to send a `GET` request
and save the response body to a file:

```sh
curl \
    --request GET \
    --output my-media.mp3 \
    http://localhost:42000/media/d06997da-6072-4a06-b7d4-6dd46cbbf716/content
```

## Retrieving playlists in M3U format

You can retrieve playlists in M3U format
using the `/playlists/:id/m3u` endpoint.
To retrieve a playlist in M3U format,
you can use [`curl`](https://curl.se)
to send a `GET` request and save the response body to a file:

```sh
curl \
    --request GET \
    --output my-playlist.m3u \
    http://localhost:42000/playlists/944f57ed-56eb-43a4-bc80-0667b9f0c1e7/m3u
```

## Ping

You can check the status of the app by sending
either a `GET` or `HEAD` request to the `/ping` endpoint.
The app should respond with a `204 No Content` status code.

For example, you can use `curl` to do that:

```sh
curl \
    --request HEAD \
    --head \
    http://localhost:42000/ping
```

## Server-Sent Events

You can subscribe to the Server-Sent Events (SSE) by sending
a `GET` request to the `/sse` endpoint.
The app will send you the events as they happen.

For example, you can use `curl` to do that:

```sh
curl \
    --request GET \
    --no-buffer \
    http://localhost:42000/sse
```
