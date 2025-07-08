import os
import subprocess
import shutil
import argparse
import sys


def convert_file_to_pdf(file_path, output_dir):
    subprocess.run(
        f'flatpak run org.libreoffice.LibreOffice \
        --headless \
        --convert-to pdf \
        --outdir "{output_dir}" "{file_path}"', shell=True)
    
    print(f"*** Convert inputs: {output_dir} {file_path}" )
    
    pdf_file_path = f'{output_dir}{file_path.rsplit("/", 1)[1].split(".")[0]}.pdf'
    
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

            # only work with West accounts for now
            if  "West" in root:
                # print(f" \t\t >>>>>{root} <<<")

                # for now only grab certain types of files
                init_base, init_ext = os.path.splitext(file)
                if init_ext == ".docx" or init_ext == ".pdf":                    
                    try:
                        # if .docx then convert to .pdf and save to target location
                        if init_ext == ".docx":
                            # shutil.copy(source_path, target_path)
                            pdf_file = convert_file_to_pdf(source_path,target_directory)
                            # print(f"--------- {pdf_file}")
                        else: 
                            shutil.copy(source_path, target_path)
                        copied_count += 1
                        print(f"copied {copied_count} :{source_path} to {target_path}\n")
                    except Exception as e:
                        print(f"****** Error copying {source_path}: {e}")

    print(f"Final Copied File Count: {copied_count}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description= "A basic script to copy files nested in subdirectories into one target directory")
    parser.add_argument("source_folder", help="The folder where the source folders/files are located")
    parser.add_argument("target_folder", help="The single target folder for all the files")

    if (len(sys.argv) == 1 or len(sys.argv) == 2):
        print("2 arguments are required")
        parser.print_help()
        sys.exit(0)
    else:
        args = parser.parse_args()

    source_folder = args.source_folder
    target_folder = args.target_folder

    copy_files_to_single_folder(source_folder, target_folder)
    print("------------- File consolidation completed.\n\n")
