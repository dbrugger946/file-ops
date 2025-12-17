import os
import subprocess
import shutil
import argparse
import sys
import logging
import csv
from datetime import datetime

# Create and configure logger
logging.basicConfig(filename="conversion.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')


# Creating an object
logger = logging.getLogger()

# Setting the threshold of logger to DEBUG
logger.setLevel(logging.DEBUG)

# Need to turn off logging at some point
#
# This will disable all logging calls with a severity level of CRITICAL or less
# (effectively all standard logging)
# logging.disable(logging.CRITICAL)

# Create and open a csv file for tracking filtered files
csv_file = open("csv-file-tracker.csv", 'w', newline='')
csv_writer = csv.writer(csv_file)
# Writing a header row
csv_writer.writerow(['Sales Region', 'Account Folder', 'Downloaded (docx) FileName','creation date','modified date','size (kb)','Completion Level', 'pdf version link'])


def convert_file_to_pdf(file_path, output_dir):
    """ This function calls libreoffice directly in the linux env
    and converts docx files into pdfs, and puts the new pdfs in the target  
    or consolidated directory"""

    try:
        result = subprocess.run(
            f'flatpak run org.libreoffice.LibreOffice \
            --headless \
            --convert-to pdf \
            --outdir "{output_dir}" "{file_path}"', capture_output=True, text=True, shell=True, check=False)
        
        logging.debug(f"Command executed successfully: {result.args}")
        logging.debug(f"Stdout:\n{result.stdout}")
        if result.stderr:
            logging.warning(f"Stderr:\n{result.stderr}")
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {e.args}")
        logging.error(f"Stderr:\n{e.stderr}")
    except FileNotFoundError:
        logging.error("Command not found. Check if the executable is in your PATH.")

    logger.debug(f"*** Convert input {output_dir} {file_path}" )
    
    pdf_file_path = f'{output_dir}/{file_path.rsplit("/", 1)[1].split(".")[0]}.pdf'

    logger.debug(f"=====: {pdf_file_path}")
    
    if os.path.exists(pdf_file_path):
        return pdf_file_path
    else:
        return None


def copy_files_to_single_folder(source_directory, target_directory):
    """
    a function that copies all the files from subdirectories within a source_directory
    into a single target_directory.

    there is some hardcoded filtering for document type and directory name, which could be pushed up as optional args
    """
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    copied_count = 0
    for root, _, files in os.walk(source_directory):
        for file in files:
            source_path = os.path.join(root, file)
            target_path = os.path.join(target_directory, file)

            # by default looks at all account subdirs across all regions, can be constrained
            if True:
                logger.debug(f" \t\t >>>>>current (root): {root} <<<")

                # for now only grab certain types of files
                init_base, init_ext = os.path.splitext(file)
                if init_ext == ".docx" or init_ext == ".pdf":                    
                    try:
                        copied_count += 1
                        print(f"Current Sub Directory File Count: {copied_count}")
                        # if .docx then convert to .pdf and save to target location
                        if init_ext == ".docx":
                            # the conversion function also puts the new pdf in the target directory
                            pdf_file = convert_file_to_pdf(source_path,target_directory)
                            logger.debug(f"--------- {pdf_file}")
                            logger.debug(f">>Copied {copied_count} :{source_path} >>> {pdf_file}\n")

                            if "After Action Report" in init_base :  

                                statinfo = os.stat(source_path)
                                create_date = datetime.fromtimestamp(statinfo.st_ctime)
                                modified_date = datetime.fromtimestamp(statinfo.st_mtime)


                                file_size_bytes = os.path.getsize(source_path)
                                aar_template_size = 129516
                                completion_flag = '4: undertermined'
                                if (aar_template_size + 100) >= file_size_bytes <= (aar_template_size + 400):
                                    completion_flag = '2: possibly'
                                elif (aar_template_size + 400 < file_size_bytes):
                                    completion_flag = '3: likely'
                                else:
                                    completion_flag = '1: unlikely'

                                file_size_kb = file_size_bytes / 1024
                                subdirname = os.path.basename(root)
                                # no_quotes_subdir = subdirname.replace('\"','')
                                no_quotes_subdir = subdirname.strip('\"')
                                sales_region = no_quotes_subdir.split("-")[0]
                                # print(f" {no_quotes_subdir} {file} {file_size}") 
                                # print(sales_region)
                                csv_writer.writerow([sales_region,no_quotes_subdir,file,create_date.date(),modified_date.date(), round(file_size_kb,2), completion_flag, pdf_file])

                        else: 
                            # source file is a pdf and it is just copied to target directory
                            shutil.copy(source_path, target_path)
                            logger.debug(f">>Copied: {copied_count} :{source_path} >>> {target_path}\n")
                    except Exception as e:
                        logger.debug(f"****** Error copying {source_path}: {e}")

    logger.debug(f"Final Converted and Copied File Count: {copied_count}")
    print(f"Final Converted and Copied File Count: {copied_count}")
    csv_file.close() 


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description= "A basic script to copy files nested in subdirectories into one target directory")
    parser.add_argument("source_folder", help="The folder where the source folders/files are located")
    parser.add_argument("target_folder", help="The single target folder for all the files")

    if (len(sys.argv) == 1 or len(sys.argv) == 2):
        logger.debug("2 arguments are required")
        parser.logger.debug_help()
        sys.exit(0)
    else:
        args = parser.parse_args()

    source_folder = args.source_folder
    target_folder = args.target_folder

    copy_files_to_single_folder(source_folder, target_folder)
    logger.debug("------------- File consolidation completed.\n\n")
