#!/bin/bash


if [ ! -d quast ];
then
	mkdir post_QC/test #To store output files
fi

#main quast command
python /home/groupb/bin/tools/quast/quast.py /home/groupb/analysis/Team2-GenomeAssembly/post_QC/contig/*.fasta -o /home/groupb/analysis/Team2-GenomeAssembly/post_QC/test

echo "Based on the quast report, the ideal assmbly tool is: 'SPADES'."
echo "Please direct to /home/groupb/analysis/Team2-GenomeAssembly/de_novo/spades for the final whole genome output."


