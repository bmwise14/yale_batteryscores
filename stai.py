#!/usr/bin/python

import pandas as pd

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
    score on that particular subscale and then added to the final subscore total (Avram).

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
                               'STAI_19',
                               'STAI_20']
        stai_state_keys = ['STAI_22', 'STAI_24', 'STAI_25', 'STAI_28', 'STAI_29', 'STAI_31', 'STAI_32', 'STAI_35',
                           'STAI_37',
                           'STAI_38', 'STAI_40']
        stai_state_rev_keys = ['STAI_21', 'STAI_23', 'STAI_26', 'STAI_27', 'STAI_30', 'STAI_33', 'STAI_34', 'STAI_36',
                               'STAI_39']


        # all = [stai_trait_keys, stai_trait_rev_keys, stai_state_keys, stai_state_rev_keys]
        #
        #
        # for x in all:
        #     for_x = input[x].apply(pd.to_numeric, args=('coerce',))
        #     # sum the number of forward questions left blank or preferred not to answer
        #     x_forward_leftblank = for_x.apply(lambda x: sum(x.isnull().values), axis=1)
        #     x_forward_prefernotanswer = for_x[for_x[x] == nonresp['STAI']].count(axis=1)
        #     x_forward_unanswered = x_forward_leftblank + x_forward_prefernotanswer
        #     # sum all the forward scores
        #     x_forward_score = for_x[(for_x[x] >= 1) & (for_x[x] <= 4)].sum(axis=1)


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
        # Then divide that by the total number of questions in the subscale.
        # Add all of this to to the original drive score.
        total_STAI_Trait_score = total_STAI_Trait_score + (total_STAI_Trait_unanswered * total_STAI_Trait_score / (len(stai_trait_keys)+len(stai_trait_rev_keys)))

        # Discard any value below 20 and above 80
        # total_STAI_Trait_score = ['Discard (<20)' if x < 20 else 'Discard (>80)' if x > 80 else x for x in total_STAI_Trait_score]


        staitraitall = pd.DataFrame(
            {'STAI_Trait_Score': total_STAI_Trait_score, 'STAI_Trait_Left_Blank': total_stai_trait_leftblank,
             'STAI_Trait_Prefer_Not_to_Answer': total_stai_trait_prefernotanswer})


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
        # Then divide that by the total number of questions in the subscale.
        # Add all of this to to the original drive score.
        total_STAI_state_score = total_STAI_state_score + (total_STAI_state_unanswered * total_STAI_state_score / (len(stai_state_keys)+len(stai_state_rev_keys)))


        # Discard any value below 20 and above 80
        # total_STAI_state_score = ['Discard (<20)' if x < 20 else 'Discard (>80)' if x > 80 else x for x in total_STAI_state_score]

        staistateall = pd.DataFrame(
            {'STAI_State_Score': total_STAI_state_score, 'STAI_State_Left_Blank': total_stai_state_leftblank,
             'STAI_State_Prefer_Not_to_Answer': total_stai_state_prefernotanswer})



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
