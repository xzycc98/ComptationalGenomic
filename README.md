# 1. GenomeAssembly

## Tools Installation

```
conda install -c bioconda fastqc
conda install -c bioconda trimmomatic
conda install -c bioconda quast

## SPAdes Installation

To download SPAdes Linux binaries and extract them, go to the directory in which you wish SPAdes to be installed and run:

    wget http://cab.spbu.ru/files/release3.15.2/SPAdes-3.15.2-Linux.tar.gz
    tar -xzf SPAdes-3.15.2-Linux.tar.gz
    cd SPAdes-3.15.2-Linux/bin/
In this case you do not need to run any installation scripts – SPAdes is ready to use. We also suggest adding SPAdes installation directory to the PATH variable.

## Platanus_B Installation

To download Platanus_B binaries, go to the directory in which you wish to install Platanus_B and run:

    git clone https://github.com/rkajitani/Platanus_B.git
    cd Platanus_B
    make
    cp platanus_b <installation_path>

Platanus_B also requires the installation of OpenMP (to compile the source code), Minimap2 (for the assembly of long reads), and Perl (to execute the scripts).
Linux 64 bit binary (precompiled) can also be downloaded here: http://platanus.bio.titech.ac.jp/platanus-assembler/platanus-1-2-4

## IDBA_UD Installation 

To download IDBA_UD binaries, go to the directory in which you wish to install IDBA_UD and run:

    git clone https://github.com/loneknightpy/idba.git
    cd idba
    ./build.sh

IBDA_UD requires GCC to compile source code. All IDBA executables will be listed under the bin directory in IDBA upon installation. 
```
## Pre Trimming Quality assessmnet with FastQC
The fastQC command used was
```
fastqc *_1.fastq  *_2.fastq
```
## Trimming
Trimming was done using trimmomatic. The following command was used
```
trimmomatic PE input_1.fq.gz input_2.fq.gz output_1.fq output_1_unpaired.fq output_2.fq output_2_unpaired.fq HEADCROP:10 TRAILING:20 SLIDINGWINDOW:4:20 AVGQUAL:20 MINLEN:75

cat output_1_unpaired.fq output_2_unpaired.fq > merged_output.fq
```


## De Novo Assembly Quality Assessment with QUAST
Using [QUAST v5.0.2](http://quast.sourceforge.net/install.html) for post-QC evalution and visualization. 

After replacing module ```cgi.escape``` to ```html.escape``` in ``` quast_libs/site_packages/jsontemplate/jsontemplate.py ```.

Run following code and direct to ```report.pdf``` to check the evalution result of the assemblers.
```
quast.py <spades_contigs.fasta> <megahit_contigs.fasta> <platanus_contigs.fasta> <idba_contigs.fasta> -o /quast/output
```
## Integration of multiple genome assemblies using Contig Integrator for Sequence Assembly(CISA)
[CISA v1.3](http://sb.nhri.org.tw/CISA/en/CISA) basically consists of four major phases:
* Identification of the representative contigs and possible extensions
* removal and splitting of the contigs that may be misassembled, and clipping of uncertain regions that are located at the extremities of the contigs
* iterative merging of the contigs with a minimum 30% overlap and estimating the maximal size of repetitive regions
* merging of the contigs based on the size of repetitive regions

Prerequisite

* MUMmer 3.22 or higher

* BLAST 2.2.25+ or higher

* python2.X

Installation
```
conda install -c bioconda mummer
conda install -c bioconda blast
wget ftp://sb.nhri.org.tw/CISA/upload/en/2014/3/CISA_20140304-05194132.tar
tar xf CISA_20140304-05194132.tar
```

Create the merge.config configuration file
```
count=4 
data=spades.fasta,title=spades
data=platanus.fasta,title=platanus
data=megahit.fasta,title=megahit
data=idba.fasta,title=idba
Master_file=merge_contigs.fa
min_length=100
Gap=11
```
Merge contigs
```
Merge.py merge.config
```
Create the cisa.config configuration file
```
genome=n (Fill in the largest total length in assemblies quast report)
infile=merge_contigs.fa
outfile=final_contig.fa
nucmer=/tool/path/MUMmer3.23/nucmer
R2_Gap=0.95 (default:0.95)
CISA=/tool/path/CISA1.3
makeblastdb=/tool/path/makeblastdb
blastn=/tool/path/blastn
```
CISA
```
CISA.py cisa.config
```
## Evaluate meta_contig with best assembly from single assembler using Quast
```
quast.py <cisa_contig.fasta> <best_assembly.fasta>  -o /path/to/output
```







# 2. GenePrediction


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
