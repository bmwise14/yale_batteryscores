#!/usr/bin/python

"""
Battery Scores Package for Processing Qualtrics CSV Files

@author: Bradley Wise
@email: bradley.wise@yale.edu
@version: 1.1
@date: 2016.12.06
"""

import pandas as pd

# input = the data you are using with with the keys listed below as headers

def subjectid(input):
    try:
        subj_id = pd.DataFrame({'SUBJ_ID': input['SUBJ_ID']})
        return subj_id
    except KeyError:
        print("We could not find the header 'SUBJ_ID' in your dataset. Please try again.")