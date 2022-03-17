## 1. Genome assembly
• staring from FASTQ files – perform sequence read quality control (QC)

• perform genome assembly using multiple tools

• evaluate the performance of multiple tools (assembly metrics)

• combine tools and merge assemblies as needed

• deliverable #1 – QC and assembly pipeline

• deliverable #2 – FASTA files with assembled contigs to gene prediction


## 2. Gene prediction
• starting from assembled genomes – predict genes (features) using multiple tools

• compare the results of multiple tools

• validate ab initio predictions with homology

• combine tools and merge predictions as needed

• coherent gene naming scheme

• provide confidence levels for gene predictions

• deliverable #1 – gene prediction pipeline

• deliverable #2 – gff files for functional annotation group

• deliverable #3 – FASTA files for gene nucleotide and protein sequences


## 3. Functional annotation
• starting from gene (feature) predictions – predict various aspects of gene (protein) function

• perform both ab initio and homology-based prediction as appropriate

• aspects of function to predict – biochemical activity, molecular function, (sub)cellular localization, domain and motif composition, higher 
level features such as protein families or operons, enzymatic activity, virulence factors etc (note that this list is not exhaustive)

• deliverable #1 – functional annotation pipeline

• deliverable #2 – gff files for comparative genomics group

• deliverable #3 – annotated FASTA files for gene nucleotide and protein sequences


## 4. Comparative genomics
• combining data from all three previous analysis – compare genome sequences in order to perform outbreak analysis

• what is the identity of the species/strains that cause the outbreak?

• how are the isolates related to each other? how do they differ?

• which isolates correspond to outbreak versus sporadic strains?

• what are the virulence and antibiotic resistance profiles of the outbreak isolates?

• what is the recommended outbreak response and treatment?

• deliverable #1 – comparative genomics pipeline

• deliverable #2 – specific public health recommendations to CDC

## 5. Predictive webserver
• combining data from all four previous groups – create a predictive webserver that allows for automated analyses of your species of interest

• possible functional utility of the predictive webserver include
    • distance from the closest isolate in the database
    
    • assigning whether the uploaded isolate looks like outbreak or sporadic strain(s)
    
    • visualization of the distance between your isolate and database isolate as a phylogenetic tree and/or heatmap
    
    • virulence factor and antimicrobial resistance profiling of your isolates

• deliverable #1 – fully functional online predictive webserver

