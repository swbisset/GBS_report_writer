# GBS_report_writer
A collection of scripts for generating reports in LaTeX format for the different stages of GBS analysis. All scripts are executable in Python3. `tex_writer.py` is to run directly from within the specific 'report_writer' scripts, so there should be no need to generate it automatically. 

## Required files
All report writer scripts require a Config file and a requesite template.tex file, in addition to the specific additional files. See info below for what each specific report writer needs. 

## QC_report_writer.py
```
usage: QC_report_writer.py [-h] [-n] [-d DIRECTORY] [-v] Config_file

Minimum information needed in Config file: PROJECTID DATE MULTIPLEX BLANKS

positional arguments:
  Config_file           The config file with all additional information

options:
  -h, --help            show this help message and exit
  -n, --No_Tex          Select this if you do not want to produce a tex file
  -d DIRECTORY, --Directory DIRECTORY
                        The directory where the files being read are located
  -v, --Verbose         Display additional comments for debugging
  ```

### Dependencies
Python dependencies: pandas, numpy, openpyxl, odfpy. 

### Required files
- **Config_file**: 
  The Config file containing all additional required information. See below for required information in the Config file. 

### Config file 
The config file needs to contain the following information with the corresponding labels, separated by a colon. Comments beginning with '#' will be ignored. 
- **SAMPLEFILE**: The .xlsx file containing the sample information provided by the client. 
- **SUMMARYFILE**: The summary counts file, in .xlsx or .ods format. 
- **PROJECTID**: The ID of the project which will be included in the report. This will also be used in the resulting file names. 
- **DATE**: The date of the project to be included in the report. 
- **MULTIPLEX**: The plexicity level of the analysis. 
- **BLANKS**: The number of blanks included *per sample page*. So, if there are two sample pages and a total of four blanks, only include a blank number of 2. 

Example Config file: 
```
# Comments are ignored
PROJECTID: LOExxxx 
DATE: 10-02-2022 
SAMPLEFILE: sample.xlsx
SUMMARYFILE: summary.ods
MULTIPLEX: 94 
BLANKS: 1 
```

---
