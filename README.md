# GBS_report_writer
A collection of scripts for generating reports in LaTeX format for the different stages of GBS analysis. All scripts are executable in Python3. `tex_writer.py` is to run directly from within the specific 'report_writer' scripts, so there should be no need to generate it automatically. 

## Required files
All report writer scripts require a Config file and a requesite template.tex file, in addition to the specific additional files. See info below for what each specific report writer needs. 

## QC_report_writer.py
```
usage: QC_report_writer.py [-h] [-v] Sample_file Summary_file Config_file

Minimum information needed in Config file: PROJECTID DATE MULTIPLEX BLANKS

positional arguments:`
  Sample_file    The sample .xlsx file provided by the client`
  Summary_file   The summary .ods (or equivalent) file generated following sequencing`
  Config_file    The config file with all additional information`

options:
  -h, --help     show this help message and exit
  -v, --Verbose  Display additional comments for debugging
  ```
  
