#!/usr/bin/python

import pandas as pd


# input = the data you are using with with the keys listed below as headers
# nonresval = the Prefer Not To Answer Choice on your Questionnaire


def qids(input, nonresp):

    # QUICK INVENTORY OF DEPRESSIVE SYMPTOMS - SELF RATED (QIDS-SR16)

    # RESOURCES USED:
    """http://www.ids-qids.org/index2.html#SCORING"""
    """http://www.sciencedirect.com/science/article/pii/S0006322302018668?np=y"""

    # SCORING:
    """

    """
    # NONE    MILD    MODERATE    SEVERE    PREFER NOT TO ANSWER
    #  0       1         2          3             YOUR #

    qids_keys = ['QIDS_1', 'QIDS_2', 'QIDS_3', 'QIDS_4', 'QIDS_5', 'QIDS_6', 'QIDS_7', 'QIDS_8', 'QIDS_9', 'QIDS_10',
                 'QIDS_11', 'QIDS_12', 'QIDS_13', 'QIDS_14', 'QIDS_15', 'QIDS_16']


    sleep_keys = ['QIDS_1', 'QIDS_2', 'QIDS_3', 'QIDS_4']
    weight_keys = ['QIDS_6', 'QIDS_7', 'QIDS_8', 'QIDS_9']
    psychomotor_keys = ['QIDS_15', 'QIDS_16']
    mood_key = ['QIDS_5']
    concentration_key = ['QIDS_10']
    self_criticism_key = ['QIDS_11']
    suicidal_key = ['QIDS_12']
    interest_key = ['QIDS_13']
    energy_key = ['QIDS_14']

    # ------------------------------------------------------------------------------
    # For sleep, weight, and psychomotor, just gets the highest score from each domain
    sleep = input[sleep_keys].apply(pd.to_numeric, args=('coerce',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                   value=[0, 1, 2, 3])
    sleepvalue = sleep[(sleep[sleep_keys] >= 0) & (sleep[sleep_keys] <= 3)].max(axis=1, skipna=True)

    # ---------------------------
    weight = input[weight_keys].apply(pd.to_numeric, args=('coerce',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                   value=[0, 1, 2, 3])
    weightvalue = weight[(weight[weight_keys] >= 0) & (weight[weight_keys] <= 3)].max(axis=1, skipna=True)

    # ---------------------------
    psychomotor = input[psychomotor_keys].apply(pd.to_numeric, args=('coerce',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                   value=[0, 1, 2, 3])
    psychvalue = psychomotor[(psychomotor[psychomotor_keys] >= 0) & (psychomotor[psychomotor_keys] <= 3)].max(axis=1, skipna=True)




    # ------------------------------------------------------------------------------
    # replaces the qualtrics value with the scoring value for each domain
    mood = input[mood_key].apply(pd.to_numeric, args=('coerce',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                   value=[0, 1, 2, 3])
    moodscore = mood[(mood[mood_key] >= 0) & (mood[mood_key] <= 3)].sum(axis=1, skipna=True)

    # ---------------------------
    concentration = input[concentration_key].apply(pd.to_numeric, args=('coerce',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                   value=[0, 1, 2, 3])
    concscore = concentration[(concentration[concentration_key] >= 0) & (concentration[concentration_key] <= 3)].sum(axis=1, skipna=True)

    # ---------------------------
    selfcrit = input[self_criticism_key].apply(pd.to_numeric, args=('coerce',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                   value=[0, 1, 2, 3])
    critscore = selfcrit[(selfcrit[self_criticism_key] >= 0) & (selfcrit[self_criticism_key] <= 3)].sum(axis=1,skipna=True)

    # ---------------------------
    suicidal = input[suicidal_key].apply(pd.to_numeric, args=('coerce',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                   value=[0, 1, 2, 3])

    suicidescore = suicidal[(suicidal[suicidal_key] >= 0) & (suicidal[suicidal_key] <= 3)].sum(axis=1, skipna=True)

    # ---------------------------
    interest = input[interest_key].apply(pd.to_numeric, args=('coerce',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                   value=[0, 1, 2, 3])
    interestscore = interest[(interest[interest_key] >= 0) & (interest[interest_key] <= 3)].sum(axis=1, skipna=True)

    # ---------------------------
    energy = input[energy_key].apply(pd.to_numeric, args=('coerce',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                   value=[0, 1, 2, 3])
    energyscore = energy[(energy[energy_key] >= 0) & (energy[energy_key] <= 3)].sum(axis=1, skipna=True)



    # ------------------------------------------------------------------------------
    # SUMS THE SCORES UP!
    qids_score = sleepvalue + weightvalue + psychvalue + moodscore + concscore + critscore + suicidescore + interestscore + energyscore


    # COUNTS UP SCORES LEFT BLANK OR PREFER NOT TO ANSWER
    qids = input[qids_keys].apply(pd.to_numeric, args=('coerce',), axis=1)
    qids_leftblank = qids.apply(lambda x: sum(x.isnull().values), axis=1)
    qids_prefernotanswer = qids[qids[qids_keys] == nonresp['QIDS']].count(axis=1)


    qidsall = pd.DataFrame(
        {'QIDS_Score': qids_score, 'QIDS_Left_Blank': qids_leftblank,
         'QIDS_Prefer_Not_to_Answer': qids_prefernotanswer})


    # ------------------------------------------------------------------------------
    frames = [qidsall]
    result = pd.concat(frames, axis=1)
    return result