Reference Servers MUST respond with adequate error codes for every error condition. Error conditions are documented in a hierarchical manner, i.e. first check are shown first.

## Generic Error Conditions

These conditions are first line of checks, failing these conditions would result in the specified error, no matter other parameters.

##### Case 1
**Unauthorized user**  
More information can be found in API spec, [here]()

```
HTTP/1.1 401 Unauthorized
```

##### Case 2
**ID not found**  
When ID provided in the request doesn't match any of the checksums of any sequence, server throws a `404 Not Found` error

```text
GET /sequence/some1111garbage11111id/
```

```
HTTP/1.1 404 Not Found
```

##### Case 3
**Unsupported media type by the server**  
When media type requested by the client in the `Accept` header is not supported by the server, server throws a `415 Unsupported Media Type` error

```text
GET /sequence/6681ac2f62509cfc220d78751b8dc524

Accept : text/<some-encoding-not-supported-by-server>
```

````
HTTP/1.1 415 Unsupported Media Type
````

## Error Conditions while using start / end parameters
### Circular or non-circular sequence
Important Points:

 * **CASE 4** of this section is only for servers which DO NOT support circular sequences.

###### Case 1  
When Range header is also passed along with start / end parameters, server must throw a `400 Bad Request` error even if both are retrieving the same sequence or sub-sequence with a valid identifier and valid encoding.

_Note: Only one of the two ways should be used to query a sub-sequence._

```text
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
    ?start=10
    &end=20

Range: bytes=10-19

```

```
HTTP/1.1 400 Bad Request
```

##### Case 2  
start and end are 32 bit-unsigned integers, when recieve any value other than that, server MUST throw a `400 Bad Request` error.  
On recieving only one of the start / end parameters, server MUST throw a `400 Bad Request` error.


```text
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
    ?start=abc
    &end=20

    OR

GET /sequence/6681ac2f62509cfc220d78751b8dc524/
    ?start=-10
    &end=-29

    OR

GET /sequence/6681ac2f62509cfc220d78751b8dc524/
    ?start=abc
```

```
HTTP/1.1 400 Bad Request
```

##### Case 3  
When  
`start >= size of sequence`  
OR  
`end > size of the sequence`

Here, size of the sequence is 230218

`6681ac2f62509cfc220d78751b8dc524` is a non-circular sequence; size = 230218  
`3332ed720ac7eaa9b3655c06f6b9e196` is a circular sequence; size = 5384

```text
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
    ?start=23021
    8&end=230218

    OR

GET /sequence/6681ac2f62509cfc220d78751b8dc524/
    ?start=67
    &end=230219

    OR

GET /sequence/6681ac2f62509cfc220d78751b8dc524/
    ?start=230218
    &end=230219

    OR

GET /sequence/3332ed720ac7eaa9b3655c06f6b9e196/
    ?start=5384
    &end=5

```

```
HTTP/1.1 400 Bad Request
```

##### Case 4  
start > end;  
Circular sequences **not** supported by the server;  

Server MUST respond with a `501 Not Implemented` error. Doesn't matter the type of sequence (circular or non-circular).


```text
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
    ?start=220218
    &end=671
```

```
HTTP/1.1 501 Not Implemented
```



### Non-circular sequence
Important Points:

 * **CASE 1** of this section is only for servers which support circular sequences.


##### Case 1
start > end;  
circular sequences are supported by the server  

But since sequence is not circular, server MUST repond with a `416 Range Not Satisfiable` error.

```text
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
    ?start=220218
    &end=671
```

```
HTTP/1.1 416 Range Not Satisfiable
```


## Error Conditions while using Range header

Notation:
    `Range: bytes=first-byte-spec - last-byte-spec`  
    For example : `Range: bytes=5-10`. Here 5 is first-byte-spec and 10 is last-byte-spec.

### Circular or non-circular sequence
##### Case 1
When start / end parameters are also passed along with Range header, server must throw a `400 Bad Request` error even if both are retrieving the same sequence or sub-sequence with a valid identifier and valid encoding.

_Note: Only one of the two ways should be used to query a sub-sequence._

```text
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
    ?start=10
    &end=20

Range: bytes=10-19

```

```
HTTP/1.1 400 Bad Request
```

##### Case 2
first-byte-spec and last-byte-spec are integers, when recieve any value other than that, server MUST throw a `400 Bad Request` error.  
On recieving only one of the first-byte-spec or last-byte-spec, server MUST throw a `400 Bad Request` error.  
Reference server must only accept `bytes` as unit in `Range` header else `400 Bad Request`


```text
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

##### Case 3
`first-byte-spec > last-byte-spec`  
As stated in [success response](../sequence.md) section, Range header must not be used to retrieve sub-sequences of a circular sequences across the origin. Server must respond with `400 Bad Request` error.  
Even if the sequence is non-circular and first-byte-spec > last-byte-spec, server must throw `400 Bad Request` error.

```text
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

```text
GET /sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=230218-230218

    OR

GET /sequence/6681ac2f62509cfc220d78751b8dc524/
Range: bytes=9999999-999999999999
```

```
HTTP/1.1 400 Bad Request
```
