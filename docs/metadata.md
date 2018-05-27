API : `/sequence/:id/metadata`

Important Points :  

 * Servers may or may not support other encoding but must support `application/vnd.ga4gh.seq.v1.0.0+json`.
 * `Accept` header in the requests is optional, if not given default is `application/vnd.ga4gh.seq.v1.0.0+json` but reponse MUST have a `Content-type: application/vnd.ga4gh.seq.v1.0.0+json` header
 * This API will return all known names for an identifier and related metadata.
 * The server MAY return the query identifier in the list of identifiers.


## Success Conditions
<h5> Case 1 </h5>
Identifier can be MD5 or truncated SHA512(if supported by the server) or any alias for the sequence, supported by the server.

```
GET  /sequence/3332ed720ac7eaa9b3655c06f6b9e196/metadata/
```
```
HTTP/1.1 200 OK
Content-Type: application/vnd.ga4gh.seq.v1.0.0+json

<JSON object shown below>
```
```json
{
    "metadata" : {
        "id" : "3332ed720ac7eaa9b3655c06f6b9e196",
        "length": 5384,
        "aliases" : [
            {
                "alias": "3332ed720ac7eaa9b3655c06f6b9e196"
            },
            {
                "alias":   "2085c82d80500a91dd0b8aa9237b0e43f1c07809bd6e6785"
            }
        ]
    }
}
```

## Error Conditions
<h5> Case 1 </h5>
**ID not found**  
When ID provided in the request doesn't match any of the checksums of any sequence or alias supported by the server, server throws a `404 Not Found` error

```
GET /sequence/some1111garbage11111id/metadata/
```

```
HTTP/1.1 404 Not Found
```

<h5> Case 2 </h5>
**Unsupported media type by the server**  
When media type requested by the client in the `Accept` header is not supported by the server, server throws a `415 Unsupported Media Type` error

```
GET /sequence/3332ed720ac7eaa9b3655c06f6b9e196/metadata/
Accept : text/<some-encoding-not-supported-by-server>
```

```
HTTP/1.1 415 Unsupported Media Type
```




*Note : More details on the API specification are available [here](https://docs.google.com/document/d/1q2ZE9YewJTpaqQg82Nrz_jVy8KsDpKoG1T8RvCAAsbI/edit#heading=h.gx07qh8j1d00)*
