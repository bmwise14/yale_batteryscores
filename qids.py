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


# input = the data you are using with with the keys listed below as headers
# nonresval = the Prefer Not To Answer Choice on your Questionnaire


def qids(input, nonresp):

    # QUICK INVENTORY OF DEPRESSIVE SYMPTOMS - SELF RATED (QIDS-SR16)

    # RESOURCES USED:
    """http://www.ids-qids.org/index2.html#SCORING"""
    """http://www.sciencedirect.com/science/article/pii/S0006322302018668?np=y"""

    # SCORING:
    """
    1. The QIDS-SR16 total scores range from 0 to 27.
    The total score is obtained by adding the scores for each of the nine symptom domains of the DSM-IV MDD criteria:
    depressed mood, loss of interest or pleasure, concentration/decision making, self-outlook, suicidal ideation,
    energy/fatigability, sleep, weight/appetite change, and psychomotor changes (Rush et al. 2003).
    Sixteen items are used to rate the nine criterion domains of major depression: 4 items are used to rate sleep disturbance
    (early, middle, and late insomnia plus hypersomnia); 2 items are used to rate psychomotor disturbance (agitation and retardation);
    4 items are used to rate appetite/weight disturbance (appetite increase or decrease and weight increase or decrease).
    Only one item is used to rate the remaining 6 domains (depressed mood, decreased interest, decreased energy,
    worthlessness/guilt, concentration/decision making, and suicidal ideation). Each item is rated 0-3.
    For symptom domains that require more than one item, the highest score of the item relevant for each domain is taken.
    For example, if early insomnia is 0, middle insomnia is 1, late insomnia is 3, and hypersomnia is 0,
    the sleep disturbance domain is rated 3. The total score ranges from 0-27.

    2. How to handle prefer not to answer is not explicitly mentioned in the primary resources above, so
    if any subscale value is left blank or PFN among the 6 1-item domains and the 3 multiple item domains,
    then that value will be discarded.

    3. If the score is below a minimum value range or above a maximum value range for the subscale, it will be discarded.
                                                        Min     Max
                                    QIDS_TotalScore     0       27
    """
    # NONE    MILD    MODERATE    SEVERE    PREFER NOT TO ANSWER
    #  0       1         2          3             YOUR #
    try:
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
        # COUNTS UP SCORES LEFT BLANK OR PREFER NOT TO ANSWER
        qids = input[qids_keys].apply(pd.to_numeric, args=('raise',), axis=1)

        # Are there any values that don't fit in the value parameters
        qids_nofit = qids[(qids[qids_keys] != nonresp['QIDS']) &
                                  (qids[qids_keys] > 4) |
                                  (qids[qids_keys] < 1)].count(axis=1)

        qids_leftblank = qids.apply(lambda x: sum(x.isnull().values), axis=1)
        qids_prefernotanswer = qids[qids[qids_keys] == nonresp['QIDS']].count(axis=1)

        # ------------------------------------------------------------------------------
        # Count the number of values that do not fit parameter values
        nofit = qids_nofit

        # If there are any values that do not fit parameters, exit the code and make client find the values that did not work
        for x in nofit:
            if x >= 1:
                sys.exit("We found values that don't match parameter values for calculation in your QIDS dataset. "
                         "Please make sure your values range from 1-4 (see qids script) and have only ONE prefer not to answer value.")
        # ------------------------------------------------------------------------------


        # For sleep, weight, and psychomotor, just gets the MAX SINGLE SCORE from each domain
        sleep = input[sleep_keys].apply(pd.to_numeric, args=('raise',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                       value=[0, 1, 2, 3])

        sleepvalue = sleep[(sleep[sleep_keys] >= 0) & (sleep[sleep_keys] <= 3)].max(axis=1, skipna=True)

        # ---------------------------
        weight = input[weight_keys].apply(pd.to_numeric, args=('raise',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                       value=[0, 1, 2, 3])

        weightvalue = weight[(weight[weight_keys] >= 0) & (weight[weight_keys] <= 3)].max(axis=1, skipna=True)

        # ---------------------------
        psychomotor = input[psychomotor_keys].apply(pd.to_numeric, args=('raise',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                       value=[0, 1, 2, 3])

        psychvalue = psychomotor[(psychomotor[psychomotor_keys] >= 0) & (psychomotor[psychomotor_keys] <= 3)].max(axis=1, skipna=True)

        # ------------------------------------------------------------------------------
        # replaces the qualtrics value with the scoring value for each domain
        mood = input[mood_key].apply(pd.to_numeric, args=('raise',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                       value=[0, 1, 2, 3])

        moodscore = mood[(mood[mood_key] >= 0) & (mood[mood_key] <= 3)].sum(axis=1, skipna=True)

        # ---------------------------
        concentration = input[concentration_key].apply(pd.to_numeric, args=('raise',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                       value=[0, 1, 2, 3])

        concscore = concentration[(concentration[concentration_key] >= 0) & (concentration[concentration_key] <= 3)].sum(axis=1, skipna=True)

        # ---------------------------
        selfcrit = input[self_criticism_key].apply(pd.to_numeric, args=('raise',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                       value=[0, 1, 2, 3])

        critscore = selfcrit[(selfcrit[self_criticism_key] >= 0) & (selfcrit[self_criticism_key] <= 3)].sum(axis=1,skipna=True)

        # ---------------------------
        suicidal = input[suicidal_key].apply(pd.to_numeric, args=('raise',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                       value=[0, 1, 2, 3])

        suicidescore = suicidal[(suicidal[suicidal_key] >= 0) & (suicidal[suicidal_key] <= 3)].sum(axis=1, skipna=True)

        # ---------------------------
        interest = input[interest_key].apply(pd.to_numeric, args=('raise',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                       value=[0, 1, 2, 3])

        interestscore = interest[(interest[interest_key] >= 0) & (interest[interest_key] <= 3)].sum(axis=1, skipna=True)

        # ---------------------------
        energy = input[energy_key].apply(pd.to_numeric, args=('raise',), axis=1).replace(to_replace=[1, 2, 3, 4],
                                                                                       value=[0, 1, 2, 3])

        energyscore = energy[(energy[energy_key] >= 0) & (energy[energy_key] <= 3)].sum(axis=1, skipna=True)

        # ------------------------------------------------------------------------------
        # SUMS THE SCORES UP!
        qids_score = sleepvalue + weightvalue + psychvalue + moodscore + concscore + critscore + suicidescore + interestscore + energyscore

        qidsall = pd.DataFrame(
            {'QIDS_Score': qids_score, 'QIDS_Left_Blank': qids_leftblank,
             'QIDS_Prefer_Not_to_Answer': qids_prefernotanswer})


        # ------------------------------------------------------------------------------
        frames = [qidsall]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print "We could not find the QIDS headers in your dataset. Please look at the qids function in this package and put in the correct keys."
    except ValueError:
        print("We found strings in your QIDS dataset. Please make sure there are no strings/letters in your input. Otherwise, we can't do our thang.")