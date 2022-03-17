#!/bin/bash

for i in $(ls -1 /home/groupb/spades.sample.out/contigs_name/* | sed 's/_contigs.fasta//');
do
echo "${i}"_contigs.fasta
prokka --outdir /home/groupb/Gene_Prediction/prokka/"${i##*/}" --prefix "${i##*/}" --quiet --rfam --kingdom Bacteria"${i}"_contigs.fasta
done

#DONE
