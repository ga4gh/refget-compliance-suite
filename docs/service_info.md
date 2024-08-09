API : `/sequence/service-info`

Return configuration information about this server implementation. Default configuation is `application/vnd.ga4gh.refget.v1.0.0+json`


## Success Conditions
<h5> Case 1 </h5>
The server shall return a document detailing specifications of the service implementation.

```
GET  /sequence/service-info/
```
```
HTTP/1.1 200 OK
Content-Type: application/vnd.ga4gh.refget.v2.0.0+json

```
```json
{
    "id": "refget.server.v2",
    "name": "The GA4GH Refget API V2",
    "type": {
        "group": "org.ga4gh",
        "artifact": "refget",
        "version": "2.0.0"
    },
    "organization": {
        "name": "Example Org",
        "url": "https://www.examples.com"
    },
    "refget": {
        "circular_supported": false,
        "subsequence_limit": 4000000,
        "algorithms":  ["md5", "ga4gh"],
        "identifier_types": ["insdc"]
    }
}
```

## Error Conditions
<h5> Case 1 </h5>
**Unsupported media type by the server**
When media type requested by the client in the `Accept` header is not supported by the server, server throws a `406 Not Acceptable` error

```
GET /sequence/service-info/
Accept : text/exotic-encoding
```

```
HTTP/1.1 406 Not Acceptable
```
