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


def snaith(input):
    # SNAITH-HAMILTON PLEASURE SCALE

    # RESOURCES USED:
    """(1) http://bjp.rcpsych.org/content/bjprcpsych/167/1/99.full.pdf?origin=publication_detail"""
    """(2) http://www.sciencedirect.com/science/article/pii/S0165032706003582"""

    # SCORING:
    """
    1. In (1):
    "...it was decided to adopt the simpler method, used in the General Health Questionnaire (GHQ), in which either of the
    'Disagree' responses scores 1 point and either of the 'Agree' responses scores 0 points. Thus, teh score range is 0-14."

    2. (1) Paper - STRONGLY DISAGREE    DISAGREE    AGREE     DEFINITELY AGREE
                            1               1          0            0

    3. In (2):
    "The 14-item Snaith-Hamilton Pleasure Scale was used to measure the present state of anhedonia. The SHAPS items are displayed
    in Table 1. Each of the items has a set of four response categories, that is Definitely Agree (=1), Agree (= 2), Disagree (= 3),
    and Definitely Disagree (= 4). A higher total score indicates higher levels of state anhedonia. The SHAPS was translated
    into the Dutch language by the first authors of this manuscript. Snaith et al. propose to recode the four response categories into dichotomous
    categories, taht is, agree and disagree (score 0 and 1). However, given the limited set of items, it seems more desirable
    for research purposes to keep the original four response categories. The original scoring was only used to investigate the proportion
    of participants that could be diagnosed as anhedonic (original SHAPS score > 2). For all other analyses a total score was
    computed by summing scores across four response categories, yielding more dispersion of the data. Higher scores indicate
    less hedonic tone, and hence more anhedonic symptoms."

    4. (2) indicates a reverse scoring system.
    5. (2) Paper - STRONGLY DISAGREE    DISAGREE    AGREE     DEFINITELY AGREE
                            1               2         3             4

    6. I reversed the scores and summed their results together to create an overall Pleasure score for each participant.
    A higher score indicates more anhedonic symptoms. A lower indicates more hedonic tone.
    """

    try:
        # STRONGLY DISAGREE    DISAGREE     NEUTRAL        AGREE     DEFINITELY AGREE
        #     1                  2            3              4             5

        # ------------------------------------------------------------------------------
        # These are are the different headers and their corresponding questions
        # ALL SNAITH SCORES ARE REVERSE CODED
        snaith_headers_rev = ['snaith_1', 'snaith_2', 'snaith_3', 'snaith_4', 'snaith_5', 'snaith_6', 'snaith_7', 'snaith_8',
                          'snaith_9', 'snaith_10', 'snaith_11', 'snaith_12', 'snaith_13', 'snaith_14']


        # ------------------------------------------------------------------------------
        # SNAITH SCORE - ALL REVERSE, NO FORWARD

        # change the numbers in drive headers to numeric floats
        snaith = input[snaith_headers_rev].apply(pd.to_numeric, args=('coerce',))

        # These count the number of drive questions left blank or answered as 5 and sums them up as drive_unanswered
        snaith_leftblank = snaith.apply(lambda x: sum(x.isnull().values), axis=1)

        # reverse the scores by subtracting 6 from the raw data. Score of each item ranges from 1 to 5.
        snaith_answers_reversed = snaith[snaith[snaith_headers_rev] <= 5].rsub(6)
        # sum the reversed scores together to get the drive score
        snaith_score = snaith_answers_reversed.sum(axis=1, skipna = True)

        snaithall = pd.DataFrame({'Snaith_Score' : snaith_score, 'Snaith_Left_Blank': snaith_leftblank})


        # ------------------------------------------------------------------------------
        # Put the scores into one frame
        frames = [snaithall]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print("We could not find the SNAITH headers in your dataset. Please look at the snaith function in this package and put in the correct keys.")