#!/bin/bash

cd /home/groupc/files/gene_prediction/prokka

#conda activate team3_prokka


for i in $(ls -1 /home/groupc/files/genome_assembly/spades/spades_contigs_all_careful/* | sed 's/_contigs.fasta//');
do
echo "${i}"_contigs.fasta
prokka --outdir /home/groupc/files/gene_prediction/prokka/output/"${i##*/}" --prefix "${i##*/}" --quiet "${i}"_contigs.fasta
done

#DONE
