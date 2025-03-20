# Echo endpoint
:::warning Work in progress
<centered-image src="/img/work-in-progress.png" />
This warning will be removed once this page has passed testing.
:::


Sometimes you need to test a client's ability to respond to various message or error/status codes.  It may be difficult to purposefully generate a 500.  In these cases you can enable `HY_ADD_ECHO`.  Then you can PUT to `/_echo` a JSON as follows:

```json
{
  "status_code": ###,
  "message": {...}
}
```

This produce a response with status code as specified, with the `message` value as the body.  It also goes through the service logging system, so you can test receiving emails on 5xx, etc. (or however you choose to extend the logging)
