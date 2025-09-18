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
# example run :  (file-ops) user1@matros:~/projects/file-ops/scripts$ ./run-selected-dirs-linux.sh ./dirs.txt /home/user1/projects/notebooklm/Engagements-20250707T152647Z-1-001

    
while read -r sub_dir_name; do
    
    # python ../argview.py "$base_dir/Engagements/$sub_dir_name" $base_dir"/consolidated-files/$sub_dir_name" 

    python ../subfolder-account-copy-libreoffice.py "$base_dir/Engagements/$sub_dir_name" $base_dir"/consolidated-files/$sub_dir_name"     

done < $input_file

