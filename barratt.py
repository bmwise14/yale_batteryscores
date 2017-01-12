#!/usr/bin/python

"""
Battery Scores Package for Processing Qualtrics CSV Files

@author: Bradley Wise
@email: bradley.wise@yale.edu
@version: 1.1
@date: 2016.12.06
"""


import pandas as pd


# input = the data you are using with with the keys listed below as headers
# nonresval = the Prefer Not To Answer Choice on your Questionnaire


def barratt(input, nonresp):
    # BARRATT IMPULSIVITY SCALE

    # RESOURCES USED:
    """GSP Scales Notebook - Holmes Lab"""
    """https://holmeslab-holmeslab.pbworks.com/w/file/84244846/BISScoring.pdf"""
    """http://homepages.se.edu/cvonbergen/files/2013/01/Factor-Structure-of-the-Barratt-Impulsiveness-Scale.pdf"""

    # SCORING:
    """
    1. The Barratt Impulsiveness Scale, Version 11 (BIS-11; Patton et al., 1995) is a 30 item self-report questionnaire
    designed to assess general impulsiveness taking into account the multi-factorial nature of the construct.
    The structure of the instrument allows for the assessment of six first-order factors (attention, motor, self-control,
    cognitive complexity, perseverance, cognitive stability) and three second-order factors (attention impulsiveness,
    motor impulsiveness, nonplanning impulsiveness). A total score is obtained by summing the first or second-order factors.

    2. The items are normally scored on a 4-point scale. (RARELY/NEVER-1, OCCASIONALLY-2, OFTEN-3, ALMOST ALWAYS/ALWAYS-4).
     Questions that should be reverse scored are reverse scored. Your scale may or may not have a PREFER NOT TO ANSWER value.

    3. How to handle missing values is not explicitly mentioned in the primary resources above, so
    if any value is left blank or prefer not to answer, those missing values will be replaced with the average
    score on that particular subscale and then added to the final subscore total (Avram).

    4. If the score is below a minimum value range or above a maximum value range for the subscale, it will be discarded.
                                                        Min     Max
                                    Barratt_2attention  8       32
                                    Barratt_2motor      11      44
                                    Barratt_2nonplan    11      44
                                    Barratt_1attention  5       20
                                    Barratt_1motor      7       28
                                    Barratt_1selfcont   6       24
                                    Barratt_1complex    5       20
                                    Barratt_1persevere  4       16
                                    Barratt_1instable   3       12
                                    Barratt_tot         30      120 <- for either scale


    """


    try:
        # RARELY/NEVER - OCCASIONALLY - OFTEN - ALMOST ALWAYS/ALWAYS - PREFER NOT TO ANSWER
        #     1               2           3             4                  YOUR VALUE
        # ------------------------------------------------------------------------------
        barratt_1atten_keys = ['barratt_5', 'barratt_11', 'barratt_28']
        barratt_1atten_rev_keys = ['barratt_9', 'barratt_20']
        barratt_1instability_keys = ['barratt_6', 'barratt_24', 'barratt_26']
        barratt_1mot_keys = ['barratt_2', 'barratt_3', 'barratt_4', 'barratt_17', 'barratt_19', 'barratt_22', 'barratt_25']
        barratt_1persever_keys = ['barratt_16', 'barratt_21', 'barratt_23']
        barratt_1persever_rev_keys = ['barratt_30']
        barratt_1selfcontrol_keys = ['barratt_14']
        barratt_1selfcontrol_rev_keys = ['barratt_1', 'barratt_7', 'barratt_8', 'barratt_12', 'barratt_13']
        barratt_1complex_keys = ['barratt_18', 'barratt_27']
        barratt_1complex_rev_keys = ['barratt_10', 'barratt_15', 'barratt_29']
        barratt_2attentionalimpulsiveness_keys = ["barratt_5", "barratt_6", "barratt_11", "barratt_24", "barratt_26", "barratt_28"]
        barratt_2attentionalimpulsiveness_rev_keys =["barratt_9", "barratt_20"]
        barratt_2motorimpulsiveness_keys = ["barratt_2", "barratt_3", "barratt_4", "barratt_16",
                                      "barratt_17", "barratt_19", "barratt_21", "barratt_22", "barratt_23", "barratt_25"]
        barratt_2motorimpulsiveness_rev_keys = ["barratt_30"]
        barratt_2nonplanningimpulsiveness_keys = [ "barratt_14", "barratt_18", "barratt_27"]
        barratt_2nonplanningimpulsiveness_rev_keys = ["barratt_1", "barratt_7", "barratt_8", "barratt_10",
                                            "barratt_12", "barratt_13", "barratt_15", "barratt_29"]


        # ------------------------------------------------------------------------------
        # BIS ATTENTION

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        atten1_forward = input[barratt_1atten_keys].apply(pd.to_numeric, args=('raise',))
        atten1_forward_leftblank = atten1_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        atten1_forward_prefernotanswer = atten1_forward[atten1_forward[barratt_1atten_keys] == nonresp['barratt']].count(axis=1)
        atten1_forward_unanswered = atten1_forward_leftblank + atten1_forward_prefernotanswer

        # sum all the forward scores
        atten1_forward_score = atten1_forward[(atten1_forward[barratt_1atten_keys] >= 1) &
                                              (atten1_forward[barratt_1atten_keys] <= 4)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        atten1_rev = input[barratt_1atten_rev_keys].apply(pd.to_numeric, args=('raise',))

        # sum the number of reverse questions left blank or preferred not to answer
        atten1_reverse_leftblank = atten1_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        atten1_reverse_prefernotanswer = atten1_rev[atten1_rev[barratt_1atten_rev_keys] == nonresp['barratt']].count(axis=1)
        atten1_reverse_unanswered = atten1_reverse_leftblank + atten1_reverse_prefernotanswer

        # sum all the reverse scores
        atten1_rev_score = atten1_rev[atten1_rev[barratt_1atten_rev_keys] <= 4].rsub(5).sum(axis=1, skipna=True)

        # Total SCORE
        total_atten1_score = atten1_forward_score + atten1_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_atten1_unanswered = atten1_forward_unanswered + atten1_reverse_unanswered

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        total_atten1_score = (total_atten1_score + (total_atten1_unanswered * total_atten1_score /
                                                    (len(barratt_1atten_keys)+len(barratt_1atten_rev_keys)- total_atten1_unanswered)))


        # TOTAL ANSWERS LEFT BLANK
        total_atten1_leftblank = atten1_forward_leftblank + atten1_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_atten1_prefernotanswer = atten1_forward_prefernotanswer + atten1_reverse_prefernotanswer

        # ------------------------------------------------------------------------------
        # BIS COGNITIVE INSTABILITY - ALL FORWARD, NO REVERSE

        # SCORES AND QUESTIONS UNANSWERED
        instability = input[barratt_1instability_keys].apply(pd.to_numeric, args=('raise',))
        instability_leftblank = instability.apply(lambda x: sum(x.isnull().values), axis=1)
        instability_prefernotanswer = instability[instability[barratt_1instability_keys] == nonresp['barratt']].count(axis=1)

        # TOTAL ANSWERS UNANSWERED
        instability_unanswered = instability_leftblank + instability_prefernotanswer

        # Total SCORE
        instability_score = instability[(instability[barratt_1instability_keys] >= 1) &
                                        (instability[barratt_1instability_keys] <= 4)].sum(axis=1)

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        instability_score = (instability_score + (instability_unanswered * instability_score /
                                                  (len(barratt_1instability_keys)-instability_unanswered)))

        # ------------------------------------------------------------------------------
        # BIS MOTOR - ALL FORWARD, NO REVERSE

        # SCORES AND QUESTIONS UNANSWERED
        motor = input[barratt_1mot_keys].apply(pd.to_numeric, args=('raise',))
        motor_leftblank = motor.apply(lambda x: sum(x.isnull().values), axis=1)
        motor_prefernotanswer = motor[motor[barratt_1mot_keys] == nonresp['barratt']].count(axis=1)

        # TOTAL ANSWERS UNANSWERED
        motor_unanswered = motor_leftblank + motor_prefernotanswer

        # Total SCORE
        motor_score = motor[(motor[barratt_1mot_keys] >= 1) &
                            (motor[barratt_1mot_keys] <= 4)].sum(axis=1)


        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        motor_score = (motor_score + (motor_unanswered * motor_score / (len(barratt_1mot_keys)-motor_unanswered)))

        # ------------------------------------------------------------------------------
        # BIS SELF-CONTROL

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        selfcontrol1_forward = input[barratt_1selfcontrol_keys].apply(pd.to_numeric, args=('raise',))
        selfcontrol1_forward_leftblank = selfcontrol1_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        selfcontrol1_forward_prefernotanswer = selfcontrol1_forward[selfcontrol1_forward[barratt_1selfcontrol_keys] == nonresp['barratt']].count(axis=1)
        selfcontrol1_forward_unanswered = selfcontrol1_forward_leftblank + selfcontrol1_forward_prefernotanswer

        # sum all the forward scores
        selfcontrol1_forward_score = selfcontrol1_forward[(selfcontrol1_forward[barratt_1selfcontrol_keys] >= 1) &
                                                          (selfcontrol1_forward[barratt_1selfcontrol_keys] <= 4)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        selfcontrol1_rev = input[barratt_1selfcontrol_rev_keys].apply(pd.to_numeric, args=('raise',))

        # sum the number of reverse questions left blank or preferred not to answer
        selfcontrol1_reverse_leftblank = selfcontrol1_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        selfcontrol1_reverse_prefernotanswer = selfcontrol1_rev[selfcontrol1_rev[barratt_1selfcontrol_rev_keys] == nonresp['barratt']].count(axis=1)
        selfcontrol1_reverse_unanswered = selfcontrol1_reverse_leftblank + selfcontrol1_reverse_prefernotanswer

        # sum all the reverse scores
        selfcontrol1_rev_score = selfcontrol1_rev[selfcontrol1_rev[barratt_1selfcontrol_rev_keys] <= 4].rsub(5).sum(axis=1, skipna=True)

        # Total SCORE
        total_selfcontrol1_score = selfcontrol1_forward_score + selfcontrol1_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_selfcontrol1_unanswered = selfcontrol1_forward_unanswered + selfcontrol1_reverse_unanswered

        # TOTAL ANSWERS LEFT BLANK
        total_selfcontrol1_leftblank = selfcontrol1_forward_leftblank + selfcontrol1_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_selfcontrol1_prefernotanswer = selfcontrol1_forward_prefernotanswer + selfcontrol1_reverse_prefernotanswer


        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        total_selfcontrol1_score = (total_selfcontrol1_score + (total_selfcontrol1_unanswered * total_selfcontrol1_score /
                                                                (len(barratt_1selfcontrol_keys)+len(barratt_1selfcontrol_rev_keys)-total_selfcontrol1_unanswered)))

        # ------------------------------------------------------------------------------
        # BIS COGNITIVE COMPLEXITY

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        complex1_forward = input[barratt_1complex_keys].apply(pd.to_numeric, args=('raise',))
        complex1_forward_leftblank = complex1_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        complex1_forward_prefernotanswer = complex1_forward[complex1_forward[barratt_1complex_keys] == nonresp['barratt']].count(axis=1)
        complex1_forward_unanswered = complex1_forward_leftblank + complex1_forward_prefernotanswer

        # sum all the forward scores
        complex1_forward_score = complex1_forward[(complex1_forward[barratt_1complex_keys] >= 1) &
                                                  (complex1_forward[barratt_1complex_keys] <= 4)].sum(axis=1)


        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        complex1_rev = input[barratt_1complex_rev_keys].apply(pd.to_numeric, args=('raise',))

        # sum the number of reverse questions left blank or preferred not to answer
        complex1_reverse_leftblank = complex1_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        complex1_reverse_prefernotanswer = complex1_rev[complex1_rev[barratt_1complex_rev_keys] == nonresp['barratt']].count(axis=1)
        complex1_reverse_unanswered = complex1_reverse_leftblank + complex1_reverse_prefernotanswer

        # sum all the reverse scores
        complex1_rev_score = complex1_rev[complex1_rev[barratt_1complex_rev_keys] <= 4].rsub(5).sum(axis=1, skipna=True)

        # Total SCORE
        total_complex1_score = complex1_forward_score + complex1_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_complex1_unanswered = complex1_forward_unanswered + complex1_reverse_unanswered

        # TOTAL ANSWERS LEFT BLANK
        total_complex1_leftblank = complex1_forward_leftblank + complex1_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_complex1_prefernotanswer = complex1_forward_prefernotanswer + complex1_reverse_prefernotanswer


        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        total_complex1_score = (total_complex1_score + (total_complex1_unanswered * total_complex1_score /
                                                        (len(barratt_1complex_keys)+len(barratt_1complex_rev_keys)-total_complex1_unanswered)))

        # ------------------------------------------------------------------------------
        # BIS PERSEVERANCE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        persever1_forward = input[barratt_1persever_keys].apply(pd.to_numeric, args=('raise',))
        persever1_forward_leftblank = persever1_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        persever1_forward_prefernotanswer = persever1_forward[persever1_forward[barratt_1persever_keys] == nonresp['barratt']].count(axis=1)
        persever1_forward_unanswered = persever1_forward_leftblank + persever1_forward_prefernotanswer

        # sum all the forward scores
        persever1_forward_score = persever1_forward[(persever1_forward[barratt_1persever_keys] >= 1) &
                                                    (persever1_forward[barratt_1persever_keys] <= 4)].sum(axis=1)


        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        persever1_rev = input[barratt_1persever_rev_keys].apply(pd.to_numeric, args=('raise',))

        # sum the number of reverse questions left blank or preferred not to answer
        persever1_reverse_leftblank = persever1_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        persever1_reverse_prefernotanswer = persever1_rev[persever1_rev[barratt_1persever_rev_keys] == nonresp['barratt']].count(axis=1)
        persever1_reverse_unanswered = persever1_reverse_leftblank + persever1_reverse_prefernotanswer

        # sum all the reverse scores
        persever1_rev_score = persever1_rev[persever1_rev[barratt_1persever_rev_keys] <= 4].rsub(5).sum(axis=1, skipna=True)

        # Total SCORE
        total_persever1_score = persever1_forward_score + persever1_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_persever1_unanswered = persever1_forward_unanswered + persever1_reverse_unanswered

        # TOTAL ANSWERS LEFT BLANK
        total_persever1_leftblank = persever1_forward_leftblank + persever1_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_persever1_prefernotanswer = persever1_forward_prefernotanswer + persever1_reverse_prefernotanswer


        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        total_persever1_score = (total_persever1_score + (total_persever1_unanswered * total_persever1_score /
                                                          (len(barratt_1persever_keys)+len(barratt_1persever_rev_keys)-total_persever1_unanswered)))

        # ------------------------------------------------------------------------------
        # ATTENTIONAL IMPULSIVENESS


        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        atteimpuls2_forward = input[barratt_2attentionalimpulsiveness_keys].apply(pd.to_numeric, args=('raise',))
        atteimpuls2_forward_leftblank = atteimpuls2_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        atteimpuls2_forward_prefernotanswer = atteimpuls2_forward[atteimpuls2_forward[barratt_2attentionalimpulsiveness_keys] == nonresp['barratt']].count(axis=1)
        atteimpuls2_forward_unanswered = atteimpuls2_forward_leftblank + atteimpuls2_forward_prefernotanswer

        # sum all the forward scores
        atteimpuls2_forward_score = atteimpuls2_forward[(atteimpuls2_forward[barratt_2attentionalimpulsiveness_keys] >= 1) &
                                                        (atteimpuls2_forward[barratt_2attentionalimpulsiveness_keys] <= 4)].sum(axis=1)


        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        atteimpuls2_rev = input[barratt_2attentionalimpulsiveness_rev_keys].apply(pd.to_numeric, args=('raise',))

        # sum the number of reverse questions left blank or preferred not to answer
        atteimpuls2_reverse_leftblank = atteimpuls2_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        atteimpuls2_reverse_prefernotanswer = atteimpuls2_rev[atteimpuls2_rev[barratt_2attentionalimpulsiveness_rev_keys] == nonresp['barratt']].count(axis=1)
        atteimpuls2_reverse_unanswered = atteimpuls2_reverse_leftblank + atteimpuls2_reverse_prefernotanswer

        # sum all the reverse scores
        atteimpuls2_rev_score = atteimpuls2_rev[atteimpuls2_rev[barratt_2attentionalimpulsiveness_rev_keys] <= 4].rsub(5).sum(axis=1, skipna=True)

        # Total SCORE
        total_atteimpuls2_score = atteimpuls2_forward_score + atteimpuls2_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_atteimpuls2_unanswered = atteimpuls2_forward_unanswered + atteimpuls2_reverse_unanswered

        # TOTAL ANSWERS LEFT BLANK
        total_atteimpuls2_leftblank = atteimpuls2_forward_leftblank + atteimpuls2_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_atteimpuls2_prefernotanswer = atteimpuls2_forward_prefernotanswer + atteimpuls2_reverse_prefernotanswer

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        total_atteimpuls2_score = (total_atteimpuls2_score + (total_atteimpuls2_unanswered * total_atteimpuls2_score /
                                                              (len(barratt_2attentionalimpulsiveness_keys)+len(barratt_2attentionalimpulsiveness_rev_keys)-total_atteimpuls2_unanswered)))

        # ------------------------------------------------------------------------------
        # MOTOR IMPULSIVENESS
        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        motimpuls2_forward = input[barratt_2motorimpulsiveness_keys].apply(pd.to_numeric, args=('raise',))
        motimpuls2_forward_leftblank = motimpuls2_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        motimpuls2_forward_prefernotanswer = motimpuls2_forward[motimpuls2_forward[barratt_2motorimpulsiveness_keys] == nonresp['barratt']].count(axis=1)
        motimpuls2_forward_unanswered = motimpuls2_forward_leftblank + motimpuls2_forward_prefernotanswer

        # sum all the forward scores
        motimpuls2_forward_score = motimpuls2_forward[(motimpuls2_forward[barratt_2motorimpulsiveness_keys] >= 1) &
                                                      (motimpuls2_forward[barratt_2motorimpulsiveness_keys] <= 4)].sum(axis=1)


        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        motimpuls2_rev = input[barratt_2motorimpulsiveness_rev_keys].apply(pd.to_numeric, args=('raise',))

        # sum the number of reverse questions left blank or preferred not to answer
        motimpuls2_reverse_leftblank = motimpuls2_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        motimpuls2_reverse_prefernotanswer = motimpuls2_rev[motimpuls2_rev[barratt_2motorimpulsiveness_rev_keys] == nonresp['barratt']].count(axis=1)
        motimpuls2_reverse_unanswered = motimpuls2_reverse_leftblank + motimpuls2_reverse_prefernotanswer

        # sum all the reverse scores
        motimpuls2_rev_score = motimpuls2_rev[motimpuls2_rev[barratt_2motorimpulsiveness_rev_keys] <= 4].rsub(5).sum(axis=1, skipna=True)

        # Total SCORE
        total_motimpuls2_score = motimpuls2_forward_score + motimpuls2_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_motimpuls2_unanswered = motimpuls2_forward_unanswered + motimpuls2_reverse_unanswered


        # TOTAL ANSWERS LEFT BLANK
        total_motimpuls2_leftblank = motimpuls2_forward_leftblank + motimpuls2_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_motimpuls2_prefernotanswer = motimpuls2_forward_prefernotanswer + motimpuls2_reverse_prefernotanswer

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        total_motimpuls2_score = (total_motimpuls2_score + (total_motimpuls2_unanswered * total_motimpuls2_score /
                                                            (len(barratt_2motorimpulsiveness_keys)+len(barratt_2motorimpulsiveness_rev_keys)-total_motimpuls2_unanswered)))

        # ------------------------------------------------------------------------------
        # NONPLANNING IMPULSIVENESS


        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        nonplanimpuls2_forward = input[barratt_2nonplanningimpulsiveness_keys].apply(pd.to_numeric, args=('raise',))
        nonplanimpuls2_forward_leftblank = nonplanimpuls2_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        nonplanimpuls2_forward_prefernotanswer = nonplanimpuls2_forward[nonplanimpuls2_forward[barratt_2nonplanningimpulsiveness_keys] == nonresp['barratt']].count(axis=1)
        nonplanimpuls2_forward_unanswered = nonplanimpuls2_forward_leftblank + nonplanimpuls2_forward_prefernotanswer

        # sum all the forward scores
        nonplanimpuls2_forward_score = nonplanimpuls2_forward[(nonplanimpuls2_forward[barratt_2nonplanningimpulsiveness_keys] >= 1) &
                                                              (nonplanimpuls2_forward[barratt_2nonplanningimpulsiveness_keys] <= 4)].sum(axis=1)


        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        nonplanimpuls2_rev = input[barratt_2nonplanningimpulsiveness_rev_keys].apply(pd.to_numeric, args=('raise',))

        # sum the number of reverse questions left blank or preferred not to answer
        nonplanimpuls2_reverse_leftblank = nonplanimpuls2_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        nonplanimpuls2_reverse_prefernotanswer = nonplanimpuls2_rev[nonplanimpuls2_rev[barratt_2nonplanningimpulsiveness_rev_keys] == nonresp['barratt']].count(axis=1)
        nonplanimpuls2_reverse_unanswered = nonplanimpuls2_reverse_leftblank + nonplanimpuls2_reverse_prefernotanswer

        # sum all the reverse scores
        nonplanimpuls2_rev_score = nonplanimpuls2_rev[nonplanimpuls2_rev[barratt_2nonplanningimpulsiveness_rev_keys] <= 4].rsub(5).sum(axis=1, skipna=True)

        # Total SCORE
        total_nonplanimpuls2_score = nonplanimpuls2_forward_score + nonplanimpuls2_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_nonplanimpuls2_unanswered = nonplanimpuls2_forward_unanswered + nonplanimpuls2_reverse_unanswered


        # TOTAL ANSWERS LEFT BLANK
        total_nonplanimpuls2_leftblank = nonplanimpuls2_forward_leftblank + nonplanimpuls2_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_nonplanimpuls2_prefernotanswer = nonplanimpuls2_forward_prefernotanswer + nonplanimpuls2_reverse_prefernotanswer

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        total_nonplanimpuls2_score = (total_nonplanimpuls2_score + (total_nonplanimpuls2_unanswered * total_nonplanimpuls2_score /
                                                                    (len(barratt_2nonplanningimpulsiveness_keys)+len(barratt_2nonplanningimpulsiveness_rev_keys)-total_nonplanimpuls2_unanswered)))

        # ------------------------------------------------------------------------------
        # TOTAL BARRATT SCORE - CAN BE COMPUTED VIA PRIMARY OR SECONDARY KEYS ONLY
        barratt_total = total_atten1_score + instability_score + motor_score + total_selfcontrol1_score + total_complex1_score + total_persever1_score
        # barratt_total = ['Discard' if x < 30 else 'Discard' if x > 120 else x for x in barratt_total]


        barratt_leftblank = total_atten1_leftblank + instability_leftblank + motor_leftblank + total_selfcontrol1_leftblank + total_complex1_leftblank + total_persever1_leftblank
        barratt_pfn = total_atten1_prefernotanswer + instability_prefernotanswer + motor_prefernotanswer + total_selfcontrol1_prefernotanswer + total_complex1_prefernotanswer + total_persever1_prefernotanswer



        bistotal = pd.DataFrame(
            {'BIS_TOTAL_SCORE': barratt_total, 'BIS_TOTAL_Left_Blank': barratt_leftblank,
             'BIS_TOTAL_Prefer_Not_to_Answer': barratt_pfn})


        # ------------------------------------------------------------------------------
        # PRIMARY SCORES
        # Discard any value below 5 and above 20
        # total_atten1_score = ['Discard (<5)' if x < 5 else 'Discard (<20)' if x > 20 else x for x in total_atten1_score]
        attentionall = pd.DataFrame(
            {'BIS_Attention_Score': total_atten1_score, 'BIS_Attention_Left_Blank': total_atten1_leftblank,
             'BIS_Attention_Prefer_Not_to_Answer': total_atten1_prefernotanswer})

        # Discard any value below 3 and above 12
        # instability_score = ['Discard (<3)' if x < 3 else 'Discard (>12)' if x > 12 else x for x in instability_score]
        coginstall = pd.DataFrame(
            {'BIS_Cognitive_Instability_Score': instability_score, 'BIS_Cognitive_Instability_Left_Blank': instability_leftblank,
             'BIS_Cognitive_Instability_Prefer_Not_to_Answer': instability_prefernotanswer})

        # Discard any value below 7 and above 28
        # motor_score = ['Discard (<7)' if x < 7 else 'Discard (>28)' if x > 28 else x for x in motor_score]
        motorall = pd.DataFrame(
            {'BIS_Motor_Score': motor_score, 'BIS_Motor_Left_Blank': motor_leftblank,
             'BIS_Motor_Prefer_Not_to_Answer': motor_prefernotanswer})

        # Discard any value below 6 and above 24
        # total_selfcontrol1_score = ['Discard (<6)' if x < 6 else 'Discard (>24)' if x > 24 else x for x in total_selfcontrol1_score]
        selfcontrolall = pd.DataFrame(
            {'BIS_Self-Control_Score': total_selfcontrol1_score, 'BIS_Self-Control_Left_Blank': total_selfcontrol1_leftblank,
             'BIS_Self-Control_Prefer_Not_to_Answer': total_selfcontrol1_prefernotanswer})

        # Discard any value below 5 and above 20
        # total_complex1_score = ['Discard (<5)' if x < 5 else 'Discard (>20)' if x > 20 else x for x in total_complex1_score]
        cogcomplexall = pd.DataFrame(
            {'BIS_Cognitive_Complexity_Score': total_complex1_score, 'BIS_Cognitive_Complexity_Left_Blank': total_complex1_leftblank,
             'BIS_Cognitive_Complexity_Prefer_Not_to_Answer': total_complex1_prefernotanswer})

        # Discard any value below 4 and above 16
        # total_persever1_score = ['Discard (<4)' if x < 4 else 'Discard (>16)' if x > 16 else x for x in total_persever1_score]
        perseverall = pd.DataFrame(
            {'BIS_Perseverance_Score': total_persever1_score, 'BIS_Perseverance_Left_Blank': total_persever1_leftblank,
             'BIS_Perseverance_Prefer_Not_to_Answer': total_persever1_prefernotanswer})

        # ------------------------------------------------------------------------------
        # SECONDARY SCORES
        # Discard any value below 8 and above 32
        # total_atteimpuls2_score = ['Discard (<8)' if x < 8 else 'Discard (>32)' if x > 32 else x for x in total_atteimpuls2_score]
        attenimpulsall = pd.DataFrame(
            {'BIS_Attentional_Impulsiveness_Score': total_atteimpuls2_score, 'BIS_Attentional_Impulsiveness_Left_Blank': total_atteimpuls2_leftblank,
             'BIS_Attentional_Impulsiveness_Prefer_Not_to_Answer': total_atteimpuls2_prefernotanswer})


        # Discard any value below 11 and above 44
        # total_motimpuls2_score = ['Discard (<11)' if x < 11 else 'Discard (>44)' if x > 44 else x for x in total_motimpuls2_score]
        motorimpulsall = pd.DataFrame(
            {'BIS_Motor_Impulsiveness_Score': total_motimpuls2_score, 'BIS_Motor_Impulsiveness_Left_Blank': total_motimpuls2_leftblank,
             'BIS_Motor_Impulsiveness_Prefer_Not_to_Answer': total_motimpuls2_prefernotanswer})

        # Discard any value below 11 and above 44
        # total_nonplanimpuls2_score = ['Discard (<11)' if x < 11 else 'Discard (>44)' if x > 44 else x for x in total_nonplanimpuls2_score]
        nonplanimpulsall = pd.DataFrame(
            {'BIS_Nonplanning_Impulsiveness_Score': total_nonplanimpuls2_score, 'BIS_Nonplanning_Impulsiveness_Left_Blank': total_nonplanimpuls2_leftblank,
             'BIS_Nonplanning_Impulsiveness_Prefer_Not_to_Answer': total_nonplanimpuls2_prefernotanswer})

        # ------------------------------------------------------------------------------
        # Put the scores into one frame
        frames = [attentionall, coginstall, motorall, selfcontrolall, cogcomplexall, perseverall, attenimpulsall, motorimpulsall, nonplanimpulsall, bistotal]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print("We could not find the BARRATT headers in your dataset. Please look at the barratt function in this package and put in the correct keys.")
    except ValueError:
        print("We found strings in your BARRATT dataset. Please make sure there are no strings/letters in your input. Otherwise, we can't do our thang.")