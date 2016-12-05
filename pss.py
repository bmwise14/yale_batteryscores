#!/usr/bin/python


import pandas as pd

# input = the data you are using with with the keys listed below as headers


def pss(input):
    # PERCEIVED STRESS SCALE

    # RESOURCES USED:
    """Rdoc Scales Notebook - Holmes Lab"""
    """http://www.mindgarden.com/documents/PerceivedStressScale.pdf"""
    """http://www.psy.cmu.edu/~scohen/scales.html"""

    # TYPICAL SCORING
    """
    1. The Scale is typically 0-4, and the score is the sum of all answers.
    This battery will take your 1-5 range values and replace them with range 0-4.
    Questions that should be reverse scored are reverse scored.

    2. How to handle missing values is not explicitly mentioned in the primary resources above, so
    if any value is left blank or prefer not to answer, those missing values will be replaced with the average
    score on that particular subscale and then added to the final subscore total (Avram).

    3. If the score is below a minimum value range or above a maximum value range for the subscale, it will be discarded.
                                                        Min     Max
                                        PSS Score       0       40
    """
    try:
        # NEVER         ALMOST NEVER        SOMETIMES       FAIRLY OFTEN    VERY OFTEN
        #   0                1                  2                3               4

        # ------------------------------------------------------------------------------
        pss_negative_keys_for =['pss_1', 'pss_2', 'pss_3', 'pss_6', 'pss_9', 'pss_10']
        pss_positive_keys_rev =['pss_4', 'pss_5', 'pss_7', 'pss_8']


        # ------------------------------------------------------------------------------
        # PSS Reverse Scoring


        # change the numbers to numeric floats
        pss_reverse = input[pss_positive_keys_rev].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])

        # These count the number of questions left blank
        pss_rev_leftblank = pss_reverse.apply(lambda x: sum(x.isnull().values), axis=1)


        # reverse the scores by subtracting 4 from the raw data. Score of each item ranges from 0 to 4.
        # A score of 4 is "VERY OFTEN." It will be marked as 0 after subtraction and a score of 0 will be marked as 4.
        # sum the reversed scores together to get the PSS Reverse
        reverse_pss_score = pss_reverse[pss_reverse[pss_positive_keys_rev] <= 4].rsub(4).sum(axis=1, skipna=True)

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        reverse_pss_score = reverse_pss_score + (pss_rev_leftblank * reverse_pss_score / (len(pss_positive_keys_rev)-pss_rev_leftblank))

        # ------------------------------------------------------------------------------
        # PSS Forward Scoring


        # change the numbers to numeric floats
        pss_forward = input[pss_negative_keys_for].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])

        # These count the number of questions left blank
        pss_forward_leftblank = pss_forward.apply(lambda x: sum(x.isnull().values), axis=1)

        # sum the forward scores together to get the PSS Forward score and keeps anything less than or equal to 5
        forward_pss_score = pss_forward[(pss_forward[pss_negative_keys_for] >= 0) &
                                        (pss_forward[pss_negative_keys_for] <= 4)].sum(axis=1)

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        forward_pss_score = forward_pss_score + (pss_forward_leftblank * forward_pss_score / (len(pss_negative_keys_for)-pss_forward_leftblank))


        # ------------------------------------------------------------------------------
        # Get the total PSS Score
        total_pss_score = reverse_pss_score + forward_pss_score

        # total_pss_score = ['Discard' if x < 0 else 'Discard' if x > 40 else x for x in total_pss_score]


        # TOTAL ANSWERS LEFT BLANK
        total_pss_leftblank = pss_rev_leftblank + pss_forward_leftblank




        pssall = pd.DataFrame({'PSS Score': total_pss_score, 'PSS Left Blank': total_pss_leftblank})

        # ------------------------------------------------------------------------------

        # Put the scores into one frame
        frames = [pssall]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print("We could not find the PSS headers in your dataset. Please look at the pss function in this package and put in the correct keys.")