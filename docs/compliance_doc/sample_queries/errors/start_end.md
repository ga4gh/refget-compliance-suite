# Error Conditions while using start / end parameters
## Circular or non-circular sequence
##### Case 1
When Range header is also passed along with start / end parameters, server must throw a `400 Bad Request` error even if both are retrieving the same sequence or sub-sequence with a valid identifier and valid encoding.

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
start and end are 32 bit-unsigned integers, when recieve any value other than that, server MUST throw a `400 Bad Request` error.  
On recieving only one of the start / end parameters, server MUST throw a `400 Bad Request` error.


```
GET
/sequence/6681ac2f62509cfc220d78751b8dc524/
? start = abc & end = 20

    OR

/sequence/6681ac2f62509cfc220d78751b8dc524/
? start = -10 & end = -29

    OR

/sequence/6681ac2f62509cfc220d78751b8dc524/
? start = abc   (end is missing)

    OR

/sequence/6681ac2f62509cfc220d78751b8dc524/
? end = 20  (start is missing)
```

```
HTTP/1.1 400 Bad Request
Date: <date>
```

##### Case 3
When  
`start >= size of sequence`  
OR  
`end > size of the sequence`

Here, size of the sequence is 234055

`6681ac2f62509cfc220d78751b8dc524` is a non-circular sequence; size = 234055  
`3332ed720ac7eaa9b3655c06f6b9e196` is a circular sequence; size = 5384

```
GET
/sequence/6681ac2f62509cfc220d78751b8dc524/
? start = 234055 & end = 234055

    OR

GET
/sequence/6681ac2f62509cfc220d78751b8dc524/
? start = 67 & end = 234056

    OR

GET
/sequence/6681ac2f62509cfc220d78751b8dc524/
? start = 234055 & end = 234056

    OR

GET
/sequence/3332ed720ac7eaa9b3655c06f6b9e196/
? start = 5384 & end = 5

```

```
HTTP/1.1 400 Bad Request
Date: <date>
```

##### Case 4
start > end;  
Circular sequences **not** supported by the server;  

Server MUST respond with a `501 Not Implemented` error. Doesn't matter the type of sequence (circular or non-circular).


```
GET
/sequence/6681ac2f62509cfc220d78751b8dc524/
? start = 234000 & end = 671
```

```
HTTP/1.1 501 Not Implemented
Date: <date>
```



## Non-circular sequence
##### Case 1
start > end;  
circular sequences are supported by the server  

But since sequence is not circular, server MUST repond with a `416 Range Not Satisfiable` error.

```
GET
/sequence/6681ac2f62509cfc220d78751b8dc524/
? start = 234000 & end = 671
```

```
HTTP/1.1 416 Range Not Satisfiable
Date: <date>
```
