#!/usr/bin/python


import pandas as pd
import sys

# import any script (or all scripts using *) to use from the batteryscores package
from batteryscores import *


"""
(A) WAYS TO USE THIS TEMPLATE SCRIPT:
1. Import any or all scripts in the package to use the functions you want to use. All functions are listed
in the __init__.py script.

2. Look at each function you are going to use in this package. See what arguments are needed to call the function.
Next, download your data and input the question headers into the column dictionary that is provided. See (B).

3. You may call our reader function or not. PLEASE CHECK THE READER FUNCTION TO SEE IF IT WORKS FOR YOUR NEEDS.

4. If you use our reader, use the template below to concatenate your results.

5. If you use our template to prepare calling the script, to actually call the skeleton script in the terminal, do this:
    - python skeletonscript.py intputfile(your data file pathname) datadicfile(the column dictionary pathname) outputfile(whatever you want to call it)
"""


"""
(B) HOW TO EXPORT YOUR QUALTRICS DATA AND PUT INTO THE COLUMN DICTIONARY IF USING THE BATTERYSCORES READER FUNCTION:
1. Export your Qualtrics Data as numeric values!!!!

2. When copying your question headers to column dictionary,
copy and paste the VERY TOP ROW of your Qualtrics data to the COLUMN NAME column.

3. Make sure everything is copied and pasted correctly. Also, change your PREFER NOT TO ANSWER CHOICE to the value
that corresponds to your specific battery.

4. If there is not a Prefer Not to Answer Choice in your battery, but the battery function calls for one,
just make a value up like 9999. It won't be counted.
"""

# ------------------------------------------------------------------------------
"""IMPLEMENTING READER MODULE"""
# this variable holds the things you are passing in
inputs = reader.reader(sys.argv[1], sys.argv[2])

# BELOW IS WHAT THE BATTERYSCORES READER RETURNS IF YOU REFERENCE THE INPUTS VARIABLE

# the dataframe that the functions will use to calculate self-report scores
df = inputs[0]
# the raw dataset you put in
raw_data_frame = inputs[1]
# the column dictionary you put in
question_dict = inputs[2]
# the value for your Prefer Not To Answer choices
nonresp = inputs[3]

# ------------------------------------------------------------------------------
# storagevariable= scriptname.functionname(dataframe, prefernotanswervalue) or
# storagevariable= scriptname.functionname(dataframe)
subjects = subjectid.subjectid(df)
bisbas = bisbas.bisbas(df, nonresp)
stai = stai.stai(df, nonresp)
tci = tci.tci(df, nonresp)
neoffi = neoffi.neoffi(df, nonresp)
shipley = shipley.shipley(df)
pss = pss.pss(df)
barratt = barratt.barratt(df, nonresp)
ddq = ddq.ddq(df)

# put the variables you created above into the dataholder variable
dataholder = [subjects, neoffi]

# This concatenates the contents of the dataholder variable into one pandas dataframe
result = pd.concat(dataholder, axis=1)

# This outputs your data to a csv file. Type in the name of your outputfile in the terminal command line - system argument 4.
try:
    result.to_csv(sys.argv[3])
except IndexError:
    print "IndexError: Type an output file name (system argument 4) when calling the skeletonscript in the terminal."