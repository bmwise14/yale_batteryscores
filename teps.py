#!/usr/bin/python

import pandas as pd

# input = the data you are using with with the keys listed below as headers

def teps(input):
    # TEMPORAL EXPERIENCE OF PLEASURE SCALE

    # RESOURCES USED:
    """http://www.sciencedirect.com/science/article/pii/S0092656605000991"""
    """http://online.sfsu.edu/dgard/Documents/TEPS%20and%20item%20key.pdf"""


    # SCORING:
    """
    1. Typically Scores from 1-6 on a Likert Scale with no prefer not to answer choice.

    2. Scores are the sum of each subscale. Questions that should be reverse scored are reverse scored.

    3. Any Question left blank was not counted toward subscales or final score.
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
        anticipatory_forward = input[anticipatory_keys].apply(pd.to_numeric, args=('coerce',))
        anticipatory_forward_leftblank = anticipatory_forward.apply(lambda x: sum(x.isnull().values), axis=1)

        # sum all the forward scores
        anticipatory_forward_score = anticipatory_forward[(anticipatory_forward[anticipatory_keys] >= 1) &
                                                          (anticipatory_forward[anticipatory_keys] <= 6)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        anticipatory_rev = input[anticipatory_keys_rev].apply(pd.to_numeric, args=('coerce',))

        # sum the number of reverse questions left blank or preferred not to answer
        anticipatory_reverse_leftblank = anticipatory_rev.apply(lambda x: sum(x.isnull().values), axis=1)

        # sum all the reverse scores
        anticipatory_rev_score = anticipatory_rev.rsub(7).sum(axis=1, skipna=True)

        # Total SCORE
        total_anticipatory_score = anticipatory_forward_score + anticipatory_rev_score

        # TOTAL ANSWERS LEFT BLANK
        total_anticipatory_leftblank = anticipatory_forward_leftblank + anticipatory_reverse_leftblank


        anticall = pd.DataFrame(
            {'TEPS_Anticipatory_Score': total_anticipatory_score, 'TEPS_Anticipatory_Left_Blank': total_anticipatory_leftblank})



        # ------------------------------------------------------------------------------
        # CONSUMMATORY SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        consummatory_forward = input[consummatory_keys].apply(pd.to_numeric, args=('coerce',))
        consummatory_forward_leftblank = anticipatory_forward.apply(lambda x: sum(x.isnull().values), axis=1)

        # sum all the forward scores
        consummatory_forward_score = consummatory_forward[(consummatory_forward[consummatory_keys] >= 1) &
                                                          (consummatory_forward[consummatory_keys] <= 6)].sum(axis=1)
        # final_score = consummatory_forward_score/8


        consumall = pd.DataFrame(
            {'TEPS_Consummatory_Score': consummatory_forward_score, 'TEPS_Consummatory_Left_Blank': consummatory_forward_leftblank})

        # ------------------------------------------------------------------------------
        # Put the scores into one frame
        frames = [anticall, consumall]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print("We could not find the TEPS headers in your dataset. Please look at the teps function in this package and put in the correct keys.")