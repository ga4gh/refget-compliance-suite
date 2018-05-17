# GET Sequence by ID
API : `/sequence/:id`

Important Points :  
 * Servers may or may not support circular sequence.
 * Servers may or may not support other encoding(JSON, fasta etc) but must support `text/vnd.ga4gh.seq.v1.0.0+plain` or `text/plain`.
 * Client can query for a sub-sequence and server MUST honour.
 * `Accept` header in the requests is optional, if not given default is `text/vnd.ga4gh.seq.v1.0.0+plain` but reponse MUST have a `Content-type` header

## Success Responses

These are all the possible success responses associated with this API.
### Non Ranged Queries
##### Case 1
Circular or Non-circular sequences  
Query parameters : NA  
Checksum Algorithm : MD5  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain`
`Range : NA`   
**Description** : Complete sequence will be retrieved no matter the type (circular/non-circular)

```
GET
/sequence/6681ac2f62509cfc220d78751b8dc524/

Accept: text/vnd.ga4gh.seq.v1.0.0+plain (optional)
```
```
HTTP/1.1 200 OK
Date: <date>
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 234055
Content: CCACA........GTGGG
```
##### Case 2
Circular or Non-circular Sequences  
Query parameters : NA  
Checksum Algorithm : MD5  
`Accept : text/<new-encoding>`  
`Range : NA`   
**Description** : Complete sequence will be retrieved no matter the type (circular/non-circular). Encoding provided in the `Accept` header of request by the cient should be supported by the server otherwise reponse will be an error which be covered in **Error** section

_Note : Encoding can be different, provided supported by the server and requested by the client. This is true for other success queries (ranged) also._

```
GET
/sequence/6681ac2f62509cfc220d78751b8dc524/

Accept: text/<new-encoding>

```
```
HTTP/1.1 200 OK
Date: <date>
Content-Type: text/<new-encoding>; charset=us-ascii
Content-Length: 234055
Content: CCACA........GTGGG
```

##### Case 3
Circular or Non-circular Sequences  
Query parameters : NA  
Checksum Algorithm : Truncated SHA512  
`Accept : vnd.ga4gh.seq.v1.0.0+plain` (or any encoding supported by server)  
`Range : NA`   
**Description** : Complete sequence will be retrieved no matter the type (circular/non-circular). Checksum algorithm must be supported by the server, otherwise server will result in a `404 Not  Found` error.

_Note : Checksum Algorithm can be different, provided supported by the server. This is true for other success queries (ranged) also._

```
GET
/sequence/6681ac2f62509cfc220d78751b8dc524/

Accept: text/<new-encoding>

```
```
HTTP/1.1 200 OK
Date: <date>
Content-Type: text/<new-encoding>; charset=us-ascii
Content-Length: 234055
Content: CCACA........GTGGG
```

### Ranged Queries
#### Using start / end query parameters
Important Points:
 * start is inclusive while end is exclusive
 * start and end both are 32 bit unsigned integers
 * start / end parameters must not be used along with `Range`
 * While using start / end, response must have a `Accept-Ranges` header set to none.

##### Case 1
Circular or Non-circular Sequences  
Query parameters : start and end given  
Checksum Algorithm : MD5 (or truncated SHA512 if supported by the server)  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain` (or any encoding supported by server)  
`Range : NA`  
**Conditions** : start <= end < size of sequence  
**Description** : Sub sequence will be retrieved no matter the type (circular/non-circular).

```
GET
/sequence/6681ac2f62509cfc220d78751b8dc524/
? start=10 & end=20
```

```
HTTP/1.1 200 OK
Date: <date>
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 10
Content: CCCACACACC
Accept-Ranges: none
```

##### Case 2
Circular Sequences  
Query parameters : start and end given  
Checksum Algorithm : MD5 (or truncated SHA512 if supported by the server)  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain` (or any encoding supported by server)  
`Range : NA`  
**Conditions** : start > end ;  start < size of sequence;  
Circular sequences **must** be supported by the server (This support is optional. Server will throw a Not Implemented error if support for circular sequences is not there,which will be covered in **Error** section)  
**Description** : Sub sequence will be retrieved, from start till the last byte of the sequence then immediately from first byte till the end.  
For example :  
Sequence : ATGCATGCATGCATGC ; start = 10 & end = 2  
Response : GCATGC + AT -> GCATGCAT

```
GET
/sequence/3332ed720ac7eaa9b3655c06f6b9e196/
? start=5372 & end=5

```

```
HTTP/1.1 200 OK
Date: <date>
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 17
Content: ATCCAACCTGCAGAGTT
Accept-Ranges: none
```

#### Using Range Header
Important Points:
 * Range header's unit will be bytes. `Range: bytes=x-y` where x and y are unsigned integers.
 * x and y are both inclusive as opposed to start / end where end was exclusive.
 * Sub-sequences of a circular sequences across the origin must not be requested via the Range header, i.e y >= x will always be true.
 * More information can be found [here](https://tools.ietf.org/html/rfc7233)

##### Case 1
Circular or Non-circular Sequences  
Query parameters : NIL  
Checksum Algorithm : MD5 (or truncated SHA512 if supported by the server)  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain` (or any encoding supported by server)  
`Range: bytes=x-y` where x and y are integers  
**Conditions** : x <= y < size of sequence (if x is 0, y can not be size - 1)    
**Description** : Sub sequence will be retrieved no matter the type (circular/non-circular).
If x is not 0 and y is not size of sequence - 1, (i.e. complete sequence is not being queried) response should be a `206` otherwise `200` (case 2)

```
GET
/sequence/6681ac2f62509cfc220d78751b8dc524/

Range: bytes=10-19

```

```
HTTP/1.1 206 Partial Content
Date: <date>
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 10
Content: CCCACACACC
```

##### Case 2
Circular or Non-circular Sequences  
Query parameters : NIL  
Checksum Algorithm : MD5 (or truncated SHA512 if supported by the server)  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain` (or any encoding supported by server)  
`Range: bytes=x-y` where x and y are integers  
**Conditions** : x = 0 and y = size of sequence - 1   
**Description** : Complete sequence will be retrieved no matter the type (circular/non-circular) hence ignoring the Range header.

```
GET
/sequence/6681ac2f62509cfc220d78751b8dc524/

Range: bytes=0-234054

```

```
HTTP/1.1 200 OK
Date: <date>
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 234055
Content: CCACA........GTGGG
```

## Error Conditions
Reference Servers MUST respond with adequate error codes for every error condition. Error conditions are documented in a hierarchical manner, i.e. first check are shown first.

 * [Generic Error conditions](errors/generic.md)  
 * Ranged Query Error conditions :
    * [start / end errors](errors/start_end.md)
    * [Range header errors](errors/range_header.md)


*Note : More details on the API specification are available [here](https://docs.google.com/document/d/1q2ZE9YewJTpaqQg82Nrz_jVy8KsDpKoG1T8RvCAAsbI/edit#heading=h.pr8uvsa1k8iy)*
