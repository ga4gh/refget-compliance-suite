API : `/sequence/:id/metadata`

Important Points :

 * Servers may or may not support other encoding but must support `application/vnd.ga4gh.refget.v1.0.0+json`.
 * `Accept` header in the requests is optional, if not given default is `application/vnd.ga4gh.refget.v1.0.0+json` but response MUST have a `Content-type: application/vnd.ga4gh.refget.v1.0.0+json` header
 * This API will return all known names for an identifier and related metadata.
 * The server MAY return the query identifier in the list of identifiers.


## Success Conditions
<h5> Case 1 </h5>
Identifier can be MD5 or truncated SHA512 (if supported by the server) or any alias for the sequence, supported by the server.


```
GET  /sequence/3332ed720ac7eaa9b3655c06f6b9e196/metadata/
```
```
HTTP/1.1 200 OK
Content-Type: application/vnd.ga4gh.refget.v1.0.0+json

```
```json
{
    "metadata" : {
        "md5" : "3332ed720ac7eaa9b3655c06f6b9e196",
        "trunc512" : "2085c82d80500a91dd0b8aa9237b0e43f1c07809bd6e6785",
        "length" : 5384,
        "aliases" : [

        ]
    }
}
```
Array under `aliases` key will contain objects of aliases in the form given below with an example
```json
"aliases" : [
    {
        "alias": "CH003448.1",
        "naming_authority" : "INSDC"
    },
    {
        "alias": "chr1",
        "naming_authority" : "UCSC"
    }

]

```

## Error Conditions
<h5> Case 1 </h5>
**ID not found**
When ID provided in the request doesn't match any of the checksums of any sequence or alias supported by the server, server throws a `404 Not Found` error. If the server use the length of the digest to check that it is formed correctly it might return 400 if the length does not match expected.

```
GET /sequence/some1111garbage11111id/metadata/
```

```
HTTP/1.1 404 Not Found
```

<h5> Case 2 </h5>
**Unsupported media type by the server**
When media type requested by the client in the `Accept` header is not supported by the server, server throws a `406 Not Acceptable` error

```
GET /sequence/3332ed720ac7eaa9b3655c06f6b9e196/metadata/
Accept : text/exotic-encoding
```

```
HTTP/1.1 406 Not Acceptable
```
