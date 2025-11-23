## Various utility apps for files  

virtual python env was set to Python 3.10.17  (using uv)  


- copies all the files recursively in sub folders/directories into one folder, helpful with NotebookLM source adds  
    - subfolder-file-copy.py    
- copy functionality from subfolder-file-copy.py adds code for docx to pdf conversion via LibreOffice on Linux
    - subfolder-file-copy-libreoffice.py  
- (under construction, needs more logic from libreoffice version) same as above but adds expected code for converting docx to pdf on Mac and Windows machines with MS Word installed.
    - subfolder-file-copy-msoffice.py  

Recommended to use scripts in **scripts** directory to run utilities


### uv usage for python env

#### uv info
https://docs.astral.sh/uv/concepts/projects/init/#applications  

### setting up python virtual env

NOTE:   If have pre-existing *.toml or just cloned repo from git  
-- if starting with existing *.toml then just use  
**uv venv .venv**  
-- may need to manually adjust created pyproject.toml python version setting,     
and may need to run uv python pin before running uv run ...  
-- may need to deal with uv.lock, .python-version

Else: if starting from scratch, then create new project with:  
***uv init tutorial  
cd tutorial  
uv sync --python 3.10***  
-- may need to manually adjust created pyproject.toml python version setting, 


-- add cli's packages etc ie. 
***uv add llama-stack   
source .venv/bin/activate***  
or  
***source .venv/Scripts/activate***  

other possible commands  
uv run python <somthing.py>  



    


