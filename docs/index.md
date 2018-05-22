Welcome to Reference Sequence Rerieval Servers Compliance documentation.

## Reference Sequence Retrieval Servers
The Reference Sequence Retrieval Servers enables bulk access to reference genomic sequences and their metadata using an identifier which will be derieved from the sequence itself. Reference Servers can be queried for complete sequence as well as sub-sequences.

## Compliance Document
This documentation is primarily for the implementers of Reference Servers. Implementers **MUST** adhere to the documentation during the development phase of servers. This document uses 3 test sequences, two non-circular and one circular (**Circular sequence support in the Reference Server is optional**. Changes in the response w.r.t this support will be covered in later sections) for all the sample queries and error conditions. Testing suite for the Reference Server will also consists of these three sequences for API testing. All the implementations of Reference Servers **MUST** comply with the reponses mentioned w.r.t these sequences.
