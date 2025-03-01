---
slug: /config
title: Configuration
---

## Environment variables

You can configure the service at runtime using various environment variables:

- `PELICAN__SERVER__HOST` -
  host to run the server on
  (default: `0.0.0.0`)
- `PELICAN__SERVER__PORT` -
  port to run the server on
  (default: `10200`)
- `PELICAN__SERVER__TRUSTED` -
  trusted IP addresses
  (default: `*`)
- `PELICAN__GRAPHITE__SQL__HOST` -
  host of the SQL API of the graphite database
  (default: `localhost`)
- `PELICAN__GRAPHITE__SQL__PORT` -
  port of the SQL API of the graphite database
  (default: `10220`)
- `PELICAN__GRAPHITE__SQL__PASSWORD` -
  password to authenticate with the SQL API of the graphite database
  (default: `password`)
- `PELICAN__MINIUM__S3__SECURE` -
  whether to use secure connections for the S3 API of the minium database
  (default: `false`)
- `PELICAN__MINIUM__S3__HOST` -
  host of the S3 API of the minium database
  (default: `localhost`)
- `PELICAN__MINIUM__S3__PORT` -
  port of the S3 API of the minium database
  (default: `10210`)
- `PELICAN__MINIUM__S3__USER` -
  user to authenticate with the S3 API of the minium database
  (default: `readwrite`)
- `PELICAN__MINIUM__S3__PASSWORD` -
  password to authenticate with the S3 API of the minium database
  (default: `password`)
- `PELICAN__DEBUG` -
  enable debug mode
  (default: `true`)
