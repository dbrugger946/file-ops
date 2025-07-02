#!/bin/bash
script="$0"
input_file="$1"
base_dir="$2"
tenth="${10}"
echo "The script name : $script"
echo "The input file of sub directories :  $input_file"
echo "The base directory for input/output : $base_dir"
echo "***********************************************"

# may want to override base_dir
# base_dir=/Users/dbrugger/projects2/notebooklm
# also, may want to paramaterize source and destination subfolders

    
while read -r sub_dir_name; do
    # echo $dir_name
    # echo $base_dir
    python ../subfolder-file-copy.py $base_dir"/Engagements/"$sub_dir_name $base_dir"/consolidated-files/25june2025/"$sub_dir_name           
done < $input_file

