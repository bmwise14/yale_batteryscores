#!/usr/bin/python


import pandas as pd

# input = the data you are using with with the keys listed below as headers
# nonresval = the Prefer Not To Answer Choice on your Questionnaire


def bisbas(input, nonresp):
    # BEHAVIORAL INHIBITION SCALE / BEHAVIORAL ACTIVATION SCALE

    # RESOURCES USED:
    """GSP Scales Notebook - Holmes Lab"""
    """http://psycnet.apa.org/journals/psp/67/2/319.pdf"""

    # SCORING:
    """
    1. Scores are the sum of each subscale. Questions that should be reverse scored are reverse scored.

    2. Any Prefer Not To Answer selection was not counted toward the subscales or final score.

    3. Any Question left blank was not counted toward the subscale or final score.
    """

    try:
        # VERY TRUE - SOMEWHAT TRUE - SOMEWHAT FALSE - VERY FALSE - PREFER NOT TO ANSWER
        #     1             2               3               4               5

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

        # ------------------------------------------------------------------------------
        # DRIVE SCORE - ALL REVERSE, NO FORWARD

        # change the numbers in drive headers to numeric floats
        drive = input[drive_headers].apply(pd.to_numeric, args=('coerce',))

        # These count the number of drive questions left blank or answered as 5 and sums them up as drive_unanswered
        drive_leftblank = drive.apply(lambda x: sum(x.isnull().values), axis=1)
        drive_prefernotanswer = drive[drive[drive_headers] == nonresp['BISBAS']].count(axis=1)
        drive_unanswered = drive_leftblank + drive_prefernotanswer

        # reverse the scores by subtracting 5 from the raw data. Score of each item ranges from 1 to 4.
        # A score of 5 is "prefer not to answer" and will not be scored.
        # Adds up the reverse scores
        drive_score = drive[drive[drive_headers] <= 4].rsub(5).sum(axis=1, skipna=True)


        driveall = pd.DataFrame({'Drive Score' : drive_score, 'Drive Left Blank': drive_leftblank,
             'Drive Prefer Not to Answer': drive_prefernotanswer})


        # ------------------------------------------------------------------------------
        # FUNSEEKING SCORE - ALL REVERSE, NO FORWARD

        # change the numbers in funseeking headers to numeric floats
        funseeking = input[funseeking_headers].apply(pd.to_numeric, args=('coerce',))

        # These count the number of drive questions left blank or answered as 5 and sums them up as drive_unanswered
        funseeking_leftblank = funseeking.apply(lambda x: sum(x.isnull().values), axis=1)
        funseeking_prefernotanswer = funseeking[funseeking[funseeking_headers] == nonresp['BISBAS']].count(axis=1)
        funseeking_unanswered = funseeking_leftblank + funseeking_prefernotanswer

        # reverse the scores by subtracting 5 from the raw data. Score of each item ranges from 1 to 4.
        # A score of 5 is "prefer not to answer."
        # sum the reversed scores together to get the funseeking score
        funseeking_score = funseeking[funseeking[funseeking_headers] <= 4].rsub(5).sum(axis=1,skipna=True)


        funseekingall = pd.DataFrame({'Funseeking Score': funseeking_score, 'Funseeking Left Blank': funseeking_leftblank,
             'Funseeking Prefer Not to Answer': funseeking_prefernotanswer})


        # ------------------------------------------------------------------------------
        # REWARD SCORE - ALL REVERSE, NO FORWARD


        # change the numbers in reward headers to numeric floats
        reward = input[reward_headers].apply(pd.to_numeric, args=('coerce',))

        # These count the number of drive questions left blank or answered as 5 and sums them up as drive_unanswered
        reward_leftblank = reward.apply(lambda x: sum(x.isnull().values), axis=1)
        reward_prefernotanswer = reward[reward[reward_headers] == nonresp['BISBAS']].count(axis=1)
        reward_unanswered = reward_leftblank + reward_prefernotanswer

        # reverse the scores by subtracting 5 from the raw data. Score of each item ranges from 1 to 4.
        # A score of 5 is "prefer not to answer."
        # sum the reversed scores together to get the reward seeking score
        reward_score = reward[reward[reward_headers] <= 4].rsub(5).sum(axis=1,skipna=True)


        rewardall = pd.DataFrame({'Reward Score': reward_score, 'Reward Left Blank': reward_leftblank,
             'Reward Prefer Not to Answer': reward_prefernotanswer})


        # ------------------------------------------------------------------------------
        # BIS Score


        # change the numbers in reverse_code_bis to numeric floats
        bis_reverse = input[reverse_code_bis].apply(pd.to_numeric, args=('coerce',))

        # These count the number of drive questions left blank or answered as 5 and sums them up as drive_unanswered
        bisreverse_leftblank = bis_reverse.apply(lambda x: sum(x.isnull().values), axis=1)
        bisreverse_prefernotanswer = bis_reverse[bis_reverse[reverse_code_bis] == nonresp['BISBAS']].count(axis=1)
        bisreverse_unanswered = bisreverse_leftblank + bisreverse_prefernotanswer

        # reverse the scores by subtracting 5 from the raw data. Score of each item ranges from 1 to 4.
        # A score of 5 is "prefer not to answer."
        # sum the reversed scores together to get the BIS Reverse score
        reverse_bis_score = bis_reverse[bis_reverse[reverse_code_bis] <= 4].rsub(5).sum(axis=1, skipna=True)


        # change the numbers in forward_code_bis to numeric floats
        bis_forward = input[forward_code_bis].apply(pd.to_numeric, args=('coerce',))

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


        # TOTAL ANSWERS LEFT BLANK
        total_bis_leftblank = bis_forward_leftblank + bisreverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_bis_prefernotanswer = bis_forward_prefernotanswer + bisreverse_prefernotanswer


        bisall = pd.DataFrame({'BIS Score': total_bis_score, 'BIS Left Blank': total_bis_leftblank,
             'BIS Prefer Not to Answer': total_bis_prefernotanswer})

        # ------------------------------------------------------------------------------

        allscores = pd.DataFrame({'Drive Score' : drive_score, 'Funseeking Score': funseeking_score,
                                  'Reward Score': reward_score, 'BIS Score': total_bis_score})
        allunanswered = pd.DataFrame({'Drive Left Blank': drive_leftblank, 'Funseeking Left Blank': funseeking_leftblank,
                                      'Reward Left Blank': reward_leftblank, 'BIS Left Blank': total_bis_leftblank})
        allprefernotanswer = pd.DataFrame({'Drive Prefer Not to Answer': drive_prefernotanswer, 'Funseeking Prefer Not to Answer': funseeking_prefernotanswer,
                                           'Reward Prefer Not to Answer': reward_prefernotanswer, 'BIS Prefer Not to Answer': total_bis_prefernotanswer})



        # Put the scores into one frame
        frames = [allscores, allunanswered, allprefernotanswer]
        result = pd.concat(frames, axis=1)
        return result


        # if QC_Non_resp_BIS < 7:
        #     BISBAS_BIS = int(sum(bis)) + float(QC_Non_resp_BIS * sum(bis) / len(bis))
        # if QC_Non_resp_BAS_drive < 4:
        #     BISBAS_BAS_Drive = int(sum(bas_drive)) + float(QC_Non_resp_BAS_drive * sum(bas_drive) / len(bas_drive))
        # if QC_Non_resp_BAS_fun < 4:
        #     BISBAS_BAS_Fun = int(sum(bas_fun)) + float(QC_Non_resp_BAS_fun * sum(bas_fun) / len(bas_fun))
        # if QC_Non_resp_BAS_rew < 5:
        #     BISBAS_BAS_Reward = int(sum(bas_reward)) + float(QC_Non_resp_BAS_rew * sum(bas_reward) / len(bas_reward))
        #
        # QC_Non_resp_BISBAS = QC_Non_resp_BIS + QC_Non_resp_BAS_drive + QC_Non_resp_BAS_fun + QC_Non_resp_BAS_rew
    except KeyError:
        print("We could not find the BISBAS headers in your dataset. Please look at the bisbas function in this package and put in the correct keys.")