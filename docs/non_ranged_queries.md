## Non Ranged Sequence API queries

#### Successful Response

**1.**  
Simple API call to a non-circular/circular chromosome, keeping deafult encoding. Server responds with `status code 200` and `message OK`.   
_Request_
````
GET /sequence/959cb1883fc1ca9ae1394ceb475a356ead1ecceff5824ae7/
````

_Response_
````
HTTP/1.1 200 OK
Date: <date>
Content-Type: text/vnd.ga4gh.seq.v1.0.0+plain; charset=us-ascii
Content-Length: 3365
Content: CCACA.....GTGGG ````
