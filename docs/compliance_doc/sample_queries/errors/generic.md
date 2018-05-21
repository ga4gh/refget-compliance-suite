# Generic Error Conditions

These conditions are first line of checks, failing these conditions would result in the specified error, no matter other parameters.

##### Case 1
**Unauthorized user**  
More information can be found in API spec, [here]()

```
HTTP/1.1 401 Unauthorized
```

##### Case 2
**ID not found**  
When ID provided in the request doesn't match any of the checksums of any sequence, server throws a `404 Not Found` error

```
GET /sequence/some1111garbage11111id/
```

```
HTTP/1.1 404 Not Found
```

##### Case 3
**Unsupported media type by the server**  
When media type requested by the client in the `Accept` header is not supported by the server, server throws a `415 Unsupported Media Type` error

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524

Accept : text/<some-encoding-not-supported-by-server>
```

```
HTTP/1.1 415 Unsupported Media Type
```
