Reference Servers will consists of two `GET` APIs.

 * GET Sequence by ID `/sequence/:id`  
 * GET Metadata by ID `/sequence/:id/metadata`

Detailed specifications regarding these APIs are covered in the doc, available [here](https://docs.google.com/document/d/1q2ZE9YewJTpaqQg82Nrz_jVy8KsDpKoG1T8RvCAAsbI/edit)

Important points :

 * Servers **MAY** or **MAY NOT** support circular sequences
 * Servers **MUST** implement MD5 while truncated SHA512 is optional
 * Server **MAY** support a `301 Moved Permanently` and `Location` header redirecting the client to retrieve sequence data from an alternative location.
