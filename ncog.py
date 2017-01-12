#!/usr/bin/python

"""
Battery Scores Package for Processing Qualtrics CSV Files

@author: Bradley Wise with help from Audrey Luo
@email: bradley.wise@yale.edu, audrey.luo@yale.edu
@version: 1.1
@date: 2016.10.28


"""
import pandas as pd

# input = the data you are using with with the keys listed below as headers
# nonresval = the Prefer Not To Answer Choice on your Questionnaire


def ncog(input, nonresp):
    # Short Form of Need for Cognition

    # RESOURCES USED:
    """Short Form of the Need for Cognition Scale  - Holmes Lab"""
    """http://www.sjdm.org/dmidi/Need_for_Cognition_short.html"""


    # SCORING:
    """
    1. Raw subscores are computed by summing the total score. This scale replaces your Qualtrics Scale with the Scale below.
       Questions that should be reverse scored are reverse scored.

    2. How to handle missing values is not explicitly mentioned in the primary resources above, so
    if any value is left blank or prefer not to answer, those missing values will be replaced with the average
    score on that particular subscale and then added to the final subscore total (Avram).

    4. Minimum possible score = 18. Maximum possible score = 90.
    """

    try:
        # EXTREMELY UNCHARACTERISTIC - SOMEWHAT UNCHARACTERISTIC - UNCERTAIN - SOMEWHAT CHARACTERISTIC - EXTREMELY CHARACTERISTIC - PREFER NOT TO ANSWER
        #         1                                 2                  3                  4                         5                       YOUR #
        # ------------------------------------------------------------------------------
        ncog_keys = ['ncog_1', 'ncog_2', 'ncog_5', 'ncog_6', 'ncog_10', 'ncog_11', 'ncog_13', 'ncog_14', 'ncog_15', 'ncog_18']
        ncog_rev_keys = ['ncog_3', 'ncog_4', 'ncog_7', 'ncog_8', 'ncog_9', 'ncog_12', 'ncog_16', 'ncog_17']


        # ------------------------------------------------------------------------------
        # NCOG SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        ncog_forward = input[ncog_keys].apply(pd.to_numeric, args=('raise',))


        ncog_forward_leftblank = ncog_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        ncog_forward_prefernotanswer = ncog_forward[ncog_forward[ncog_keys] == nonresp['ncog']].count(axis=1)
        ncog_forward_unanswered = ncog_forward_leftblank + ncog_forward_prefernotanswer

        # sum all the forward scores
        ncog_forward_score = ncog_forward[(ncog_forward[ncog_keys] >= 0) &
                                                        (ncog_forward[ncog_keys] <= 5)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        ncog_rev = input[ncog_rev_keys].apply(pd.to_numeric, args=('raise',))

        # sum the number of reverse questions left blank or preferred not to answer
        ncog_reverse_leftblank = ncog_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        ncog_reverse_prefernotanswer = ncog_rev[ncog_rev[ncog_rev_keys] == nonresp['ncog']].count(axis=1)
        ncog_reverse_unanswered = ncog_reverse_leftblank + ncog_reverse_prefernotanswer

        # sum all the reverse scores
        ncog_rev_score = ncog_rev[ncog_rev[ncog_rev_keys] <= 5].rsub(6).sum(axis=1, skipna=True)

        # Total SCORE
        total_ncog_score = ncog_forward_score + ncog_rev_score

        # TOTAL ANSWERS UNANSWERED
        total_ncog_unanswered = ncog_forward_unanswered + ncog_reverse_unanswered

        # TOTAL ANSWERS LEFT BLANK
        total_ncog_leftblank = ncog_forward_leftblank + ncog_reverse_leftblank

        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_ncog_prefernotanswer = ncog_forward_prefernotanswer + ncog_reverse_prefernotanswer


        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the total number of questions in the subscale.
        # Add all of this to to the original drive score.
        total_ncog_score = (total_ncog_score + (total_ncog_unanswered * total_ncog_score / (len(ncog_keys)+len(ncog_rev_keys))))


        # Discard any value below 18 and above 90
        total_ncog_score = ['Discard' if x < 18
                            else 'Discard' if x > 90 else x for x in total_ncog_score]

        ncogall = pd.DataFrame(
            {'ncog_Score': total_ncog_score,
             'ncog_Left_Blank': total_ncog_leftblank,
             'ncog_Prefer_Not_to_Answer': total_ncog_prefernotanswer})

        # ------------------------------------------------------------------------------
        # Put all the scores into one frame
        frames = [ncogall]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print("We could not find the ncog headers in your dataset. Please look at the ncog function in this package and put in the correct keys.")
    except ValueError:
        print("We found strings in your ncog dataset. Please make sure there are no strings/letters in your input. Otherwise, we can't do our thang.")