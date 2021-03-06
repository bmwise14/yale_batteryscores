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


def bisbas(input, nonresp):
    # BEHAVIORAL INHIBITION SCALE / BEHAVIORAL ACTIVATION SCALE

    # RESOURCES USED:
    """GSP Scales Notebook - Holmes Lab"""
    """Range of Scores for Self-Report Measures: Holmes Lab GSP Scales Notebook"""
    """http://psycnet.apa.org/journals/psp/67/2/319.pdf"""

    # SCORING:
    """
    1. Scores are the sum of each subscale. Questions that should be reverse scored are reverse scored.

    2. How to handle missing values is not explicitly mentioned in the primary resources above, so
    if any value is left blank or prefer not to answer, those missing values will be replaced with the average
    score on that particular subscale and then added to the final subscore total (Avram).

    3. If the score is below a minimum value range or above a maximum value range for the subscale, it will be discarded.
                                                        Min     Max
                                            BAS_DRIVE   4       16
                                            BAS_FUN     4       16
                                            BAS_REWARD  5       20
                                            BIS         7       28

    """

    try:
        # VERY TRUE - SOMEWHAT TRUE - SOMEWHAT FALSE - VERY FALSE - PREFER NOT TO ANSWER
        #     1             2               3               4               YOUR #

        # ------------------------------------------------------------------------------
        # These are are the different headers and their corresponding questions
        # ALL BISBAS SCORES ARE REVERSE CODED EXCEPT the BIS HEADER
        drive_headers = ["BISBAS_3", "BISBAS_9", "BISBAS_12", "BISBAS_21"]
        funseeking_headers = ["BISBAS_5", "BISBAS_10", "BISBAS_15", "BISBAS_20"]
        reward_headers = ["BISBAS_4", "BISBAS_7", "BISBAS_14", "BISBAS_18",
                          "BISBAS_23"]
        forward_code_bis = ["BISBAS_2", "BISBAS_22"]
        reverse_code_bis = ["BISBAS_8", "BISBAS_13", "BISBAS_16",
                            "BISBAS_19", "BISBAS_24"]
        fillerheaders = ["BISBAS_1", "BISBAS_6", "BISBAS_11", "BISBAS_17"]


        # ------------------------------------------------------------------------------
        # FILLERS

        # change the numbers in drive headers to numeric floats
        fillers = input[fillerheaders].apply(pd.to_numeric, args=('raise',))

        # Are there any values that don't fit in the value parameters
        fillers_nofit = fillers[(fillers[fillerheaders] != nonresp['BISBAS']) &
                                  (fillers[fillerheaders] > 4) |
                                  (fillers[fillerheaders] < 1)].count(axis=1)


        # ------------------------------------------------------------------------------
        # DRIVE SCORE - ALL REVERSE, NO FORWARD

        # change the numbers in drive headers to numeric floats
        drive = input[drive_headers].apply(pd.to_numeric, args=('raise',))

        # Are there any values that don't fit in the value parameters
        drive_nofit = drive[(drive[drive_headers] != nonresp['BISBAS']) &
                                  (drive[drive_headers] > 4) |
                                  (drive[drive_headers] < 1)].count(axis=1)

        # These count the number of drive questions left blank or answered as 5 and sums them up as drive_unanswered
        drive_leftblank = drive.apply(lambda x: sum(x.isnull().values), axis=1)
        drive_prefernotanswer = drive[drive[drive_headers] == nonresp['BISBAS']].count(axis=1)
        drive_unanswered = drive_leftblank + drive_prefernotanswer

        # reverse the scores by subtracting 5 from the raw data. Score of each item ranges from 1 to 4.
        # A score of 5 is "prefer not to answer" and will not be scored.
        # Adds up the reverse scores
        drive_score = drive[drive[drive_headers] <= 4].rsub(5).sum(axis=1, skipna=True)


        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        drive_score = drive_score + (drive_unanswered * drive_score / (len(drive_headers)-drive_unanswered))


        driveall = pd.DataFrame({'Drive_Score' : drive_score, 'Drive Left Blank': drive_leftblank,
             'Drive Prefer Not to Answer': drive_prefernotanswer})


        # ------------------------------------------------------------------------------
        # FUNSEEKING SCORE - ALL REVERSE, NO FORWARD

        # change the numbers in funseeking headers to numeric floats
        funseeking = input[funseeking_headers].apply(pd.to_numeric, args=('raise',))

        # Are there any values that don't fit in the value parameters
        funseeking_nofit = funseeking[(funseeking[funseeking_headers] != nonresp['BISBAS']) &
                                  (funseeking[funseeking_headers] > 4) |
                                  (funseeking[funseeking_headers] < 1)].count(axis=1)

        # These count the number of drive questions left blank or answered as 5 and sums them up as drive_unanswered
        funseeking_leftblank = funseeking.apply(lambda x: sum(x.isnull().values), axis=1)
        funseeking_prefernotanswer = funseeking[funseeking[funseeking_headers] == nonresp['BISBAS']].count(axis=1)
        funseeking_unanswered = funseeking_leftblank + funseeking_prefernotanswer

        # reverse the scores by subtracting 5 from the raw data. Score of each item ranges from 1 to 4.
        # A score of 5 is "prefer not to answer."
        # sum the reversed scores together to get the funseeking score
        funseeking_score = funseeking[funseeking[funseeking_headers] <= 4].rsub(5).sum(axis=1, skipna=True)

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        funseeking_score = funseeking_score + (funseeking_unanswered * funseeking_score / (len(funseeking_headers)-funseeking_unanswered))


        funseekingall = pd.DataFrame({'Funseeking Score': funseeking_score, 'Funseeking Left Blank': funseeking_leftblank,
             'Funseeking Prefer Not to Answer': funseeking_prefernotanswer})


        # ------------------------------------------------------------------------------
        # REWARD SCORE - ALL REVERSE, NO FORWARD


        # change the numbers in reward headers to numeric floats
        reward = input[reward_headers].apply(pd.to_numeric, args=('raise',))

        # Are there any values that don't fit in the value parameters
        reward_nofit = reward[(reward[reward_headers] != nonresp['BISBAS']) &
                                  (reward[reward_headers] > 4) |
                                  (reward[reward_headers] < 1)].count(axis=1)

        # These count the number of drive questions left blank or answered as 5 and sums them up as drive_unanswered
        reward_leftblank = reward.apply(lambda x: sum(x.isnull().values), axis=1)
        reward_prefernotanswer = reward[reward[reward_headers] == nonresp['BISBAS']].count(axis=1)
        reward_unanswered = reward_leftblank + reward_prefernotanswer

        # reverse the scores by subtracting 5 from the raw data. Score of each item ranges from 1 to 4.
        # A score of 5 is "prefer not to answer."
        # sum the reversed scores together to get the reward seeking score
        reward_score = reward[reward[reward_headers] <= 4].rsub(5).sum(axis=1,skipna=True)

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        reward_score = reward_score + (reward_unanswered * reward_score / (len(reward_headers)-reward_unanswered))

        rewardall = pd.DataFrame({'Reward Score': reward_score, 'Reward Left Blank': reward_leftblank,
             'Reward Prefer Not to Answer': reward_prefernotanswer})


        # ------------------------------------------------------------------------------
        # BIS Score


        # change the numbers in reverse_code_bis to numeric floats
        bis_reverse = input[reverse_code_bis].apply(pd.to_numeric, args=('raise',))

        # Are there any values that don't fit in the value parameters
        bis_reverse_nofit = bis_reverse[(bis_reverse[reverse_code_bis] != nonresp['BISBAS']) &
                                  (bis_reverse[reverse_code_bis] > 4) |
                                  (bis_reverse[reverse_code_bis] < 1)].count(axis=1)

        # These count the number of drive questions left blank or answered as 5 and sums them up as drive_unanswered
        bisreverse_leftblank = bis_reverse.apply(lambda x: sum(x.isnull().values), axis=1)
        bisreverse_prefernotanswer = bis_reverse[bis_reverse[reverse_code_bis] == nonresp['BISBAS']].count(axis=1)
        bisreverse_unanswered = bisreverse_leftblank + bisreverse_prefernotanswer

        # reverse the scores by subtracting 5 from the raw data. Score of each item ranges from 1 to 4.
        # A score of 5 is "prefer not to answer."
        # sum the reversed scores together to get the BIS Reverse score
        reverse_bis_score = bis_reverse[bis_reverse[reverse_code_bis] <= 4].rsub(5).sum(axis=1, skipna=True)


        # change the numbers in forward_code_bis to numeric floats
        bis_forward = input[forward_code_bis].apply(pd.to_numeric, args=('raise',))

        # Are there any values that don't fit in the value parameters
        bis_forward_nofit = bis_forward[(bis_forward[forward_code_bis] != nonresp['BISBAS']) &
                                  (bis_forward[forward_code_bis] > 4) |
                                  (bis_forward[forward_code_bis] < 1)].count(axis=1)

        # These count the number of drive questions left blank or answered as 5 and sums them up as drive_unanswered
        bis_forward_leftblank = bis_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        bis_forward_prefernotanswer = bis_forward[bis_forward[forward_code_bis] == nonresp['BISBAS']].count(axis=1)
        bis_forward_unanswered = bis_forward_leftblank + bis_forward_prefernotanswer

        bis_unanswered = bisreverse_unanswered + bis_forward_unanswered

        # sum the forward scores together to get the BIS Forward score and keeps anything over 5 from the sum. Anything that is 5 is not counted in the final score
        forward_bis_score = bis_forward[(bis_forward[forward_code_bis] >= 1) &
                                        (bis_forward[forward_code_bis] <= 4)].sum(axis=1)

        # Get the total BIS Score
        total_bis_score = reverse_bis_score + forward_bis_score


        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        total_bis_score = (total_bis_score + (bis_unanswered * total_bis_score / (len(reverse_code_bis)+len(forward_code_bis)-bis_unanswered)))

        # TOTAL ANSWERS LEFT BLANK
        total_bis_leftblank = bis_forward_leftblank + bisreverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_bis_prefernotanswer = bis_forward_prefernotanswer + bisreverse_prefernotanswer


        bisall = pd.DataFrame({'BIS Score': total_bis_score, 'BIS Left Blank': total_bis_leftblank,
             'BIS Prefer Not to Answer': total_bis_prefernotanswer})

        # ------------------------------------------------------------------------------
        # Count the number of values that do not fit parameter values
        nofit = drive_nofit + funseeking_nofit + reward_nofit + bis_reverse_nofit + bis_forward_nofit + fillers_nofit

        # If there are any values that do not fit parameters, exit the code and make client find the values that did not work
        for x in nofit:
            if x >= 1:
                sys.exit("We found values that don't match parameter values for calculation in your BISBAS dataset. "
                         "Please make sure your values range from 1-4 (see bisbas script) and have only ONE prefer not to answer value.")

        # -----------------------------------------------------------------------------
        # Put the scores into one frame
        frames = [driveall, funseekingall, rewardall, bisall]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print("We could not find the BISBAS headers in your dataset. Please look at the bisbas function in this package and put in the correct keys.")
    except ValueError:
        print("We found strings in your BISBAS dataset. Please make sure there are no strings/letters in your input. Otherwise, we can't do our thang.")