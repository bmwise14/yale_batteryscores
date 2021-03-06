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

def stai(input, nonresp):
    # STATE-TRAIT ANXIETY INVENTORY FOR ADULTS

    # RESOURCES USED:
    """GSP Scales - Holmes Lab"""
    """http://www.mindgarden.com/145-state-trait-anxiety-inventory-for-adults"""

    # SCORING:
    """
    1. Score of each item typically ranges from 1-4 with a prefer not to answer choice.

    2. Scores are the sum of each subscale. Questions that should be reverse scored are reverse scored.

    3. How to handle missing values is not explicitly mentioned in the primary resources above, so
    if any value is left blank or prefer not to answer, those missing values will be replaced with the average
    score on that particular subscale and then added to the final subscore total (Avram). (see rdoc.py)

    4. If the score is below a minimum value range or above a maximum value range for the subscale, it will be discarded.
                                                        Min     Max
                                        STAI_tAnxiety   20      80
                                        STAI_sAnxiety   20      80
    """

    try:
        # NOT AT ALL - SOMEWHAT - MODERATELY SO - VERY MUCH SO - PREFER NOT TO ANSWER
        #     1            2           3               4               YOUR VALUE
        # ------------------------------------------------------------------------------
        stai_trait_keys = ['STAI_3', 'STAI_4', 'STAI_6', 'STAI_7', 'STAI_9', 'STAI_12', 'STAI_13', 'STAI_14', 'STAI_17',
                           'STAI_18']
        stai_trait_rev_keys = ['STAI_1', 'STAI_2', 'STAI_5', 'STAI_8', 'STAI_10', 'STAI_11', 'STAI_15', 'STAI_16',
                               'STAI_19', 'STAI_20']
        stai_state_keys = ['STAI_22', 'STAI_24', 'STAI_25', 'STAI_28', 'STAI_29', 'STAI_31', 'STAI_32', 'STAI_35',
                           'STAI_37','STAI_38', 'STAI_40']
        stai_state_rev_keys = ['STAI_21', 'STAI_23', 'STAI_26', 'STAI_27', 'STAI_30', 'STAI_33', 'STAI_34', 'STAI_36',
                               'STAI_39']

        # ------------------------------------------------------------------------------
        # STAI TRAIT SCORE

        # change the numbers in forward STAI Trait headers to numeric floats
        stai_trait_forward = input[stai_trait_keys].apply(pd.to_numeric, args=('raise',))

        # Are there any values that don't fit in the value parameters
        stai_trait_forward_nofit = stai_trait_forward[(stai_trait_forward[stai_trait_keys] != nonresp['STAI']) &
                                  (stai_trait_forward[stai_trait_keys] > 4) |
                                  (stai_trait_forward[stai_trait_keys] < 1)].count(axis=1)

        # sum the number of forward questions left blank or preferred not to answer
        stai_trait_forward_leftblank = stai_trait_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        stai_trait_forward_prefernotanswer = stai_trait_forward[stai_trait_forward[stai_trait_keys] == nonresp['STAI']].count(axis=1)
        stai_trait_forward_unanswered = stai_trait_forward_leftblank + stai_trait_forward_prefernotanswer

        # sum all the forward scores
        stai_trait_forward_score = stai_trait_forward[(stai_trait_forward[stai_trait_keys] >= 1) &
                                                      (stai_trait_forward[stai_trait_keys] <= 4)].sum(axis=1)

        # change the numbers in reverse STAI Trait headers to numeric floats
        stai_trait_rev = input[stai_trait_rev_keys].apply(pd.to_numeric, args=('raise',))

        # Are there any values that don't fit in the value parameters
        stai_trait_rev_nofit = stai_trait_rev[(stai_trait_rev[stai_trait_rev_keys] != nonresp['STAI']) &
                                  (stai_trait_rev[stai_trait_rev_keys] > 4) |
                                  (stai_trait_rev[stai_trait_rev_keys] < 1)].count(axis=1)

        # sum the number of reverse questions left blank or preferred not to answer
        stai_trait_reverse_leftblank = stai_trait_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        stai_trait_reverse_prefernotanswer = stai_trait_rev[stai_trait_rev[stai_trait_rev_keys] == nonresp['STAI']].count(axis=1)
        stai_trait_reverse_unanswered = stai_trait_reverse_leftblank + stai_trait_reverse_prefernotanswer

        # sum all the reverse scores
        stai_trait_reverse_score = stai_trait_rev[stai_trait_rev[stai_trait_rev_keys] <= 4].rsub(5).sum(axis=1, skipna=True)

        # Total STAI TRAIT SCORE
        total_STAI_Trait_score = stai_trait_forward_score + stai_trait_reverse_score
        # TOTAL STAI TRAIT ANSWERS UNANSWERED
        total_STAI_Trait_unanswered = stai_trait_forward_unanswered + stai_trait_reverse_unanswered


        # TOTAL ANSWERS LEFT BLANK
        total_stai_trait_leftblank = stai_trait_forward_leftblank + stai_trait_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_stai_trait_prefernotanswer = stai_trait_forward_prefernotanswer + stai_trait_reverse_prefernotanswer


        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original drive score.
        total_STAI_Trait_score = total_STAI_Trait_score + (total_STAI_Trait_unanswered * total_STAI_Trait_score /

                                                           (len(stai_trait_keys)+len(stai_trait_rev_keys) - (total_STAI_Trait_unanswered)))



        staitraitall = pd.DataFrame(
            {'STAI_Trait_Score': total_STAI_Trait_score, 'STAI_Trait_Left_Blank': total_stai_trait_leftblank,
             'STAI_Trait_Prefer_Not_to_Answer': total_stai_trait_prefernotanswer})


        # ------------------------------------------------------------------------------
        # STAI STATE SCORE

        # change the numbers in forward STAI STATE headers to numeric floats
        stai_state_forward = input[stai_state_keys].apply(pd.to_numeric, args=('raise',))

        # Are there any values that don't fit in the value parameters
        stai_state_forward_nofit = stai_state_forward[(stai_state_forward[stai_state_keys] != nonresp['STAI']) &
                                  (stai_state_forward[stai_state_keys] > 4) |
                                  (stai_state_forward[stai_state_keys] < 1)].count(axis=1)

        # sum the number of forward questions left blank or preferred not to answer
        stai_state_forward_leftblank = stai_state_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        stai_state_forward_prefernotanswer = stai_state_forward[stai_state_forward[stai_state_keys] == nonresp['STAI']].count(axis=1)
        stai_state_forward_unanswered = stai_state_forward_leftblank + stai_state_forward_prefernotanswer

        # sum all the forward scores
        stai_state_forward_score = stai_state_forward[(stai_state_forward[stai_state_keys] >= 1) &
                                                      (stai_state_forward[stai_state_keys] <= 4)].sum(axis=1)

        # change the numbers in forward STAI STATE headers to numeric floats
        stai_state_rev = input[stai_state_rev_keys].apply(pd.to_numeric, args=('raise',))

        # Are there any values that don't fit in the value parameters
        stai_state_rev_nofit = stai_state_rev[(stai_state_rev[stai_state_rev_keys] != nonresp['STAI']) &
                                  (stai_state_rev[stai_state_rev_keys] > 4) |
                                  (stai_state_rev[stai_state_rev_keys] < 1)].count(axis=1)

        # sum the number of forward questions left blank or preferred not to answer
        stai_state_rev_leftblank = stai_state_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        stai_state_rev_prefernotanswer = stai_state_rev[stai_state_rev[stai_state_rev_keys] == nonresp['STAI']].count(axis=1)
        stai_state_rev_unanswered = stai_state_rev_leftblank + stai_state_rev_prefernotanswer

        # sum all the reverse scores
        stai_state_reverse_score = stai_state_rev[stai_state_rev[stai_state_rev_keys] <= 4].rsub(5).sum(axis=1, skipna=True)

        # Total STAI STATE SCORE
        total_STAI_state_score = stai_state_forward_score + stai_state_reverse_score
        # TOTAL STAI TRAIT ANSWERS UNANSWERED
        total_STAI_state_unanswered = stai_state_forward_unanswered + stai_state_rev_unanswered


        # TOTAL ANSWERS LEFT BLANK
        total_stai_state_leftblank = stai_state_forward_leftblank + stai_state_rev_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_stai_state_prefernotanswer = stai_state_forward_prefernotanswer + stai_state_rev_prefernotanswer

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original drive score.
        total_STAI_state_score = total_STAI_state_score + (total_STAI_state_unanswered * total_STAI_state_score /
                                                           (len(stai_state_keys)+len(stai_state_rev_keys) - (total_STAI_state_unanswered)))


        staistateall = pd.DataFrame(
            {'STAI_State_Score': total_STAI_state_score, 'STAI_State_Left_Blank': total_stai_state_leftblank,
             'STAI_State_Prefer_Not_to_Answer': total_stai_state_prefernotanswer})



        # ------------------------------------------------------------------------------
        # Count the number of values that do not fit parameter values
        nofit = stai_trait_forward_nofit + stai_trait_rev_nofit + stai_state_forward_nofit + stai_state_rev_nofit

        # If there are any values that do not fit parameters, exit the code and make client find the values that did not work
        for x in nofit:
            if x >= 1:
                sys.exit("We found values that don't match parameter values for calculation in your STAI dataset. "
                         "Please make sure your values range from 1-4 (see stai script) and have only ONE prefer not to answer value.")


        # ------------------------------------------------------------------------------

        # Put the scores into one frame
        frames = [staitraitall, staistateall]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print("We could not find the STAI headers in your dataset. Please look at the stai function in this package and put in the correct keys.")
    except ValueError:
        print("We found strings in your STAI dataset. Please make sure there are no strings/letters in your input. Otherwise, we can't do our thang.")
