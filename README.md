# Run an in silico PCR using IPCress and parse results

IPCress is a tool from the exonerate package:   
https://www.ebi.ac.uk/about/vertebrate-genomics/software/ipcress-manual

It can be run on the cluster using:   
```sbatch run_iPCRress_insilicoPCR.sh```  

needing as input:
- primer information (/test/input/db.txt)
- fasta db (/test/input/db.fasta)

A parser for the output from IPCress in python can be run using:
```python iPCRess_parser.py iPCRess_output.txt out_parse.csv out_parse.fasta```

It will create a fasta file with the PCR products and a csv containing miscallenous information about the PCR results including:
- Gene
- Strain
- Size in bp
- Direction
- Start position
- Stop position
- Primer matches
