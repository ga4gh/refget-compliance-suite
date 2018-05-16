# GET Sequence by ID
API : `/sequence/:id`

Important Points :  
 * Servers may or may not support circular chromosome.
 * Servers may or may not support other encoding(JSON, fasta etc) but must support `text/vnd.ga4gh.seq.v1.0.0+plain` or `text/plain`.
 * Client can query for a sub-sequence and server MUST honour.
 * `Accept` header in the requests is optional, if not given default is `text/vnd.ga4gh.seq.v1.0.0+plain` but reponse MUST have a `Content-type` header

## Success Responses

These are all the possible success responses associated with this API.
### Non Ranged Queries
##### Case 1
Circular or Non-circular Chromosomes  
Query parameters : NA  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain`
`Range : NA`   
**Description** : Complete sequence of the chromosome will be retrieved no matter the type (circular/non-circular)

```
GET
/sequence/959cb1883fc1ca9ae1394ceb475a356ead1ecceff5824ae7/

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
Circular or Non-circular Chromosomes  
Query parameters : NA  
`Accept : text/<new-encoding>`  
`Range : NA`   
**Description** : Complete sequence of the chromosome will be retrieved no matter the type (circular/non-circular). Encoding provided in the `Accept` header of request by the cient should be supported by the server otherwise reponse will be an error which be covered in **Error** section

_Note : Encoding can be different, provided supported by the server and requested by the client. This is true for other success queries (ranged) also._

```
GET
/sequence/959cb1883fc1ca9ae1394ceb475a356ead1ecceff5824ae7/

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
Circular or Non-circular Chromosomes  
Query parameters : start and end given  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain` (or any encoding supported by server)  
`Range : NA`  
**Conditions** : start <= end < size of chromosome  
**Description** : Sub sequence of the chromosome will be retrieved no matter the type (circular/non-circular).

```
GET
/sequence/
959cb1883fc1ca9ae1394ceb475a356ead1ecceff5824ae7/
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
Circular Chromosomes  
Query parameters : start and end given  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain` (or any encoding supported by server)  
`Range : NA`  
**Conditions** : start > end ;  start < size of chromosome;  
Circular chromosomes **must** be supported by the server (This support is optional. Server will throw a Not Implemented error if support for circular chromosomes is not there,which will be covered in **Error** section)  
**Description** : Sub sequence of the circular chromosome will be retrieved, from start till the last byte of the chromosome then immediately from first byte till the end.  
For example :  
Sequence : ATGCATGCATGCATGC ; start = 10 & end = 2  
Response : GCATGC + AT -> GCATGCAT

```
GET
/sequence/
2085c82d80500a91dd0b8aa9237b0e43f1c07809bd6e6785/
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
 * Sub-sequences of circular chromosomes across the origin must not be requested via the Range header, i.e y >= x.
 * More information can be found [here](https://tools.ietf.org/html/rfc7233)

##### Case 1
Circular or Non-circular Chromosomes  
Query parameters : NIL  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain` (or any encoding supported by server)  
`Range: bytes=x-y` where x and y are integers  
**Conditions** : x <= y < size of chromosome (if x is 0, y can not be size - 1)    
**Description** : Sub sequence of the chromosome will be retrieved no matter the type (circular/non-circular).
If x is not 0 and y is not size of chromosome - 1, (i.e. complete sequence is not being queried) response should be a `206` otherwise `200` (case 2)

```
GET
/sequence/
959cb1883fc1ca9ae1394ceb475a356ead1ecceff5824ae7/

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
Circular or Non-circular Chromosomes  
Query parameters : NIL  
`Accept : text/vnd.ga4gh.seq.v1.0.0+plain` (or any encoding supported by server)  
`Range: bytes=x-y` where x and y are integers  
**Conditions** : x = 0 and y = size of chromosome - 1   
**Description** : Complete sequence of the chromosome will be retrieved no matter the type (circular/non-circular) hence ignoring the Range header.

```
GET
/sequence/
959cb1883fc1ca9ae1394ceb475a356ead1ecceff5824ae7/

Range: bytes=0-234054

```

```
HTTP/1.1 206 Partial Content
Date: <date>
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 234055
Content: CCACA........GTGGG
```




*Note : More details on the API specification are available [here](https://docs.google.com/document/d/1q2ZE9YewJTpaqQg82Nrz_jVy8KsDpKoG1T8RvCAAsbI/edit#heading=h.pr8uvsa1k8iy)*
