# Error Conditions while using Range header

Notation:
    `Range: bytes=first-byte-spec - last-byte-spec`  
    For example : `Range: bytes=5-10`. Here 5 is first-byte-spec and 10 is last-byte-spec.

## Circular or non-circular sequence
##### Case 1
When start / end parameters are also passed along with Range header, server must throw a `400 Bad Request` error even if both are retrieving the same sequence or sub-sequence with a valid identifier and valid encoding.

_Note: Only one of the two ways should be used to query a sub-sequence._

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
?start=10&end=20

Range: bytes=10-19

```

```
HTTP/1.1 400 Bad Request
```

##### Case 2
first-byte-spec and last-byte-spec are integers, when recieve any value other than that, server MUST throw a `400 Bad Request` error.  
On recieving only one of the first-byte-spec or last-byte-spec, server MUST throw a `400 Bad Request` error.  
Reference server must only accept `bytes` as unit in `Range` header else `400 Bad Request`


```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
Range: units=10-19

    OR

GET /sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=ab-19

    OR

GET /sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=-10-19

    OR

GET /sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=10--19

    OR

GET /sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=10-    
```

```
HTTP/1.1 400 Bad Request
```

#### Case 3
`first-byte-spec > last-byte-spec`  
As stated in [success response](../sequence.md) section, Range header must not be used to retrieve sub-sequences of a circular sequences across the origin. Server must respond with `400 Bad Request` error.  
Even if the sequence is non-circular and first-byte-spec > last-byte-spec, server must throw `400 Bad Request` error.

````
GET /sequence/3332ed720ac7eaa9b3655c06f6b9e196/
Range: bytes=5200-56
```

```
HTTP/1.1 416 Range Not Satisfiable
```

##### Case 4  
`first-byte-spec >= size of sequence`

Here size of the sequence is 230218.  
Doesn't matter if sequence is circular or non-circular as first-byte-spec is inclusive and server can not honour the query in any case, will throw a `400 Bad Request` error

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=230218-230218

    OR

GET /sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=9999999-999999999999
```

```
HTTP/1.1 400 Bad Request
```
