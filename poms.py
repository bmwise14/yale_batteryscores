#!/usr/bin/python

import pandas as pd

# input = the data you are using with with the keys listed below as headers
# nonresval = the Prefer Not To Answer Choice on your Questionnaire


def poms(input, nonresp):
    # PROFILE OF MOOD STATES

    # Resources USED:
    """GSP Scales Notebook - Holmes Lab"""

    # SCORING:
    """
    1. Scores are the sum of each subscale, which ranges from 0-4.
    This battery will take your 1-5 range values and replace them with range 0-4.
    Then the final score is the Total Mood Disturbance Score, which is the sum of
    all factor scores minus the vigor score.

    2. Any Prefer Not To Answer selection was not counted toward the subscales or final score.

    3. Any Question left blank was not counted toward the subscale or final score.
    """
    try:
        # NOT AT ALL - A LITTLE - MODERATELY - QUITE A BIT - EXTREMELY - PREFER NOT TO ANSWER
        #     0            1          2             3           4           YOUR CHOICE
        # ------------------------------------------------------------------------------
        tension_anxiety_keys = ['poms_1', 'poms_6', 'poms_12', 'poms_16', 'poms_20']
        depression_dejection_keys = ['poms_7', 'poms_11', 'poms_15', 'poms_17', 'poms_21']
        anger_hostility_keys = ['poms_2', 'poms_9', 'poms_14', 'poms_25', 'poms_28']
        vigor_activity_keys = ['poms_4', 'poms_8', 'poms_10', 'poms_27', 'poms_30']
        fatigue_inertia_keys = ['poms_3', 'poms_13', 'poms_19', 'poms_22', 'poms_23']
        confusion_bewilderment_keys = ['poms_5', 'poms_18', 'poms_24', 'poms_26', 'poms_29']


        # ------------------------------------------------------------------------------
        # TENSION / ANXIETY SCORE - ALL FORWARD NO REVERSE

        # SCORES AND QUESTIONS UNANSWERED
        tension_anxiety = input[tension_anxiety_keys].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])
        tension_leftblank = tension_anxiety.apply(lambda x: sum(x.isnull().values), axis=1)
        tension_prefernotanswer = tension_anxiety[tension_anxiety[tension_anxiety_keys] == nonresp['poms']].count(axis=1)

        # TOTAL ANSWERS UNANSWERED
        tension_anxiety_unanswered = tension_leftblank + tension_prefernotanswer

        # Total SCORE
        tension_anxiety_score = tension_anxiety[(tension_anxiety[tension_anxiety_keys] >=0) &
                                                (tension_anxiety[tension_anxiety_keys] <=4)].sum(axis=1)

        tenanxall = pd.DataFrame(
            {'POMS_Tension/Anxiety_Score': tension_anxiety_score, 'POMS_Tension/Anxiety_Left_Blank': tension_leftblank,
             'POMS_Tension/Anxiety_Prefer_Not_to_Answer': tension_prefernotanswer})


        # ------------------------------------------------------------------------------
        # DEPRESSION / DEJECTION SCORE - ALL FORWARD NO REVERSE

        # SCORES AND QUESTIONS UNANSWERED
        depression_dejection = input[depression_dejection_keys].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])
        depression_dejection_leftblank = depression_dejection.apply(lambda x: sum(x.isnull().values), axis=1)
        depression_dejection_prefernotanswer = depression_dejection[depression_dejection[depression_dejection_keys] == nonresp['poms']].count(axis=1)

        # TOTAL ANSWERS UNANSWERED
        depression_dejection_unanswered = depression_dejection_leftblank + depression_dejection_prefernotanswer

        # Total SCORE
        depression_dejection_score = depression_dejection[(depression_dejection[depression_dejection_keys] >= 0) &
                                                          (depression_dejection[depression_dejection_keys] <= 4)].sum(axis=1)

        depdejall = pd.DataFrame(
            {'POMS_Depresssion/Dejection_Score': depression_dejection_score, 'POMS_Depresssion/Dejection_Left_Blank': depression_dejection_leftblank,
             'POMS_Depresssion/Dejection_Prefer_Not_to_Answer': depression_dejection_prefernotanswer})


        # ------------------------------------------------------------------------------
        # ANGER / HOSTILITY SCORE - ALL FORWARD NO REVERSE

        # SCORES AND QUESTIONS UNANSWERED
        anger_hostility = input[anger_hostility_keys].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])
        anger_hostility_leftblank = anger_hostility.apply(lambda x: sum(x.isnull().values), axis=1)
        anger_hostility_prefernotanswer = anger_hostility[anger_hostility[anger_hostility_keys] == nonresp['poms']].count(axis=1)

        # TOTAL ANSWERS UNANSWERED
        anger_hostility_unanswered = anger_hostility_leftblank + anger_hostility_prefernotanswer

        # Total SCORE
        anger_hostility_score = anger_hostility[(anger_hostility[anger_hostility_keys] >= 0) &
                                                (anger_hostility[anger_hostility_keys] <= 4)].sum(axis=1)

        anghosall = pd.DataFrame(
            {'POMS_Anger/Hostility_Score': anger_hostility_score, 'POMS_Anger/Hostility_Left_Blank': anger_hostility_leftblank,
             'POMS_Anger/Hostility_Prefer_Not_to_Answer': anger_hostility_prefernotanswer})



        # ------------------------------------------------------------------------------
        # VIGOR / ACTIVITY SCORE - ALL FORWARD NO REVERSE

        # SCORES AND QUESTIONS UNANSWERED
        vigor_activity = input[vigor_activity_keys].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])
        vigor_activity_leftblank = vigor_activity.apply(lambda x: sum(x.isnull().values), axis=1)
        vigor_activity_prefernotanswer = vigor_activity[vigor_activity[vigor_activity_keys] == nonresp['poms']].count(axis=1)

        # TOTAL ANSWERS UNANSWERED
        vigor_activity_unanswered = vigor_activity_leftblank + vigor_activity_prefernotanswer

        # Total SCORE
        vigor_activity_score = vigor_activity[(vigor_activity[vigor_activity_keys] >= 0) &
                                              (vigor_activity[vigor_activity_keys] <= 4)].sum(axis=1)

        vigactall = pd.DataFrame(
            {'POMS_Vigor/Activity_Score': vigor_activity_score, 'POMS_Vigor/Activity_Left_Blank': vigor_activity_leftblank,
             'POMS_Vigor/Activity_Prefer_Not_to_Answer': vigor_activity_prefernotanswer})

        # ------------------------------------------------------------------------------
        # FATIGUE / INERTIA SCORE - ALL FORWARD NO REVERSE

        # SCORES AND QUESTIONS UNANSWERED
        fatigue_inertia = input[fatigue_inertia_keys].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])
        fatigue_inertia_leftblank = fatigue_inertia.apply(lambda x: sum(x.isnull().values), axis=1)
        fatigue_inertia_prefernotanswer = fatigue_inertia[fatigue_inertia[fatigue_inertia_keys] == nonresp['poms']].count(axis=1)

        # TOTAL ANSWERS UNANSWERED
        fatigue_inertia_unanswered = fatigue_inertia_leftblank + fatigue_inertia_prefernotanswer

        # Total SCORE
        fatigue_inertia_score = fatigue_inertia[(fatigue_inertia[fatigue_inertia_keys] >= 0) &
                                                (fatigue_inertia[fatigue_inertia_keys] <= 4)].sum(axis=1)

        fatinertall = pd.DataFrame(
            {'POMS_Fatigue/Inertia_Score': fatigue_inertia_score, 'POMS_Fatigue/Inertia_Left_Blank': fatigue_inertia_leftblank,
             'POMS_Fatigue/Inertia_Prefer_Not_to_Answer': fatigue_inertia_prefernotanswer})


        # ------------------------------------------------------------------------------
        # CONFUSION / BEWILDERMENT SCORE - ALL FORWARD NO REVERSE

        # SCORES AND QUESTIONS UNANSWERED
        confusion_bewilderment = input[confusion_bewilderment_keys].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])
        confusion_bewilderment_leftblank = confusion_bewilderment.apply(lambda x: sum(x.isnull().values), axis=1)
        confusion_bewilderment_prefernotanswer = confusion_bewilderment[confusion_bewilderment[confusion_bewilderment_keys] == nonresp['poms']].count(axis=1)

        # TOTAL ANSWERS UNANSWERED
        confusion_bewilderment_unanswered = confusion_bewilderment_leftblank + confusion_bewilderment_prefernotanswer

        # Total SCORE
        confusion_bewilderment_score = confusion_bewilderment[(confusion_bewilderment[confusion_bewilderment_keys] >= 0) &
                                                              (confusion_bewilderment[confusion_bewilderment_keys] <= 4)].sum(axis=1)

        confbewildall = pd.DataFrame(
            {'POMS_Confusion/Bewilderment_Score': confusion_bewilderment_score, 'POMS_Confusion/Bewilderment_Left_Blank': confusion_bewilderment_leftblank,
             'POMS_Confusion/Bewilderment_Prefer_Not_to_Answer': confusion_bewilderment_prefernotanswer})


        # ------------------------------------------------------------------------------
        # TOTAL MOOD DISTURBANCE SCORE
        # (T + D + A + F + C) - V
        # (TENSION + DEPRESSION + ANGER + FATIGUE + CONFUSION) - VIGOR

        totalmoodscore = pd.DataFrame({'POMS_Total_Mood_Disturbance': (tension_anxiety_score + depression_dejection_score +
                                                                       anger_hostility_score + fatigue_inertia_score +
                                                                       confusion_bewilderment_score) - vigor_activity_score})

        # ------------------------------------------------------------------------------
        # Put the scores into one frame
        frames = [tenanxall, depdejall, anghosall, vigactall, fatinertall, confbewildall, totalmoodscore]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print("We could not find the POMS headers in your dataset. Please look at the poms function in this package and put in the correct keys.")

