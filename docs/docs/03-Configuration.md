---
slug: /configuration
title: Configuration
---

## Environment variables

You can configure the app at runtime using various environment variables:

- `EMITUNES__SERVER__HOST` -
  host to run the server on
  (default: `0.0.0.0`)
- `EMITUNES__SERVER__PORT` -
  port to run the server on
  (default: `42000`)
- `EMITUNES__SERVER__TRUSTED`
  trusted IP addresses
  (default: ``)
- `EMITUNES__DATATUNES__SQL__HOST` -
  host of the SQL API of the datatunes database
  (default: `localhost`)
- `EMITUNES__DATATUNES__SQL__PORT` -
  port of the SQL API of the datatunes database
  (default: `41000`)
- `EMITUNES__DATATUNES__SQL__PASSWORD` -
  password to authenticate with the SQL API of the datatunes database
  (default: `password`)
- `EMITUNES__MEDIATUNES__S3__SECURE` -
  whether to use secure connections for the S3 API of the mediatunes database
  (default: `false`)
- `EMITUNES__MEDIATUNES__S3__HOST` -
  host of the S3 API of the mediatunes database
  (default: `localhost`)
- `EMITUNES__MEDIATUNES__S3__PORT` -
  port of the S3 API of the mediatunes database
  (default: `40000`)
- `EMITUNES__MEDIATUNES__S3__USER` -
  user to authenticate with the S3 API of the mediatunes database
  (default: `readwrite`)
- `EMITUNES__MEDIATUNES__S3__PASSWORD` -
  password to authenticate with the S3 API of the mediatunes database
  (default: `password`)
