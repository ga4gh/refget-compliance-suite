## Get sequence by ID

The primary method for accessing specified sequence data. We can also query a sub-sequence either by using query params ```start``` and ```end``` or by using ```Range``` header in http request.

**URL** : `/sequence/:id`

**Method** : `GET`  

**Auth Required** : YES  

**Default Encoding** : text  
```Content-type: text/vnd.ga4gh.seq.v1.0.0+plain
```  
Unless negotiated with the client and allowed by the server  

#### URL params
**id** (required)  
A string specifying the sequence to be returned. The identifier shall be a checksum derived from the sequence using one of the supported checksum algorithms, or an alias for the sequence supported by the server. You can have a look at checksum algrorithm currently in use [here](checksum.md)

#### Query params
**start** (optional)  
The start position of the range on the sequence, 0-based, inclusive.

**end** (optional)  
The end position of the range on the sequence, 0-based, exclusive.

#### Headers
**Range** (optional)  
[RFC 7233](https://tools.ietf.org/html/rfc7233). Current spec doesn't allow multiple parts as specified in rfc.  
0-based inclusive of start and end bytes specified.

**Accept** (optional)  
Defaults to text/plain, unless negotiated with the client and supported by the server.