#!/usr/bin/python

"""
Battery Scores Package for Processing Qualtrics CSV Files

@author: Bradley Wise
@email: bradley.wise@yale.edu
@version: 1.1
@date: 2016.12.06
"""

import pandas as pd
import sys


"""
1. This reader function converts the .csv datafile into a pandas dataframe that subsequent functions
in this package canuse.

2. You do not need to use this reader as long as you use the PANDAS package and can reference the keys outlined in
each self-report function in your dataset in some way.

3. Please check the skeleton script for further instructions.
"""

def reader(datafilepath, columndictionary):
    # Read your raw data and the column dictionary
    try:
        raw_data_frame = pd.read_csv(datafilepath)
        question_dict = pd.read_csv(columndictionary)
    except IOError:
        print "IO ERROR: one of the pathnames for your column dictionary or datafile does not exist. Please type in a valid pathname for both."


    # Turn the raw data frame into a pandas dataframe
    # and replace your raw data column names with the question names
    df = pd.DataFrame(raw_data_frame, index=range(1, len(raw_data_frame)),
                                columns=question_dict['COLUMN_NAME'])
    df.columns = question_dict['QUESTION_NAME']


    # Zip Prefer Not To Answer Choices into a dictionary with the Self-Report Question Names so that functions can reference them
    scale_list = [item.split('_')[0] for item in question_dict['QUESTION_NAME'] if item.split('_')[0] != 'SUBJ']
    nonresvals = [question_dict['PreferNotToAnswerSelection'][idx] for idx, item in enumerate(question_dict['QUESTION_NAME']) if
                  item.split('_')[0] != 'SUBJ']
    nonresponse = dict(zip(scale_list, nonresvals))

    return df, raw_data_frame, question_dict, nonresponse