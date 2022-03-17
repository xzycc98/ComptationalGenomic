# Team2-GenePrediction


## Tools Installation

```
## Prokka Installation
conda install -c conda-forge -c bioconda prokka
prokka --setupdb
```
```
## Prodigal Installation
conda install -c conda-forge -c bioconda prodigal
prokka --setupdb
```
```
## GeneMarkS Installation
wget http://topaz.gatech.edu/GeneMark/tmp/GMtool_fhCZT/gms2_linux_64.tar.gz
cp  gmhmmp2_key   ~/.gmhmmp2_key
```
```
## Glimmer Installation
conda install -c bioconda glimmer
```
```
## Balrog Installation
conda create -n balrog_env python=3.7
conda activate balrog_env
conda install -c conda-forge -c bioconda balrog mmseqs2
conda install -c pytorch pytorch torchvision torchaudio cpuonly
```
```
## MetaGeneAnnotator Installation
wget metagene.nig.ac.jp/metagene/mga_x86_64.tar.gz
tar xzf mga_x86_64.tar.gz
```
## Prediction 
## with Prokka
The command used was
```
prokka <assembly.fasta> --outdir <output/path/> --kingdom Bacteria --rfam
```
## with Prodigal
The command used was
```
prodigal -i <output/path/assembly.fasta> -o <output/path/output.gff> --output_format --output_format gff
```
## with Glimmer3
The command used was
```
build-icm [options] output_file < input-file
glimmer3 seq.fna output_file.icm result
#output will give two files: result.predict (gff file) and result.detail which lists out all the genes
```
## with GeneMarkS
The command used was
```
gms2.pl -s <sequence.fasta> --genome-type <TYPE (bacteria/archae/auto)> --output <Output.gff>

```
## with balrog
The command used was
```
balrog -i <sequence.fasta> -o <out.gff>
```
## with MetaGeneAnnotator
The command used was
```
mga <sequence.fasta> -s > out.txt
# To convert to gff3 (Tentative, not necessarily correct)
awk -v OFS='\t' -e 'BEGIN{print("##gff-version 3")}{if($1 ~ "#"){print($0)}else{print($1, "MetaGeneAnnotator", "CDS", $2, $3, $7, $4, $5, $6";"$8)}}' out.txt > out.gff
```
## with BLAT (Homology Based)
The command used was
```
blat </path/to/reference.fna> </path/to/contigs.fasta> -out=psl <blat.psl.out>
```
