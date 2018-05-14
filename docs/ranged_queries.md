## Ranged Sequence API queries

#### Successful Response

**1.**  
Simple API call to a non-circular chromosome, keeping deafult encoding and using `start` and `end` query params.   
_Request_
````
GET /sequence/959cb1883fc1ca9ae1394ceb475a356ead1ecceff5824ae7/
?start=10
&end=20
````

_Response_
````
HTTP/1.1 200 OK
Date: <date>
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 10
Content: CCCACACACC ````
