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
  
### Required files
- **Sample_file**:  
  A .xlsx or .ods file containing the client-supplied information. Multiple sheets labelled 'Sample Sheet n' can be included. 
- **Summary_file**: 
  The generated .ods file containing the count numbers in each sample, as well as summarised totals reads, average reacts, coefficient of variance and 10% of total reads. 
- **Config_file**: 
  The Config file containing all additional required information. See below for required information in the Config file. 

### Config file 
The config file needs to contain the following information with the corresponding labels, separated by a colon. 
- **PROJECTID**: The ID of the project which will be included in the report. This will also be used in the resulting file names. 
- **DATE**: The date of the project to be included in the report. 
- **MULTIPLEX**: The plexicity level of the analysis. 
- **BLANKS**: The number of blanks included *per sample page*. So, if there are two sample pages and a total of four blanks, only include a blank number of 2. 

Example Config file: 
```
PROJECTID: LOExxxx 
DATE: 10-02-2022 
MULTIPLEX: 94 
BLANKS: 1 
```

---
