Refget Servers MUST respond with adequate error codes for every error condition. Error conditions are documented in a hierarchical manner, i.e. first check are shown first.

## Generic Error Conditions

These conditions are first line of checks, failing these conditions would result in the specified error, no matter other parameters.

<h5> Case 1 </h5>
**ID not found**
When ID provided in the request doesn't match any of the checksums of any sequence, server must throw a `404 Not Found` error

```
GET /sequence/some1111garbage11111id/
```

```
HTTP/1.1 404 Not Found
```

<h5> Case 2 </h5>
**Unsupported media type by the server**
When media type requested by the client in the `Accept` header is not supported by the server, server must throw a `406 Not Acceptable` error

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524
Accept : text/exotic-encoding
```

```
HTTP/1.1 406 Not Acceptable
```

## Error Conditions while using start / end parameters

<h3> Circular or non-circular sequence </h3>
Important Points:

 * **CASE 4** of this section is only for servers which DO NOT support circular sequences.

<h5> Case 1 </h5>
When Range header is also passed along with start or end or both parameters, server must throw a `400 Bad Request` error even if both are retrieving the same sequence or sub-sequence with a valid identifier and valid encoding.

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/?start=10&end=20
Range: bytes=10-19

```

```
HTTP/1.1 400 Bad Request
```

<h5> Case 2 </h5>
start and end are 32 bit-unsigned integers, on receiving any invalid value, server must throw a `400 Bad Request` error.


```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/?start=abc&end=20

    OR

GET /sequence/6681ac2f62509cfc220d78751b8dc524/?start=-10&end=-29

    OR

GET /sequence/6681ac2f62509cfc220d78751b8dc524/?start=abc
```

```
HTTP/1.1 400 Bad Request
```

<h5> Case 3 </h5>

Start and end are specified.
start >= size of sequence
OR
end > size of the sequence
Server must throw a `416 Range Not Satisfiable` error.
`6681ac2f62509cfc220d78751b8dc524` is a non-circular sequence; size = 230218
`3332ed720ac7eaa9b3655c06f6b9e196` is a circular sequence; size = 5386

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/?start=230218&end=230218

    OR

GET /sequence/6681ac2f62509cfc220d78751b8dc524/?start=67&end=230219

    OR

GET /sequence/6681ac2f62509cfc220d78751b8dc524/?start=230218&end=230219

    OR

GET /sequence/3332ed720ac7eaa9b3655c06f6b9e196/?start=5386&end=5
```

```
HTTP/1.1 416 Range Not Satisfiable
```

<h5> Case 4 </h5>
**Note : Only for servers which do NOT support circular sequence**
start > end;
Server MUST respond with a `501 Not Implemented` error regardless of the type of sequence (circular or non-circular).

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/?start=220218&end=671
```

```
HTTP/1.1 501 Not Implemented
```


<h3> Non-circular sequence </h3>
Important Points:

 * **CASE 1** of this section is only for servers which support circular sequences.


<h5> Case 1 </h5>
**Note : Only for servers which supports circular sequence**
start > end;
But since sequence is not circular, server must throe a `416 Range Not Satisfiable` error.

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/?start=220218&end=671
```

```
HTTP/1.1 416 Range Not Satisfiable
```


## Error Conditions while using Range header

Notation:
    `Range: bytes=first-byte-spec - last-byte-spec`
    For example : `Range: bytes=5-10`. Here 5 is first-byte-spec and 10 is last-byte-spec.

<h3> Circular or non-circular sequence </h3>

<h5> Case 1 </h5>
When start or end or both parameters are also passed along with Range header, server must throw a `400 Bad Request` error even if both are retrieving the same sequence or sub-sequence with a valid identifier and valid encoding.

```
GET /sequence/6681ac2f62509cfc220d78751b8dc524/?start=10&end=20
Range: bytes=10-19

```

```
HTTP/1.1 400 Bad Request
```

<h5> Case 2 </h5>
first-byte-spec and last-byte-spec are integers, on recieving any invalid value, server must throw a `400 Bad Request` error.
On recieving only one of the first-byte-spec or last-byte-spec, server must throw a `400 Bad Request` error.
On recieving any unit other than bytes, server must throw a `400 Bad Request`.

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


<h5> Case 3 </h5>
first-byte-spec >= size of sequence

Regardless of the type of sequence (circular or non-circular) since first-byte-spec is inclusive and server must throw a `400 Bad Request` error.
Size of the sequence is 230218.

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

<h5> Case 4 </h5>
first-byte-spec > last-byte-spec
As stated in [success response](success.md) section, Range header must not be used to retrieve sub-sequences of a circular sequences across the origin. Server must throw a `416 Range Not Satisfiable` error.
Even if the sequence is non-circular and first-byte-spec > last-byte-spec, server must throw a `416 Range Not Satisfiable` error.

```
GET /sequence/3332ed720ac7eaa9b3655c06f6b9e196/
Range: bytes=5200-56
```

```
HTTP/1.1 416 Range Not Satisfiable
```
