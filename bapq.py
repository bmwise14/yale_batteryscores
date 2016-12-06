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
# nonresval = the Prefer Not To Answer Choice on your Questionnaire


def bapq(input, nonresp):
    # BROAD AUTISM PHENOTYPE QUESTIONNAIRE

    # RESOURCES USED:
    """GSP Scales Notebook - Holmes Lab"""
    """http://link.springer.com/article/10.1007/s10803-006-0299-3"""
    """https://holmeslab-holmeslab.pbworks.com/w/file/84312403/BAPQ%20Scoring.pdf"""

    # SCORING:
    """
    1. Summary score for each of three subscales were computed by reverse scoring the appropriate items,
    averaging across the 12 items for each subscale and averaging across all 36 items to create a total score.
    All summary scores therefore have a range 1-6. (Hurley et al., 2007).

    2. Questions that should be reverse scored are reverse scored.

    3. Participant who chooses Prefer Not To Answer selection is not discarded, but is not counted toward the average on subscales or final score (Avram).

    4. Any Question That is left completely blank is not discarded, but not counted toward the average on subscales or final score (Avram).
    """
    try:
        # VERY RARELY - RARELY - OCCASIONALLY - SOMEWHAT OFTEN - OFTEN - VERY OFTEN - PREFER NOT TO ANSWER
        #     1           2           3              4             5          6             YOUR #
        # ------------------------------------------------------------------------------
        # THESE KEYS ARE READ BY THE COLUMN DICTIONARY -> Question_Name
        bapq_aloof_keys = ['bapq_5', 'bapq_18', 'bapq_27', 'bapq_31']
        bapq_aloof_rev_keys = ['bapq_1', 'bapq_9', 'bapq_12', 'bapq_16', 'bapq_23', 'bapq_25', 'bapq_28', 'bapq_36']
        bapq_rigid_keys = ['bapq_6', 'bapq_8', 'bapq_13', 'bapq_22', 'bapq_24', 'bapq_26', 'bapq_33', 'bapq_35']
        bapq_rigid_rev_keys = ['bapq_3', 'bapq_15', 'bapq_19', 'bapq_30']
        bapq_prag_keys = ['bapq_2', 'bapq_4', 'bapq_10', 'bapq_11', 'bapq_14', 'bapq_17', 'bapq_20', 'bapq_29',
                          'bapq_32']
        bapq_prag_rev_keys = ['bapq_7', 'bapq_21', 'bapq_34']


        # ------------------------------------------------------------------------------
        # ALOOF SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        aloof_forward = input[bapq_aloof_keys].apply(pd.to_numeric, args=('coerce',))
        aloof_forward_leftblank = aloof_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        aloof_forward_prefernotanswer = aloof_forward[aloof_forward[bapq_aloof_keys] == nonresp['bapq']].count(axis=1)

        # sum all the forward scores
        aloof_forward_score = aloof_forward[(aloof_forward[bapq_aloof_keys] >= 1) &
                                            (aloof_forward[bapq_aloof_keys] <= 6)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        aloof_rev = input[bapq_aloof_rev_keys].apply(pd.to_numeric, args=('coerce',))

        # sum the number of reverse questions left blank or preferred not to answer
        aloof_reverse_leftblank = aloof_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        aloof_reverse_prefernotanswer = aloof_rev[aloof_rev[bapq_aloof_rev_keys] == nonresp['bapq']].count(axis=1)

        # sum all the reverse scores
        aloof_rev_score = aloof_rev[aloof_rev[bapq_aloof_rev_keys] <= 6].rsub(7).sum(axis=1, skipna=True)

        # Total SCORE
        total_aloof_score = (aloof_forward_score + aloof_rev_score)/12

        # TOTAL ANSWERS LEFT BLANK
        total_aloof_leftblank = aloof_forward_leftblank + aloof_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_aloof_prefernotanswer = aloof_forward_prefernotanswer + aloof_reverse_prefernotanswer

        aloofall = pd.DataFrame(
            {'BAPQ_Aloof_Score': total_aloof_score, 'BAPQ_Aloof_Prefer_Not_to_Answer': total_aloof_prefernotanswer,
             'BAPQ_Aloof_Left_Blank': total_aloof_leftblank})



        # ------------------------------------------------------------------------------
        # RIGID SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        rigid_forward = input[bapq_rigid_keys].apply(pd.to_numeric, args=('coerce',))
        rigid_forward_leftblank = rigid_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        rigid_forward_prefernotanswer = rigid_forward[rigid_forward[bapq_rigid_keys] == nonresp['bapq']].count(axis=1)

        # sum all the forward scores
        rigid_forward_score = rigid_forward[(rigid_forward[bapq_rigid_keys] >= 1) &
                                            (rigid_forward[bapq_rigid_keys] <= 6)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        rigid_rev = input[bapq_rigid_rev_keys].apply(pd.to_numeric, args=('coerce',))

        # sum the number of reverse questions left blank or preferred not to answer
        rigid_reverse_leftblank = rigid_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        rigid_reverse_prefernotanswer = rigid_rev[rigid_rev[bapq_rigid_rev_keys] == nonresp['bapq']].count(axis=1)

        # sum all the reverse scores
        rigid_rev_score = rigid_rev[rigid_rev[bapq_rigid_rev_keys] <= 6].rsub(7).sum(axis=1, skipna=True)

        # Total SCORE
        total_rigid_score = (rigid_forward_score + rigid_rev_score)/12

        # TOTAL ANSWERS LEFT BLANK
        total_rigid_leftblank = rigid_forward_leftblank + rigid_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_rigid_prefernotanswer = rigid_forward_prefernotanswer + rigid_reverse_prefernotanswer

        rigidall = pd.DataFrame(
            {'BAPQ_Rigid_Score': total_rigid_score, 'BAPQ_Rigid_Left_Blank': total_rigid_leftblank,
             'BAPQ_Rigid_Prefer_Not_to_Answer': total_rigid_prefernotanswer})



        # ------------------------------------------------------------------------------
        # PRAGMATIC LANGUAGE SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        prag_forward = input[bapq_prag_keys].apply(pd.to_numeric, args=('coerce',))
        prag_forward_leftblank = prag_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        prag_forward_prefernotanswer = prag_forward[prag_forward[bapq_prag_keys] == nonresp['bapq']].count(axis=1)

        # sum all the forward scores
        prag_forward_score = prag_forward[(prag_forward[bapq_prag_keys] >= 1) &
                                          (prag_forward[bapq_prag_keys] <= 6)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        prag_rev = input[bapq_prag_rev_keys].apply(pd.to_numeric, args=('coerce',))

        # sum the number of reverse questions left blank or preferred not to answer
        prag_reverse_leftblank = prag_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        prag_reverse_prefernotanswer = prag_rev[prag_rev[bapq_prag_rev_keys] == nonresp['bapq']].count(axis=1)

        # sum all the reverse scores
        prag_rev_score = prag_rev[prag_rev[bapq_prag_rev_keys] <= 6].rsub(7).sum(axis=1, skipna=True)

        # Total SCORE
        total_prag_score = (prag_forward_score + prag_rev_score)/12

        # TOTAL ANSWERS LEFT BLANK
        total_prag_leftblank = prag_forward_leftblank + prag_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_prag_prefernotanswer = prag_forward_prefernotanswer + prag_reverse_prefernotanswer

        pragall = pd.DataFrame(
            {'BAPQ_Pragmatic_Language_Score': total_prag_score, 'BAPQ_Pragmatic_Left_Blank': total_prag_leftblank,
             'BAPQ_Pragmatic_Prefer_Not_to_Answer': total_prag_prefernotanswer})




        # ------------------------------------------------------------------------------
        # TOTAL SCORE

        # Add the subscale scores, then divide by the total number of subscales
        total_score = (total_aloof_score + total_rigid_score + total_prag_score) / 3

        # Add the total number of questions left blank
        total_leftblank = total_aloof_leftblank + total_rigid_leftblank + total_prag_leftblank

        # Add the total number of selections that were Prefer Not to Answer
        total_prefernottoanswer = total_aloof_prefernotanswer + total_rigid_prefernotanswer + total_prag_prefernotanswer

        totalscore = pd.DataFrame(
            {'Total_BAPQ_Score': total_score, 'Total_BAPQ_Left_Blank': total_leftblank,
             'Total_BAPQ_Prefer_Not_To_Answer': total_prefernottoanswer})


        # ------------------------------------------------------------------------------
        # Put the scores into one frame
        frames = [aloofall, rigidall, pragall, totalscore]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print("We could not find the BAPQ headers in your dataset. Please look at the bapq function in this package and put in the correct keys.")
    except TypeError:
        print("You need (1) the dataframe and (2) a numeric BAPQ 'Prefer Not To Answer' choice (or stored variable) in your function arguments.")
