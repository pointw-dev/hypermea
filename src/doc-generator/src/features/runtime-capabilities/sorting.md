# Sorting

You can request that resource collections be sorted. Sorting is based on any field name (or field names), and can be ascending or descending.

## Basic sorting request
An example is worth a dozen paragraphs:

```bash
 curl -i http://localhost:2112/people?sort=city,-lastname
 ```

This sorts the people collection first by `city`, then by `lastname` descending.


