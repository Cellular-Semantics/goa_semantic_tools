
schema

src/goa_semantic_tools/goa_semantic_tools/schemas/go_enrichment_output.schema.json

example

/Users/do12/Documents/GitHub/goa_sementic_tools/results/enrichment_6_genes.json

There is a lot of redundancy in direct annotations

e.g. 
```json
{
          "direct_annotations": [
            {
              "go_id": "GO:0007095",
              "go_name": "mitotic G2 DNA damage checkpoint signaling",
              "evidence_code": "IBA"
            },
            {
              "go_id": "GO:0007095",
              "go_name": "mitotic G2 DNA damage checkpoint signaling",
              "evidence_code": "IMP"
            },
            {
              "go_id": "GO:0007095",
              "go_name": "mitotic G2 DNA damage checkpoint signaling",
              "evidence_code": "IMP"
            }...
```
It would be much better to have the GO term mentioned once, then the various evidence codes.  For future use, we would ideally include a list of supporting refs (PMIDs, DOIs) with each evidence code.

