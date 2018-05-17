# Error Conditions while using Range header

Notation:  
`Range: bytes=x-y` where x and y are integers

## Circular or non-circular sequence
##### Case 1
When start / end parameters are also passed along with Range header, server must throw a `400 Bad Request` error even if both are retrieving the same sequence or sub-sequence with a valid identifier and valid encoding.

_Note: Only one of the two ways should be used to query a sub-sequence._

```
GET
/sequence/6681ac2f62509cfc220d78751b8dc524/
? start = 10 & end = 20

Range: bytes=10-19

```

```
HTTP/1.1 400 Bad Request
Date: <date>
```

##### Case 2
x and y are integers, when recieve any value other than that, server MUST throw a `400 Bad Request` error.  
On recieving only one of the x or y parameters, server MUST throw a `400 Bad Request` error.  
Reference server must only accept `bytes` as unit in `Range` header else `400 Bad Request`


```
GET
/sequence/6681ac2f62509cfc220d78751b8dc524/
Range: units=10-19

    OR

/sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=ab-19

    OR

/sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=-10-19

    OR

/sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=10--19

    OR

/sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=10-    
```

```
HTTP/1.1 400 Bad Request
Date: <date>
```

##### Case 3  
`x >= size of sequence`  
OR  
`y >= size of the sequence`

Here size of the sequence is 234055.  
Doesn't matter if sequence is circular or non-circular as x and y are both inclusive and server can not honour the query in any case, will throw a `400 Bad Request` error

```
GET
/sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=234054-234055

    OR

GET
/sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=234055-234055

    OR

GET
/sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=234055-234054
```

```
HTTP/1.1 400 Bad Request
Date: <date>
```

#### Case 4
`x > y`  
As stated in [success response](../sequence.md) section, Range header must not be used to retrieve sub-sequences of a circular sequences across the origin. Server must respond with `400 Bad Request` error.  
Even if the sequence is non-circular and x > y, server must throw `400 Bad Request` error.

```
GET
/sequence/3332ed720ac7eaa9b3655c06f6b9e196/
Range: bytes=5200-56
```

```
HTTP/1.1 400 Bad Request
Date: <date>
```
