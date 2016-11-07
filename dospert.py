#!/usr/bin/python

import pandas as pd

# input = the data you are using with with the keys listed below as headers
# nonresval = the Prefer Not To Answer Choice on your Questionnaire


def dospert(input, nonresp):
    # DOMAIN-SPECIFIC RISK-TAKING SCALE

    # RESOURCES USED:
    """GSP Scales Notebook - Holmes Lab"""
    """http://onlinelibrary.wiley.com/doi/10.1002/bdm.414/full"""
    """http://journal.sjdm.org/jdm06005.pdf"""

    # SCORING:
    """
    1. Scores are the sum of each subscale (Risk-Taking and Risk-Perception).
    This one uses the 40-item scale, not the 2006 revised version (Blais & Weber, 2006).

    2. Any Prefer Not To Answer selection was not counted toward the subscales.

    3. Any Question left blank was not counted toward the subscale.
    """

    try:
        # RISK TAKING MODULE
        # EXTREMELY UNLIKELY - MODERATELY UNLIKELY - SOMEWHAT UNLIKELY - NOT SURE - SOMEWHAT LIKELY - MODERATELY LIKELY - EXTREMELY LIKELY - PREFER NOT TO ANSWER
        #           1                   2                   3               4             5                    6               7                     8
        # RISK PERCEPTION MODULE
        # NOT AT ALL RISKY - SLIGHTLY RISKY - SOMEWHAT RISKY - MODERATELY RISKY - RISKY - VERY RISKY - EXTREMELY RISKY - PREFER NOT TO ANSWER
        #           1              2                3                  4            5          6            7                   8
        # ------------------------------------------------------------------------------
        risktaking_keys = ['dospert_1', 'dospert_2', 'dospert_3', 'dospert_4', 'dospert_5', 'dospert_6', 'dospert_7',
                           'dospert_8', 'dospert_9', 'dospert_10', 'dospert_11', 'dospert_12', 'dospert_13', 'dospert_14',
                           'dospert_15', 'dospert_16', 'dospert_17', 'dospert_18', 'dospert_19', 'dospert_20', 'dospert_21',
                           'dospert_22', 'dospert_23', 'dospert_24', 'dospert_25', 'dospert_26', 'dospert_27', 'dospert_28',
                           'dospert_29', 'dospert_30', 'dospert_31', 'dospert_32', 'dospert_33', 'dospert_34', 'dospert_35',
                           'dospert_36', 'dospert_37', 'dospert_38', 'dospert_39', 'dospert_40']


        riskperception_keys = ['dospert_41', 'dospert_42', 'dospert_43', 'dospert_44', 'dospert_45', 'dospert_46', 'dospert_47',
                           'dospert_48', 'dospert_49', 'dospert_50', 'dospert_51', 'dospert_52', 'dospert_53', 'dospert_54',
                           'dospert_55', 'dospert_56', 'dospert_57', 'dospert_58', 'dospert_59', 'dospert_60', 'dospert_61',
                           'dospert_62', 'dospert_63', 'dospert_64', 'dospert_65', 'dospert_66', 'dospert_67', 'dospert_68',
                           'dospert_69', 'dospert_70', 'dospert_71', 'dospert_72', 'dospert_73', 'dospert_74', 'dospert_75',
                           'dospert_76', 'dospert_77', 'dospert_78', 'dospert_79', 'dospert_80']
        # ------------------------------------------------------------------------------
        # DOSPERT RISKTAKING SCORE - ALL FORWARD, NO REVERSE

        # SCORES AND QUESTIONS UNANSWERED
        risktaking = input[risktaking_keys].apply(pd.to_numeric, args=('coerce',))
        risktaking_leftblank = risktaking.apply(lambda x: sum(x.isnull().values), axis=1)
        risktaking_prefernotanswer = risktaking[risktaking[risktaking_keys] == nonresp['dospert']].count(axis=1)

        # TOTAL ANSWERS UNANSWERED
        risktaking_unanswered = risktaking_leftblank + risktaking_prefernotanswer

        # Total SCORE
        risktaking_score = risktaking[(risktaking[risktaking_keys] >= 1) &
                                      (risktaking[risktaking_keys] <= 7)].sum(axis=1)

        risktakingall = pd.DataFrame(
            {'DOSPERT Risktaking Score': risktaking_score, 'DOSPERT Risktaking Left Blank': risktaking_leftblank,
             'DOSPERT Risktaking Prefer Not to Answer': risktaking_prefernotanswer})



        # ------------------------------------------------------------------------------
        # DOSPERT RISK PERCEPTION SCORE - ALL FORWARD, NO REVERSE

        # SCORES AND QUESTIONS UNANSWERED
        perception = input[riskperception_keys].apply(pd.to_numeric, args=('coerce',))
        perception_leftblank = perception.apply(lambda x: sum(x.isnull().values), axis=1)
        perception_prefernotanswer = perception[perception[riskperception_keys] == nonresp['dospert']].count(axis=1)

        # TOTAL ANSWERS UNANSWERED
        perception_unanswered = perception_leftblank + perception_prefernotanswer

        # Total SCORE
        perception_score = perception[(perception[riskperception_keys] >= 1) &
                                      (perception[riskperception_keys] <= 7)].sum(axis=1)

        perceptionall = pd.DataFrame(
            {'DOSPERT Risk Perception Score': perception_score, 'DOSPERT Risk Perception Left Blank': perception_leftblank,
             'DOSPERT Risk Perception Prefer Not to Answer': perception_prefernotanswer})



        # ------------------------------------------------------------------------------
        # Put the scores into one frame
        frames = [risktakingall, perceptionall]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print("We could not find the DOSPERT headers in your dataset. Please look at the dospert function in this package and put in the correct keys.")