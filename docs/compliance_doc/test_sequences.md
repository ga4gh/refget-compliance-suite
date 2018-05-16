# Test sequences

There are three sequence used in the compliance documentation for sample queries and in compliance test suite for API Testing

 * NC_001422.1 Enterobacteria phage phiX174 sensu lato  
    [fasta sequnce](./circular.faa)  
    Circular Sequence  
    Size : 5384

 * I Saccharomyces_cerevisiae chromosome:R64-1-1:I:1:230218:1  
    [fasta sequence](./samples.faa)  
    Non-circular Sequence  
    Size : 234055

 * VI Saccharomyces_cerevisiae chromosome:R64-1-1:VI:1:270161:1  
    [fasta sequence](./samples.faa)  
    Non-circular sequence  
    Size : 274664


_Note : Fasta sequences of non-circular sequences are in same file_

Checksums for these sequences can be found [here](./checksums.txt)
These checksums will be used as identifiers in sequence retrieval and metadata retrieval APIs. There are currently two types of checksum algorithms in use:
 * MD5
 * Truncated SHA512

Implementation details of these algorithms are given in API specification doc [here](https://docs.google.com/document/d/1q2ZE9YewJTpaqQg82Nrz_jVy8KsDpKoG1T8RvCAAsbI/edit#heading=h.h66j2ox4ydtw).  
**Reference Server can implement either one or both of these algorithms**
