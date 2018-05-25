API : `/sequence/:id`

Important Points

 * Servers may or may not support circular sequence.
 * Servers may or may not support other encodings(JSON, fasta etc) but must support a response type of `text/vnd.ga4gh.seq.v1.0.0+plain`.
 * Client can query for a sub-sequence and the server MUST honour.
 * `Accept` header in the requests is optional, if not given default is `text/vnd.ga4gh.seq.v1.0.0+plain` but reponse MUST have a `Content-type` header

These are all the possible success responses associated with this API.
### Complete Sequence Queries
<h5> Case 1 </h5>  
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

CCACA........GTGGG
```
<h5> Case 2 </h5>
Circular or Non-circular Sequences  
Query parameters : NA  
Checksum Algorithm : MD5  
`Accept : NIL`  
`Range : NA`   
**Description** : Complete sequence will be retrieved no matter the type (circular/non-circular). If encoding is not provided, server will assume it to be `text/vnd.ga4gh.seq.v1.0.0+plain`.  

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/

Accept: text/<new-encoding>

```
```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 230218

CCACA........GTGGG
```

<h5> Case 3 </h5>
Circular or Non-circular Sequences  
Query parameters : NA  
Checksum Algorithm : Truncated SHA512  
`Accept : vnd.ga4gh.seq.v1.0.0+plain` (or any encoding supported by server)  
`Range : NA`   
**Description** : Complete sequence will be retrieved no matter the type (circular/non-circular). Checksum algorithm must be supported by the server, otherwise server will result in a `404 Not  Found` error.

_Note : Identifier in the API requsted can also be derived using truncated SHA512, provided, the server supports it._

```
GET /sequence/959cb1883fc1ca9ae1394ceb475a356ead1ecceff5824ae7/
```
```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 230218

CCACA........GTGGG
```

### Sub-Sequence Queries
<h3> Using start / end query parameters </h3>
Important Points:

 * start is 0-based inclusive while end is 0-based exclusive
 * start and end both are 32 bit unsigned integers
 * start / end parameters must not be used along with `Range`
 * While using start / end, response must have a `Accept-Ranges` header set to none.
 * **CASE 2** of this section is only for servers which support circular sequences

<h5> Case 1 </h5>
Circular or Non-circular Sequences  
Query parameters : start and end given  
Checksum Algorithm : MD5  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain`  
`Range : NA`  
**Conditions** : start < end ; start < size of sequence;   
**Description** : Sub sequence will be retrieved no matter the type (circular/non-circular).

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
    ?start=10
    &end=20
```

```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 10
Accept-Ranges: none

CCCACACACC
```

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
    ?start=10
    &end=11
```

```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 1
Accept-Ranges: none

C
```

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
    ?start=230217
    &end=230218
```

```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 1
Accept-Ranges: none

G
```

<h5> Case 2 </h5>
Circular or Non-circular Sequences  
Query parameters : start and end given  
Checksum Algorithm : MD5  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain`  
`Range : NA`  
**Conditions** : start = end ; start < size of sequence;  
**Description** : Sub sequence of length 0 will be return (i.e. an empty string), as start is inclusive but end is exclusive.

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
    ?start=10
    &end=10
```

```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 0
Accept-Ranges: none


```


<h5> Case 3 </h5>
Circular Sequences  
Query parameters : start and end given  
Checksum Algorithm : MD5  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain`  
`Range : NA`  
**Conditions** : start > end ;  start < size of sequence; end <= size of sequence   
Circular sequences **must** be supported by the server (This support is optional. Server will throw a Not Implemented error if support for circular sequences is not there,which will be covered in **Error** section)  
**Description** : Sub sequence will be retrieved, from start till the last byte of the sequence then immediately from first byte till the end.  
For example :  
Sequence : ATGCATGCATGCATGC ; start = 10 & end = 2  
Response : GCATGC + AT -> GCATGCAT

```
GET /sequence/3332ed720ac7eaa9b3655c06f6b9e196/
    ?start=5372
    &end=5

```

```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 17
Accept-Ranges: none

ATCCAACCTGCAGAGTT
```

<h5> Case 4 </h5>
Non-circularCircular Sequences  
Query parameters : Either start or end given  
Checksum Algorithm : MD5  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain`  
`Range : NA`  
**Conditions** :  
Either start or end given; start < size of the sequence; end <= size of the sequence

**Description** : Sub sequence will be retrieved. If only start is given, end will be assumed to have a value equals to `size of the sequence`. If only end is given, start will be assumed to have a value equals to `0`.  
For example :  
Sequence : ATGCATGCATGCATGC ; start = 1    
Response : TGCATGCATGCATGC

Sequence : ATGCATGCATGCATGC ; end = 8  
Response :  ATGCATGC

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
    ?start=10
```

```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 230208
Accept-Ranges: none

CCCAC....GTGGG
```

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
    ?end=5
```

```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 5
Accept-Ranges: none

CCACA
```

<h3> Using Range Header </h3>
Notation:
    `Range: bytes=first-byte-spec - last-byte-spec`  
    For example : `Range: bytes=5-10`. Here 5 is first-byte-spec and 10 is last-byte-spec.

Important Points:

 * Range header's unit will be bytes. first-byte-spec and last-byte-spec can be integral values only and last-byte-spec >= first-byte-spec MUST be True.
 * first-byte-spec and last-byte-spec are both 0-based inclusive as opposed to start / end where end was exclusive.
 * Sub-sequences of a circular sequences across the origin must not be requested via the Range header. Refer first point.
 * More information can be found [here](https://tools.ietf.org/html/rfc7233)
 * **If last-byte-spec equals or more than size of sequence, server MUST replace the value of last-byte-spec with (size - 1).**

<h5> Case 1 </h5>
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

CCCACACACC
```

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=10-230217

```

```
HTTP/1.1 206 Partial Content
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 230208

CCCAC.....GTGGG
```


```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=10-99999999

```

```
HTTP/1.1 206 Partial Content
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 230208

CCCAC.....GTGGG
```

<h5> Case 2 </h5>
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

CCACA........GTGGG
```

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=0-999999999

```

```
HTTP/1.1 200 OK
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 230218

CCACA........GTGGG
```
*Note : More details on the API specification are available [here](HTTP/1.1HTTP/1.1  s://docs.google.com/document/d/1q2ZE9YewJTpaqQg82Nrz_jVy8KsDpKoG1T8RvCAAsbI/edit#heading=h.pr8uvsa1k8iy)*