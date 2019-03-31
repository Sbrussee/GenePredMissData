# Get input:

# Obo file download:
wget -q http://current.geneontology.org/ontology/go-basic.obo 

# Rat gaf download ebi:
wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/UNIPROT/goa_uniprot_all.gz -O goa_mouse.gaf

# Mouse gaf download ebi:
wget ftp://ftp.ebi.ac.uk/pub/databases/GO/goa/UNIPROT/goa_uniprot_all.gz -O goa_rat.gaf

# Organism rattus Download from uniprot:
wget -q ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/UP000002494_10116.fasta.gz -O rat.fa.gz
gunzip rat.fa.gz

# Organism mouse download from uniprot
wget -q ftp://ftp.uniprot.org/pub/databases/uniprot/current_release/knowledgebase/reference_proteomes/Eukaryota/UP000000589_10090.fasta.gz -O mouse.fa.gz
gunzip mouse.fa.gz

# Create db for rat
makeblastdb -in rat.fa -dbtype 'prot' -out rat

# Blast proteins mouse against the rat db
blastp -query mouse.fa -db rat -outfmt "6 qseqid score sseqid" -out out.txt


