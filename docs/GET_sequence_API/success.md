API : `/sequence/:id`

Important Points
 * Servers may or may not support circular sequence.
 * Servers may or may not support other encoding(JSON, fasta etc) but must support `text/vnd.ga4gh.seq.v1.0.0+plain` or `text/plain`.
 * Client can query for a sub-sequence and server MUST honour.
 * `Accept` header in the requests is optional, if not given default is `text/vnd.ga4gh.seq.v1.0.0+plain` but reponse MUST have a `Content-type` header

These are all the possible success responses associated with this API.
### Complete Sequence Queries
##### Case 1
Circular or Non-circular sequences  
Query parameters : NA  
Checksum Algorithm : MD5  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain`  
`Range : NA`   
**Description** : Complete sequence will be retrieved no matter the type (circular/non-circular)

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/

Accept: text/vnd.ga4gh.seq.v1.0.0+plain (optional)
```
```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 230218
Content: CCACA........GTGGG
```
##### Case 2
Circular or Non-circular Sequences  
Query parameters : NA  
Checksum Algorithm : MD5  
`Accept : text/<new-encoding>`  
`Range : NA`   
**Description** : Complete sequence will be retrieved no matter the type (circular/non-circular). Encoding provided in the `Accept` header of request by the cient should be supported by the server otherwise reponse will be an error which be covered in **Error** section

_Note : Encoding can be different, provided supported by the server and requested by the client. This is true for other success queries also._

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/

Accept: text/<new-encoding>

```
```
HTTP/1.1 200 OK
Content-Type: text/<new-encoding>; charset=us-ascii
Content-Length: 230218
Content: CCACA........GTGGG
```

##### Case 3
Circular or Non-circular Sequences  
Query parameters : NA  
Checksum Algorithm : Truncated SHA512  
`Accept : vnd.ga4gh.seq.v1.0.0+plain` (or any encoding supported by server)  
`Range : NA`   
**Description** : Complete sequence will be retrieved no matter the type (circular/non-circular). Checksum algorithm must be supported by the server, otherwise server will result in a `404 Not  Found` error.

_Note : Checksum Algorithm can be different, provided supported by the server. This is true for other success queries also._

```
GET /sequence/959cb1883fc1ca9ae1394ceb475a356ead1ecceff5824ae7/
```
```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 230218
Content: CCACA........GTGGG
```

### Sub-Sequence Queries
#### Using start / end query parameters
Important Points:
 * start is inclusive while end is exclusive
 * start and end both are 32 bit unsigned integers
 * start / end parameters must not be used along with `Range`
 * While using start / end, response must have a `Accept-Ranges` header set to none.
 * **CASE 2** of this section is only for servers which support circular sequences

##### Case 1
Circular or Non-circular Sequences  
Query parameters : start and end given  
Checksum Algorithm : MD5 (or truncated SHA512 if supported by the server)  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain` (or any encoding supported by server)  
`Range : NA`  
**Conditions** : start < end ; start < size of sequence;   
**Description** : Sub sequence will be retrieved no matter the type (circular/non-circular).

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
?start=10&end=20
```

```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 10
Content: CCCACACACC
Accept-Ranges: none
```

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
?start=10&end=11
```

```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 1
Content: C
Accept-Ranges: none
```

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
?start=230217&end=230218
```

```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 1
Content: G
Accept-Ranges: none
```

##### Case 2
Circular Sequences  
Query parameters : start and end given  
Checksum Algorithm : MD5 (or truncated SHA512 if supported by the server)  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain` (or any encoding supported by server)  
`Range : NA`  
**Conditions** : start > end ;  start < size of sequence; end <= size of sequence   
Circular sequences **must** be supported by the server (This support is optional. Server will throw a Not Implemented error if support for circular sequences is not there,which will be covered in **Error** section)  
**Description** : Sub sequence will be retrieved, from start till the last byte of the sequence then immediately from first byte till the end.  
For example :  
Sequence : ATGCATGCATGCATGC ; start = 10 & end = 2  
Response : GCATGC + AT -> GCATGCAT

```
GET /sequence/3332ed720ac7eaa9b3655c06f6b9e196/
?start=5372&end=5

```

```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 17
Content: ATCCAACCTGCAGAGTT
Accept-Ranges: none
```

#### Using Range Header
Notation:
    `Range: bytes=first-byte-spec - last-byte-spec`  
    For example : `Range: bytes=5-10`. Here 5 is first-byte-spec and 10 is last-byte-spec.

Important Points:
 * Range header's unit will be bytes. first-byte-spec and last-byte-spec can be integral values only and last-byte-spec >= first-byte-spec MUST be True.
 * first-byte-spec and last-byte-spec are both inclusive as opposed to start / end where end was exclusive.
 * Sub-sequences of a circular sequences across the origin must not be requested via the Range header. Refer first point.
 * More information can be found [here](https://tools.ietf.org/html/rfc7233)
 * **If last-byte-spec equals or more than size of sequence, server MUST replace the value of last-byte-spec with (size - 1).**

##### Case 1
Circular or Non-circular Sequences  
Query parameters : NIL  
Checksum Algorithm : MD5 (or truncated SHA512 if supported by the server)  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain` (or any encoding supported by server)  
**Conditions** : first-byte-spec <= last-byte-spec < (size - 1) (if first-byte-spec is 0, last-byte-spec can not be (size - 1))    
**Description** : Sub sequence will be retrieved no matter the type (circular/non-circular).
If first-byte-spec is not 0 and last-byte-spec is not (size - 1) or more, (i.e. complete sequence is not being queried) response should be a `206` otherwise `200` ([case 2](#case-2-2))  
Size of sequence is 230218

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/

Range: bytes=10-19

```

```
HTTP/1.1 206 Partial Content
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 10
Content: CCCACACACC
```

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/

Range: bytes=10-230217

```

```
HTTP/1.1 206 Partial Content
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 230208
Content: CCCAC.....GTGGG
```


```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/

Range: bytes=10-99999999

```

```
HTTP/1.1 206 Partial Content
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 230208
Content: CCCAC.....GTGGG
```

##### Case 2
Circular or Non-circular Sequences  
Query parameters : NIL  
Checksum Algorithm : MD5 (or truncated SHA512 if supported by the server)  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain` (or any encoding supported by server)  
**Conditions** : first-byte-spec = 0 and last-byte-spec => size of - 1   
**Description** : Complete sequence will be retrieved no matter the type (circular/non-circular) hence ignoring the Range header.  
Size of the sequence is 230218

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/

Range: bytes=0-230217

```

```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 230218
Content: CCACA........GTGGG
```

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/

Range: bytes=0-999999999

```

```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 230218
Content: CCACA........GTGGG
```
*Note : More details on the API specification are available [here](HTTP/1.1HTTP/1.1  s://docs.google.com/document/d/1q2ZE9YewJTpaqQg82Nrz_jVy8KsDpKoG1T8RvCAAsbI/edit#heading=h.pr8uvsa1k8iy)*
