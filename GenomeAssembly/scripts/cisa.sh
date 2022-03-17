#!/bin/bash

if [ ! -d meta ];
then
echo " Prerequiste: python2.X, MUMmer, blastn. makeblastdb "
echo " Please create merge.config and cisa.config file"

#	conda create -n python2.7 python=2.7
#	conda activate python2.7

# main cisa command
Merge.py /home/groupb/analysis/Team2-GenomeAssembly/post_QC/merge.config

CISA.py /home/groupb/analysis/Team2-GenomeAssembly/post_QC/cisa.config

#conda deactivate python2.7

echo "Meta assembly is done!"
fi
