#!/usr/bin/env python

import subprocess
import shlex
import os
import sys
import shutil
import argparse



# output_dir = "/home/groupb/Gene_Prediction/NODE1_anno"


def run_prokka(input_dir,output_dir):
    global errors
   # prokka_path =  os.path.join(output_dir, "prokka")

    try:
       # prokka_command = f"prokka ../spades.out/scaffolds.fasta --outdir ../Gene_Prediction/prokka --metagenome --kingdom Bacteria"
        prokka_command = f"prokka {input_dir} --outdir {output_dir} --kingdom Bacteria --rfam"
        print(f"Running Prokka for gene prediction: {prokka_command} \n \n")
        subprocess.call(shlex.split(prokka_command))
    except:
        errors += "Prokka didnt work"


def main():
    global threads
    parser = argparse.ArgumentParser()
   # parser.add_argument("-t", "--threads", help="Input thread number", required=False, type=int)
    parser.add_argument("-i", "--input_dir", help="Input assembly fasta", required=True, type=str)
    # parser.add_argument("-k", "--kingdom", help="Input kingdom:Archaea|Bacteria|Mitochondria|Viruses", required=False, type=str)
    parser.add_argument("-o", "--output_dir", help="Input prokka's output directory", required=False, type=str)


    args = parser.parse_args()
    input_dir = args.input_dir
    output_dir= args.output_dir
    # if args.threads is None or args.threads > 4:
      #  threads = 4 #Ensuring not more than 4 threads are used
    # else:
      #  threads = int(args.threads)

    run_prokka(input_dir,output_dir)

if __name__ == "__main__":
    main()