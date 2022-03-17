#!/usr/bin/env python3

"""
Pre-Requisites:
1. All assembly software are pre-installed and added to the path
2. Input data files are in zipped fastq format (.fq.gz) and each isolate is present in a separate directory
3. Current pipeline is designed for paired end reads.
"""

"""
Fixes in next update:
1. Current version assumes directories begin with CGT (Due to extra files in the same directory)
2. Check if input directories are correctly specified with backward slash at the end
3. Account for difference in forward and backward slash across windows and linux
4. Allow the user to pick the final contigs file based on QUAST results
5. Clear temp files
6. Accept choice of assembler - individual, best, combined (meta-assembly)
7. Accept choice of k-list
8. Check if software are installed
9. Parallelize the runs for each software
10. Accommodate single-ended reads 
11. Add threads option for each assembler - currently running on default
"""

"""
ToDo:
1. Move Final contigs to Quast Folder
2. Confirm FASTQC and Trimmomatic Commands
"""

import subprocess
import shlex
import os
import sys
import shutil
import argparse

POSTQC_DIR = "./PostQCReports/"
PREQC_DIR = "./PreQCReports/"
QUAST_DIR = "./QuastReport/"
# input_dir = "/home/groupb/data/"
# output_dir = "/home/groupb/output/"
ERROR_LOG = "errors.txt"


def run_quast(output_dir):
    #Move contig files to Quast contig Folder
    ###

    global errors
    try:
        quast_command = f"quast.py ./contig/*.fasta -o ./test/"
        print(f"Running Quast for all assemblies with command: {quast_command} \n \n")
        subprocess.call(shlex.split(quast_command))
    except:
        errors += "Quast command didnt work"

def run_idba_ud(combined_reads,threads,output_dir):
    global errors
    idba_ud_path = os.path.join(output_dir, "idba_ud")
    os.mkdir(idba_ud_path)

    try:
        ## Converting fastq to fasta
        # Must be converted from fq to fa
        # Fastq files must be merged if paired-end: GT1005_1.fq + GT1005_2.fq -> GT1005.fq
        for isolate in combined_reads:
            fasta_extension = isolate.rstrip(".fq")
            fasta_extension += ".fa"
            fastq_2_fasta = f"fq2fa --paired --filter {isolate} {fasta_extension}"
            print(f"Converting fastq to fasta with command: {fastq_2_fasta} \n \n")
            subprocess.call(shlex.split(fastq_2_fasta))

        ## Run Assembly
        # ./ idba / bin / idba_ud - l fasta1.fa fasta2.fa... - o idba_output /
        # -l flag for reads greater than 128
        # --mink minimum k (<=124)
        # --maxk maximum k (<=124)

        idba_ud_assembly = f"idba_ud -l {combined_reads} -o {idba_ud_path}" #--num_threads
        print(f"Running idba_ud for all isolates together with command: {idba_ud_assembly} \n \n")
        subprocess.call(shlex.split(idba_ud_assembly))

    except:
        errors += "IDBA_UD didnt work"

def run_platanus_b(combined_reads,threads,output_dir):
    # This should output a out_contig.fa and an assemble.log
    # Optional -k flag -> minimum k-mer to initialize with (default=32)
    # Optional -K flag -> maximum k-mer
    global errors
    platanus_b_path =  os.path.join(output_dir, "platanus_b")
    os.mkdir(platanus_b_path)
    try:
        platanus_b_assembly = f"platanus_b -f {combined_reads} -o {platanus_b_path}"
        print(f"Running idba_ud for all isolates together with command: {platanus_b_assembly} \n \n")
        subprocess.call(shlex.split(platanus_b_assembly))
    except:
        errors += "PlatanusB did not work"

def run_spades(combined_reads,threads,output_dir):
    """
    k-list -> Odd Numbers only less than 150 greater 21
    :param combined_reads:
    :param threads: number of threads
    :param output_dir:
    :return:
    """
    global errors
    default_k_mer_list = "21,33,55,77"
    spades_path = os.path.join(output_dir, "spades")
    os.mkdir(spades_path)

    try:
        spades_assembly = f"spades.py -k {default_k_mer_list} --careful --only-assembler -s {combined_reads} -o {spades_path}"
        print(f"Running Spades for all isolates together with command: {spades_assembly} \n \n")
        subprocess.call(shlex.split(spades_assembly))
    except:
        errors += "Spades didnt work"

def run_megahit(forward_reads,backward_reads,threads,output_dir):
    global errors
    default_k_mer_list = "21,29,33,39,55,59,77,79,99,119,125,141"
    megahit_path = os.path.join(output_dir, "megahit")
    os.mkdir(megahit_path)

    try:
        megahit_assembly = f"megahit --k-list {default_k_mer_list} -1 {forward_reads} -2 {backward_reads} -o {megahit_path}"
        print(f"Running Megahit for all isolates together with command: {megahit_assembly} \n \n")
        subprocess.call(shlex.split(megahit_assembly))
    except:
        errors += "Megahit did not work"

def run_assembly(input_dir, threads, output_dir):
    global ERROR_LOG
    forward_reads, backward_reads, combined_reads = parse_trimmed_inputs(input_dir)
    errors = ""

    run_megahit(forward_reads,backward_reads,threads,output_dir)
    run_spades(combined_reads,threads,output_dir)
    run_idba_ud(combined_reads,threads,output_dir)
    run_platanus_b(combined_reads,threads,output_dir)

    with open(ERROR_LOG, "w+") as file:
        file.write(errors)

def parse_trimmed_inputs(input_dir):
    """
    :param input_dir:
    :return: list of forward reads and backward reads for all isolates combined
    """
    global errors
    input_dir = input_dir.rstrip("/")
    input_dir += "/" #Ensuring that the slash is not repeated twice

    forward_reads = []
    backward_reads = []
    combined_reads = []

    for isolate in os.listdir(input_dir):
        if "CGT" in isolate:
            forward_reads.append(f"{input_dir}{isolate}/{isolate}_1.fq")
            backward_reads.append(f"{input_dir}{isolate}/{isolate}_2.fq")
            combined_reads.append(f"{input_dir}{isolate}/{isolate}.fq")

    return forward_reads, backward_reads, combined_reads

def run_trimmomatic(untrimmmed_forward_reads,untrimmmed_backward_reads):
    """
    :param untrimmmed_forward_reads: List of raw input forward reads in zipped fastq format
    :param untrimmmed_backward_reads: List of raw input backward reads in zipped fastq format
    :return: Trimmed and combined input files in same directory
    """
    for read_no in range(len(untrimmmed_forward_reads)):
        output1 = untrimmmed_forward_reads[read_no].rstrip(".gz")
        output2 = untrimmmed_backward_reads[read_no].rstrip(".gz")
        output1_unpaired = untrimmmed_forward_reads[read_no].rstrip(".fq.gz") + "_unpaired.fq"
        output2_unpaired = untrimmmed_backward_reads[read_no].rstrip(".fq.gz") + "_unpaired.fq"

        try:
            #Trimming the forward and backward reads
            trimmomatic_command = f"trimmomatic PE {untrimmmed_forward_reads[read_no]} {untrimmmed_backward_reads[read_no]} {output1} {output1_unpaired} {output2} {output2_unpaired} HEADCROP:10 TRAILING:20 SLIDINGWINDOW:4:20 AVGQUAL:20 MINLEN:75"
            print(f"Running Trimmomatic with command: {trimmomatic_command} \n \n")
            subprocess.call(shlex.split(trimmomatic_command))

        except:
            print(f"Error with Trimmomatic for {untrimmmed_forward_reads[read_no]}")

        try:
            #Combining the trimmed forward and backward reads
            combined_output = untrimmmed_forward_reads.rstrip("_1.fq.gz") + ".fq"
            combine_command = f"cat {output1} {output2} > {combined_output}"
            print(f"Running fastq cat command: {combine_command} \n \n")
            subprocess.call(shlex.split(combine_command))

        except:
            print("Error in combining trimmed files into single fastq file")

def run_fastqc(forward_reads, backward_reads, output_dir):
    """
    :param forward_reads: list of forward reads
    :param backward_reads: list of backward or reverse reads
    :param output_dir: output directory for html reports from fastqc
    :return:
    """
    for read_no in range(len(forward_reads)):
        try:
            fastqc_command = f"fastqc {forward_reads[read_no]} {backward_reads[read_no]} -o {output_dir}"  # --num_threads
            print(f"Running FASTQC with command: {fastqc_command} \n \n")
            subprocess.call(shlex.split(fastqc_command))

        except:
            print(f"Error with FASTQC for {forward_reads[read_no]}")

def perform_qc_trimming(input_dir):
    global PREQC_DIR, POSTQC_DIR

    input_dir = input_dir.rstrip("/")
    input_dir += "/" #Ensuring that the slash is not repeated twice

    untrimmmed_forward_reads = []
    untrimmmed_backward_reads = []
    for isolate in os.listdir(input_dir):
        if "CGT" in isolate:
            untrimmmed_forward_reads.append(f"{input_dir}{isolate}/{isolate}_1.fq.gz")
            untrimmmed_backward_reads.append(f"{input_dir}{isolate}/{isolate}_2.fq.gz")

    run_fastqc(untrimmmed_forward_reads,untrimmmed_backward_reads,PREQC_DIR)
    run_trimmomatic(untrimmmed_forward_reads,untrimmmed_backward_reads)
    forward_reads, backward_reads, combined_reads = parse_trimmed_inputs(input_dir)
    run_fastqc(forward_reads, backward_reads, POSTQC_DIR)

def create_output_directories(output_dir):
    ## Removing Output Directory if it already exists
    if os.path.exists(output_dir) and os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    ## Creating a new output directory
    os.mkdir(output_dir)

def sanity_check(input_dir):
    #Checking if Input directory exists
    if os.path.exists(input_dir):
        exit_code = 0
    else:
        exit_code = 1
    return exit_code

def main():
    global threads
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--output", help="Output Directorry", required=False, type=str)
    parser.add_argument("-i", "--input", help="Input Directory", required=True, type=str)
    parser.add_argument("-t", "--threads", help="Number of Threads to use", required=False, type=int)
    #k-list -> Odd Numbers only less than 150 greater 21 (Add condition during argparse)
    # parser.add_argument("-k", "--k-mer", nargs='*', action ="append" help="k-mer list", required=False)
    # parse.add_argument("-a")

    args = parser.parse_args()

    if args.threads is None or args.threads > 4:
        threads = 4 #Ensuring not more than 4 threads are used
    else:
        threads = int(args.threads)

    if sanity_check(args.input)==0:
        sys.exit()

    ## Create output directories
    create_output_directories(args.output)

    ## Perform Initial QC and Trimming
    perform_qc_trimming(args.input)

    ## Running De-Novo Assembly using the trimmed reads
    run_assembly(args.input,threads,args.output)

    ## Run QUAST for post assembly QC
    run_quast(args.output)

if __name__ == "__main__":
    main()

