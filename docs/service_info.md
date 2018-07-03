API : `/sequence/service-info`

Return configuration information about this server implementation. Default configuation is `application/vnd.ga4gh.seq.v1.0.0+json`


## Success Conditions
<h5> Case 1 </h5>
The server shall return a document detailing specifications of the service implementation.

```
GET  /sequence/service-info/
```
```
HTTP/1.1 200 OK
Content-Type: application/vnd.ga4gh.seq.v1.0.0+json

```
```json
{
  "service" : {
    "circular_supported" : false,
    "algorithms": ["md5", "trunc512"],
    "subsequence_limit": 4000000,
    "Supported_api_versions": ["1.0"]
  }
}
```

## Error Conditions
<h5> Case 1 </h5>
**Unsupported media type by the server**  
When media type requested by the client in the `Accept` header is not supported by the server, server throws a `415 Unsupported Media Type` error

```
GET /sequence/service-info/
Accept : text/exotic-encoding
```

```
HTTP/1.1 415 Unsupported Media Type
```
