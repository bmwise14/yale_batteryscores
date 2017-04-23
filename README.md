# ABOUT
If you use Qualtrics survey materials and collect the data through csv, this will tabulate raw scores of the following self-report 
scales for a large number of participants. This code was implemented using the pandas package. Below are the self-report scales:

* **BAPQ** – Broad Autism Phenotype Questionnaire
* **Barratt** – Barratt Impulsivity Scale
* **BISBAS** – Behavioral Inhibition Scale / Behavioral Activation Scale
* **DDQ** – Delay Discounting Task
* **DOSPERT** – Domain-Specific Risk-Taking Scale
* **NEO-FFI** – Neuroticism-Extroversion-Openness Five Factor Inventory
* **POMS** – Profile of Mood States
* **PSS** – Perceived Stress Scale
* **QIDS-SR16** – Quick Inventory of Depressive Symptoms-Self Report, 16 item
* **SNAITH** – Snaith-Hamilton Pleasure Scale
* **SHIPLEY** – Shipley Institute of Living Scale (Shipley Vocabulary) – Shipley 2
* **STAI** – State-Trait Anxiety Inventory for Adults
* **TCI** – Temperament and Character Inventory – Revised – 140 Scoring Key
* **TEPS** – Temporal Experience of Pleasure


**IMPORTANT:** When using these scoring templates, make sure self-report scale matches the one used. For more information, look inside the .py file
for each scale.




# COLUMN DICTIONARY
The column dictionary is an essential component to using the package. **reader.py** "reads" the headings in the column dictionary and 
uses those headings for score tabulation.

When looking at your qualtrics data, make sure you know what the headings for your scale are.


Under sampledataset_columndict_scriptToCallFunctions, look at the column_dictionary.csv
You will only need to fill in data for the following:

**COLUMN_NAME** - this is the name of the headings for your qualtrics data

**PreferNotToAnswerSelection** - this is the code you made for your prefer not to answer choice



# HOW TO USE
1. Clone or download the package and put it in a folder called batteryscores
2. Extract your raw data from Qualtrics
3. Make sure your Qualtrics headings match the headings you input in the column_dictionary
4. Create a blank python file or use skeletonscript.py as a template

```python
import pandas as pd
import sys

# import any script (or all scripts using *) to use from the batteryscores package
from batteryscores import *
```

After you have imported the necessary packages, create a variable for the reader:

```python
inputs = reader.reader(your_raw_data_path, column_dictionary_path)
```

The reader has 4 outputs. Make sure you create variables for those outputs. For example:

```python
# the dataframe that the functions will use to calculate self-report scores
df = inputs[0]
# the raw dataset you put in
raw_data_frame = inputs[1]
# the column dictionary you put in
question_dict = inputs[2]
# the value for your Prefer Not To Answer choices
nonresp = inputs[3]
```


Now that you have created those variables, you can call each self-report function. Each function is called a little differently, 
so please be sure to check what needs to be called. Here is an example of what you may call:
```python
# storagevariable= scriptname.functionname(dataframe, prefernotanswervalue) or
# storagevariable= scriptname.functionname(dataframe)
subjects = subjectid.subjectid(df)
bisbas = bisbas.bisbas(df, nonresp)
stai = stai.stai(df, nonresp)
barratt = barratt.barratt(df, nonresp)
bapq = bapq.bapq(df, nonresp)
neoffi = neoffi.neoffi(df, nonresp)
dospert = dospert.dospert(df, nonresp)
poms = poms.poms(df, nonresp)
pss = pss.pss(df)
shipley = shipley.shipley(df)
tci = tci.tci(df, nonresp)
teps = teps.teps(df)
snaith = snaith.snaith(df)
ddq = ddq.ddq(df)
qids = qids.qids(df, nonresp)
ncog = ncog.ncog(df, nonresp)
```

Finally, put the tabulated scores in an array variable, concatenate the results, and output those results to a csv file. 

For example:
```python
# put the variables you created above into the dataholder variable
dataholder = [subjects, neoffi]

# This concatenates the contents of the dataholder variable into one pandas dataframe
result = pd.concat(dataholder, axis=1)

# This outputs your data to a csv file. Type in the name of your outputfile
result.to_csv(file_name_for_outputted_scores)
```

Next, call the script in python, and you should be all set!
