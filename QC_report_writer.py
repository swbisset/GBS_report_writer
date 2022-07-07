# Need to install pandas, numpy
# dependencies: openpyxl, odfpy
import pandas as pd
import numpy as np
import argparse
import sys
import os


def count_pages(xlsx_file):
    count = 0
    try:
        df = pd.read_excel(xlsx_file, sheet_name='Sample Sheet 1')
    except ValueError:
        return count
    count += 1
    try:
        df = pd.read_excel(xlsx_file, sheet_name='Sample Sheet 2')
    except ValueError:
        return count
    count += 1
    try:
        df = pd.read_excel(xlsx_file, sheet_name='Sample Sheet 3')
    except ValueError:
        return count
    count += 1
    return count


def add_position(sheet_df):
    sheet_df['Position'] = sheet_df['Well']
    i = 0
    for x in sheet_df.index:
        if i >= 96:
            plate = 2
        else:
            plate = 1
        pos = '%s%s' % (plate, sheet_df.loc[x, 'Position'])
        sheet_df.loc[x, 'Position'] = pos
        i += 1
    return sheet_df


def read_text(text_file, has_comments=False):
    line_str = ""
    if has_comments:
        with open(text_file) as r:
            for line in r:
                if not line.startswith("#"):
                    line_str += line
    else:
        with open(text_file) as r:
            for line in r:
                line_str += line
    return line_str

help_str = "Minimum information needed in Config file: \nPROJECTID \nDATE \n MULTIPLEX \nBLANKS"

parser = argparse.ArgumentParser(description=help_str)
parser.add_argument('Sample_file', help = "The sample .xlsx file provided by the client")
parser.add_argument('Summary_file', help = "The summary .ods (or equivalent) file generated following sequencing")
parser.add_argument('Config_file', help = "The config file with all additional information")
parser.add_argument('-v', '--Verbose', help = "Display additional comments for debugging", action='store_true')

try:
    args = parser.parse_args()
except SystemExit:
    print("No input recognised. Please try again")
    sys.exit()

args = parser.parse_args()

sample_file = args.Sample_file      # This provides us with sample name if BELOWAV fails, and helps with BLANKSTAT
summary_file = args.Summary_file    # This provides us with TOTALREADS, AVREADCOUNT, COEFFVAR, BLANKSTAT and BELOWAV
config_file = args.Config_file      # This provides us with PROJECTID, DATE, MPLEX, NOPLATES (maybe), BLANKS

# Set commenting on if verbose has been selected
comment = False
if args.Verbose:
    comment = True

TOTALREAD, AVREADCOUNT, TENPERCENT, BLANKS, BELOWAV = 0, 0, 0, 0, 0
PROJECTID, DATE, MPLEX, BLANKSTAT = "", "", "", "PASS"
BELOWAV_list = []

# First, we need to check how many sample pages the provided 'Summary_file' has
pages = count_pages(sample_file)
if pages < 1:
    print("Cannot find sheet labelled 'Sample Sheet 1' in %s. Did you specify the correct file?" % sample_file)
    sys.exit()
else:
    print('%s sheets read in from %s' % (str(pages), sample_file))
# TODO: Come back to this and implement a way of dealing with having 2 or 3 xlsx sheets.

# Read in the sample .xlsx file. Only selecting 'Well' and 'Sample Name' columns.
sample_df = pd.read_excel(sample_file, skiprows=1, sheet_name='Sample Sheet 1', usecols=['Well', 'Sample Name'],
                          dtype={'Well': 'object', 'Sample Name': 'object'})

# Add an additional column, named 'Position' which contains the plate number & well info.
sample_df = add_position(sample_df)

# Read in the sample .ods file. Only selecting 'Sample' and 'Count' columns. Can get TOTALREAD immediately.
summary_df = pd.read_excel(summary_file, usecols=['Sample', 'Count'], dtype={'Sample': object, 'Count': 'float64'})
position = np.where(summary_df['Sample'] == 'total')[0]
TOTALREAD = summary_df.loc[position[0], 'Count']
if comment:
    print('Total number of reads: %s million' % (str(TOTALREAD)))

# Read in the Config file
config = read_text(config_file, True) # Telling this 'True' is just telling the function to ignore comments
config_split = config.split('\n')
for x in range(0, len(config_split)):
    if "PROJECTID" in config_split[x]:
        PROJECTID = config_split[x].split(": ")[1]
    if "DATE" in config_split[x]:
        DATE = config_split[x].split(": ")[1]
    if "MULTIPLEX" in config_split[x]:
        MPLEX = config_split[x].split(": ")[1]
    if "BLANKS" in config_split[x]:
        BLANKS = config_split[x].split(": ")[1]
if comment:
    print("Project ID:\t%s\nDate:\t%s\nMultiplex level:\t%s\nNumber of blanks:\t%s" % (PROJECTID, DATE, MPLEX, BLANKS))

# Read in AVREADCOUNT, COEFFVAR, TENPERCENT
summary_df2 = pd.read_excel(summary_file, usecols=[5, 6, 7, 8])
# pos1 = np.where(summary_df2['Unnamed: 5'] == 'Average')[0]
AVREADCOUNT = summary_df2.loc[np.where(summary_df2['Unnamed: 5'] == 'Average')[0][0], 'Unnamed: 6']
COEFFVAR = (summary_df2.loc[np.where(summary_df2['Unnamed: 5'] == 'CV')[0][0], 'Unnamed: 6']) * 100
TENPERCENT = summary_df2.loc[np.where(summary_df2['Unnamed: 7'] == '10% Average')[0][0], 'Unnamed: 8']
if comment:
    print('Average number of reads:\t%s million \nCoefficient of variance:\t%s \n10 percent of reads:\t%s' %
          (str(AVREADCOUNT), str(COEFFVAR), str(TENPERCENT)))

# Now we implement the blank check, and return which samples failed the 10% average mark
# First step is to get the ID of the blanks from the 'Sample file', and compare the counts in the 'Summary File'
blank_num = int(BLANKS)
blank_position = []
for x in range(0, blank_num):   # First we read through the xlsx file and get the sample positions of all blanks
    blank_str = "BLANK%s" % str(x+1)
    position = np.where(sample_df['Sample Name'] == blank_str)[0]
    blank_position.append(sample_df.loc[position[0], 'Position'])
for x in range(0, len(blank_position)):    # Next, check the blanks and make sure all are < the 10 percent cut-off
    position = np.where(summary_df['Sample'] == str(blank_position[x]))[0]
    if summary_df.loc[position[0], 'Count'] > TENPERCENT:
        print("Blank at position %s exceeded threshold" % str(blank_position[x]))
        BLANKSTAT = "FAIL"

# Now, we read through all the samples (from 0 < [multiplex level]) and check none have less than 10% average
# counts
for x in range(0, int(MPLEX)):
    if int(summary_df.loc[x, 'Count']) < TENPERCENT:
        # print("Sample %s has less than 10 percent the average number of reads" % (summary_df.loc[x, 'Sample']))
        BELOWAV += 1
        BELOWAV_list.append(sample_df.loc[np.where(sample_df['Position'] == str(summary_df.loc[x, 'Sample']))[0][0],
                                          'Sample Name'])
if comment:
    print("Number of samples to fail sequencing threshold: %s" % str(len(BELOWAV_list)))

# Now we tidy up the numbers before writing them out to the file
TOTALREAD = str(round((TOTALREAD / 1000000), 0)).split('.')[0]
AVREADCOUNT = str(round((AVREADCOUNT / 1000000), 1))
COEFFVAR = str(round(COEFFVAR, 0)).split('.')[0]

# Write information to temporary file
out_file = "%s_info.txt" % PROJECTID
with open(out_file, 'w') as w:
    w.write("%s : %s\n%s : %s\n%s : %s million\n%s : %s\n%s : %s million\n%s : %s\n%s : %s\n%s : %s" % ('PROJECTID',
                                    PROJECTID, 'DATE', DATE, 'TOTALREADS', TOTALREAD, 'MPLEX', MPLEX, 'AVREADCOUNT',
                                    AVREADCOUNT, 'COEFFVAR', COEFFVAR, 'BLANKSTAT', BLANKSTAT, 'BELOWAV', BELOWAV))

# TODO: Set tex_writer.py to be called from within this file.
output_tex = "%s_QC_report.tex" % PROJECTID
os.system("python3 tex_writer.py %s %s %s" % (out_file, 'QC_report_template.tex', output_tex))
