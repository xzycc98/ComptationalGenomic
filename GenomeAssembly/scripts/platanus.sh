#! /bin/bash

#./platanus.sh -p /home/groupb/bin/tools/ -d /home/groupb/data -o /home/groupb/platanus_output/

function HELP {
	echo "The Platanus_B shell script requires flags, -p, -d, and -o for the path to the platanus executable, path to the data (fasta files), and the desired output directory, respectively."
	echo "Users can also submit optional flags -t, -k, and -K for threads, minimumn k size, and maximum k factor, respectively."
	echo "Minimum k size is 32 by default."
	echo "Maximum k factor is 0.5 by default. Maximum K = FLOAT*Read_Length"
	exit 2
}

threads=1
mink=32
maxk=0.5

while getopts "p:d:o:t:k:K:v" option; do 
	case $option in
		p) platanus_dir=$OPTARG;;
		d) data_dir=$OPTARG;;
		o) output=$OPTARG;;
		t) threads=$OPTARG;;
		k) mink=$OPTARG;;
		K) maxk=$OPTARG;;
		v)set -x;;
		\?) HELP;;
	esac
done

let start_time="$(date +%s)"
echo "$platanus_dir is the platanus directory"
echo "$data_dir is the data directory"

#Append files from file directory to file list
file_list=()
for FILE in $data_dir/*;
do 
	extension="${FILE##*/}"
	if [[ $extension == *"CGT"* ]]; then
		file_list+="$FILE/$extension.fa "
	fi
done


reads="${file_list[@]}"
reads=${reads::-1} #Removal of last space
#echo $reads
cd $platanus_dir

echo "Running Platanus_B"
./platanus_b assemble -f $reads -t $threads -k $mink -K $maxk -o $output 2>log
#Assemble with list of reads and output both out_contig.fa and log
let current_time="$(date +%s)"
let seconds=$current_time-$start_time
echo "Platanus_B Runtime: $seconds"
