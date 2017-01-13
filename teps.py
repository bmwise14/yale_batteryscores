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

def teps(input):
    # TEMPORAL EXPERIENCE OF PLEASURE SCALE

    # RESOURCES USED:
    """http://www.sciencedirect.com/science/article/pii/S0092656605000991"""
    """http://online.sfsu.edu/dgard/Documents/TEPS%20and%20item%20key.pdf"""


    # SCORING:
    """
    1. Typically Scores from 1-6 on a Likert Scale with no prefer not to answer choice.

    2. How to handle missing values is not explicitly mentioned in the primary resources above, so
    if any value is left blank, those missing values will be replaced with the average
    score on that particular subscale and then added to the final subscore total (Avram).

    3. If the score is below a minimum value range or above a maximum value range for the subscale, it will be discarded.
                                                        Min     Max
                                TEPS_ANTICIPATORY       10      60
                                TEPS_CONSUMMATORY       8       48
    """

    try:
        # Very false for me   moderately false for me   Slightly false for me   Slightly true for me   Moderately true for me   Very true for me
        #          1                      2                       3                      4                      5                      6

        # ------------------------------------------------------------------------------
        anticipatory_keys = ['TEPS_1', 'TEPS_4', 'TEPS_6', 'TEPS_8', 'TEPS_10', 'TEPS_11', 'TEPS_15', 'TEPS_16', 'TEPS_18']
        anticipatory_keys_rev = ['TEPS_13']
        consummatory_keys = ['TEPS_2', 'TEPS_3', 'TEPS_5', 'TEPS_7', 'TEPS_9', 'TEPS_12', 'TEPS_14', 'TEPS_17']

        # ------------------------------------------------------------------------------
        # ANTICIPATORY SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        anticipatory_forward = input[anticipatory_keys].apply(pd.to_numeric, args=('raise',))

        # Are there any values that don't fit in the value parameters
        anticipatory_forward_nofit = anticipatory_forward[(anticipatory_forward[anticipatory_keys] > 6) |
                                                          (anticipatory_forward[anticipatory_keys] < 1)].count(axis=1)

        anticipatory_forward_leftblank = anticipatory_forward.apply(lambda x: sum(x.isnull().values), axis=1)

        # sum all the forward scores
        anticipatory_forward_score = anticipatory_forward[(anticipatory_forward[anticipatory_keys] >= 1) &
                                                          (anticipatory_forward[anticipatory_keys] <= 6)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        anticipatory_rev = input[anticipatory_keys_rev].apply(pd.to_numeric, args=('raise',))

        # Are there any values that don't fit in the value parameters
        anticipatory_rev_nofit = anticipatory_rev[(anticipatory_rev[anticipatory_keys_rev] > 6) |
                                                          (anticipatory_rev[anticipatory_keys_rev] < 1)].count(axis=1)

        # sum the number of reverse questions left blank or preferred not to answer
        anticipatory_reverse_leftblank = anticipatory_rev.apply(lambda x: sum(x.isnull().values), axis=1)

        # sum all the reverse scores
        anticipatory_rev_score = anticipatory_rev[anticipatory_rev[anticipatory_keys_rev] <= 6].rsub(7).sum(axis=1, skipna=True)

        # Total SCORE
        total_anticipatory_score = anticipatory_forward_score + anticipatory_rev_score

        # TOTAL ANSWERS LEFT BLANK
        total_anticipatory_leftblank = anticipatory_forward_leftblank + anticipatory_reverse_leftblank


        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        total_anticipatory_score = total_anticipatory_score + (total_anticipatory_leftblank * total_anticipatory_score /
                                                               (len(anticipatory_keys) + len(anticipatory_keys_rev)-total_anticipatory_leftblank))

        anticall = pd.DataFrame(
            {'TEPS_Anticipatory_Score': total_anticipatory_score, 'TEPS_Anticipatory_Left_Blank': total_anticipatory_leftblank})


        # ------------------------------------------------------------------------------
        # CONSUMMATORY SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        consummatory_forward = input[consummatory_keys].apply(pd.to_numeric, args=('raise',))

        # Are there any values that don't fit in the value parameters
        consummatory_forward_nofit = consummatory_forward[(consummatory_forward[consummatory_keys] > 6) |
                                                          (consummatory_forward[consummatory_keys] < 1)].count(axis=1)

        consummatory_forward_leftblank = consummatory_forward.apply(lambda x: sum(x.isnull().values), axis=1)

        # sum all the forward scores
        consummatory_forward_score = consummatory_forward[(consummatory_forward[consummatory_keys] >= 1) &
                                                          (consummatory_forward[consummatory_keys] <= 6)].sum(axis=1)

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        consummatory_forward_score = consummatory_forward_score + (consummatory_forward_leftblank * consummatory_forward_score /
                                                                   (len(consummatory_keys)-consummatory_forward_leftblank))

        consumall = pd.DataFrame(
            {'TEPS_Consummatory_Score': consummatory_forward_score, 'TEPS_Consummatory_Left_Blank': consummatory_forward_leftblank})

        # ------------------------------------------------------------------------------
        # Count the number of values that do not fit parameter values
        nofit = anticipatory_forward_nofit + anticipatory_rev_nofit + consummatory_forward_nofit

        # If there are any values that do not fit parameters, exit the code and make client find the values that did not work
        for x in nofit:
            if x >= 1:
                sys.exit("We found values that don't match parameter values for calculation in your TEPS dataset. "
                         "Please make sure your values range from 1-6 (see teps script).")


        # ------------------------------------------------------------------------------
        # Put the scores into one frame
        frames = [anticall, consumall]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print("We could not find the TEPS headers in your dataset. Please look at the teps function in this package and put in the correct keys.")
    except ValueError:
        print("We found strings in your TEPS dataset. Please make sure there are no strings/letters in your input. Otherwise, we can't do our thang.")