#!/usr/bin/python

import pandas as pd

# input = the data you are using with with the keys listed below as headers
# nonresval = the Prefer Not To Answer Choice on your Questionnaire

def stai(input, nonresp):
    # STATE-TRAIT ANXIETY INVENTORY FOR ADULTS

    # RESOURCES USED:
    """GSP Scales - Holmes Lab"""

    # SCORING:
    """
    1. Score of each item typically ranges from 1-4 with a prefer not to answer choice.

    2. Scores are the sum of each subscale. Questions that should be reverse scored are reverse scored.

    3. Any Prefer Not To Answer selection was not counted toward the subscales or final score

    4. Any Question left blank was not counted toward the subscale or final score
    """

    try:
        # NOT AT ALL - SOMEWHAT - MODERATELY SO - VERY MUCH SO - PREFER NOT TO ANSWER
        #     1            2           3               4               5
        # ------------------------------------------------------------------------------
        stai_trait_keys = ['STAI_3', 'STAI_4', 'STAI_6', 'STAI_7', 'STAI_9', 'STAI_12', 'STAI_13', 'STAI_14', 'STAI_17',
                           'STAI_18']
        stai_trait_rev_keys = ['STAI_1', 'STAI_2', 'STAI_5', 'STAI_8', 'STAI_10', 'STAI_11', 'STAI_15', 'STAI_16',
                               'STAI_19',
                               'STAI_20']
        stai_state_keys = ['STAI_22', 'STAI_24', 'STAI_25', 'STAI_28', 'STAI_29', 'STAI_31', 'STAI_32', 'STAI_35',
                           'STAI_37',
                           'STAI_38', 'STAI_40']
        stai_state_rev_keys = ['STAI_21', 'STAI_23', 'STAI_26', 'STAI_27', 'STAI_30', 'STAI_33', 'STAI_34', 'STAI_36',
                               'STAI_39']




        # ------------------------------------------------------------------------------
        # STAI TRAIT SCORE

        # change the numbers in forward STAI Trait headers to numeric floats
        stai_trait_forward = input[stai_trait_keys].apply(pd.to_numeric, args=('coerce',))

        # sum the number of forward questions left blank or preferred not to answer
        stai_trait_forward_leftblank = stai_trait_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        stai_trait_forward_prefernotanswer = stai_trait_forward[stai_trait_forward[stai_trait_keys] == nonresp['STAI']].count(axis=1)
        stai_trait_forward_unanswered = stai_trait_forward_leftblank + stai_trait_forward_prefernotanswer

        # sum all the forward scores
        stai_trait_forward_score = stai_trait_forward[(stai_trait_forward[stai_trait_keys] >= 1) &
                                                      (stai_trait_forward[stai_trait_keys] <= 4)].sum(axis=1)

        # change the numbers in reverse STAI Trait headers to numeric floats
        stai_trait_rev = input[stai_trait_rev_keys].apply(pd.to_numeric, args=('coerce',))

        # sum the number of reverse questions left blank or preferred not to answer
        stai_trait_reverse_leftblank = stai_trait_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        stai_trait_reverse_prefernotanswer = stai_trait_rev[stai_trait_rev[stai_trait_rev_keys] == nonresp['STAI']].count(axis=1)
        stai_trait_reverse_unanswered = stai_trait_reverse_leftblank + stai_trait_reverse_prefernotanswer

        # sum all the reverse scores
        stai_trait_reverse_score = stai_trait_rev.rsub(5).sum(axis=1, skipna=True)

        # Total STAI TRAIT SCORE
        total_STAI_Trait_score = stai_trait_forward_score + stai_trait_reverse_score
        # TOTAL STAI TRAIT ANSWERS UNANSWERED
        total_STAI_Trait_unanswered = stai_trait_forward_unanswered + stai_trait_reverse_unanswered


        # TOTAL ANSWERS LEFT BLANK
        total_stai_trait_leftblank = stai_trait_forward_leftblank + stai_trait_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_stai_trait_prefernotanswer = stai_trait_forward_prefernotanswer + stai_trait_reverse_prefernotanswer



        staitraitall = pd.DataFrame(
            {'STAI Trait Score': total_STAI_Trait_score, 'STAI Trait Left Blank': total_stai_trait_leftblank,
             'STAI Trait Prefer Not to Answer': total_stai_trait_prefernotanswer})


        # ------------------------------------------------------------------------------
        # STAI STATE SCORE

        # change the numbers in forward STAI STATE headers to numeric floats
        stai_state_forward = input[stai_state_keys].apply(pd.to_numeric, args=('coerce',))
        # sum the number of forward questions left blank or preferred not to answer
        stai_state_forward_leftblank = stai_state_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        stai_state_forward_prefernotanswer = stai_state_forward[stai_state_forward[stai_state_keys] == nonresp['STAI']].count(axis=1)
        stai_state_forward_unanswered = stai_state_forward_leftblank + stai_state_forward_prefernotanswer

        # sum all the forward scores
        stai_state_forward_score = stai_state_forward[(stai_state_forward[stai_state_keys] >= 1) &
                                                      (stai_state_forward[stai_state_keys] <= 4)].sum(axis=1)

        # change the numbers in forward STAI STATE headers to numeric floats
        stai_state_rev = input[stai_state_rev_keys].apply(pd.to_numeric, args=('coerce',))

        # sum the number of forward questions left blank or preferred not to answer
        stai_state_rev_leftblank = stai_state_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        stai_state_rev_prefernotanswer = stai_state_rev[stai_state_rev[stai_state_rev_keys] == nonresp['STAI']].count(axis=1)
        stai_state_rev_unanswered = stai_state_rev_leftblank + stai_state_rev_prefernotanswer

        # sum all the reverse scores
        stai_state_reverse_score = stai_state_rev.rsub(5).sum(axis=1, skipna=True)

        # Total STAI STATE SCORE
        total_STAI_state_score = stai_state_forward_score + stai_state_reverse_score
        # TOTAL STAI TRAIT ANSWERS UNANSWERED
        total_STAI_state_unanswered = stai_state_forward_unanswered + stai_state_rev_unanswered


        # TOTAL ANSWERS LEFT BLANK
        total_stai_state_leftblank = stai_state_forward_leftblank + stai_state_rev_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_stai_state_prefernotanswer = stai_state_forward_prefernotanswer + stai_state_rev_prefernotanswer

        staistateall = pd.DataFrame(
            {'STAI State Score': total_STAI_state_score, 'STAI State Left Blank': total_stai_state_leftblank,
             'STAI State Prefer Not to Answer': total_stai_state_prefernotanswer})



        # ------------------------------------------------------------------------------

        # Put the scores into one frame
        frames = [staitraitall, staistateall]
        result = pd.concat(frames, axis=1)
        return result


        # if QC_Non_resp_STAI_T < 3:
        #     STAI_tAnxiety = int(sum(stai_trait) / len(stai_trait) * 20)
        # if QC_Non_resp_STAI_S < 3:
        #     STAI_sAnxiety = int(sum(stai_state) / len(stai_state) * 20)
        #
        # QC_Non_resp_STAI = QC_Non_resp_STAI_T + QC_Non_resp_STAI_S
    except KeyError:
        print("We could not find the STAI headers in your dataset. Please look at the stai function in this package and put in the correct keys.")
