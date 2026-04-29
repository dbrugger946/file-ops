#!/bin/bash
script="$0"
input_file="$1"
base_dir="$2"

echo "The script name : $script"
echo "The input file of sub directories :  $input_file"
echo "The base directory for input/output : $base_dir"
echo "***********************************************"

# may want to override base_dir
# base_dir=/Users/dbrugger/projects2/notebooklm
# also, may want to paramaterize source and destination subfolders

# example run :  run from /Users/dbrugger/projects2/notebooklm/file-ops/scripts
# ./run-subfolder-template-check-mac.sh ./dirs.txt /Users/dbrugger/projects2/notebooklm/Engagements-20260429T131439Z

    
while read -r sub_dir_name; do
    
    python ../subfolder-template-check-libreoffice-mac.py "$base_dir/$sub_dir_name" $base_dir"/consolidated-files/$sub_dir_name"     

done < $input_file

