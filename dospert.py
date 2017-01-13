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


def dospert(input, nonresp):
    # DOMAIN-SPECIFIC RISK-TAKING SCALE

    # RESOURCES USED:
    """GSP Scales Notebook - Holmes Lab"""
    """http://onlinelibrary.wiley.com/doi/10.1002/bdm.414/epdf"""
    """http://journal.sjdm.org/jdm06005.pdf"""

    # SCORING:
    """
    1. Scores are the sum of each subscale (Risk-Taking and Risk-Perception).
    This one uses the 40-item scale, not the 2006 revised version (Blais & Weber, 2006).

    2. If any value is left blank or prefer not to answer, those missing values will be replaced with the average
    score on that particular subscale and then added to the final subscore total (Blais & Weber, 2006).

    3. If the score is below a minimum value range or above a maximum value range for the subscale, it will be discarded.
                                                        Min     Max
                                    DOSPERT_taking      40      280
                                    DOSPERT_perception  40      280
    """

    try:
        # RISK TAKING MODULE
        # EXTREMELY UNLIKELY - MODERATELY UNLIKELY - SOMEWHAT UNLIKELY - NOT SURE - SOMEWHAT LIKELY - MODERATELY LIKELY - EXTREMELY LIKELY - PREFER NOT TO ANSWER
        #           1                   2                   3               4             5                    6               7                     YOUR #
        # RISK PERCEPTION MODULE
        # NOT AT ALL RISKY - SLIGHTLY RISKY - SOMEWHAT RISKY - MODERATELY RISKY - RISKY - VERY RISKY - EXTREMELY RISKY - PREFER NOT TO ANSWER
        #           1              2                3                  4            5          6            7                   YOUR #
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
        risktaking = input[risktaking_keys].apply(pd.to_numeric, args=('raise',))

        # Are there any values that don't fit in the value parameters
        risktaking_nofit = risktaking[(risktaking[risktaking_keys] != nonresp['dospert']) &
                                  (risktaking[risktaking_keys] > 7) |
                                  (risktaking[risktaking_keys] < 1)].count(axis=1)

        risktaking_leftblank = risktaking.apply(lambda x: sum(x.isnull().values), axis=1)
        risktaking_prefernotanswer = risktaking[risktaking[risktaking_keys] == nonresp['dospert']].count(axis=1)

        # TOTAL ANSWERS UNANSWERED
        risktaking_unanswered = risktaking_leftblank + risktaking_prefernotanswer

        # Total SCORE
        risktaking_score = risktaking[(risktaking[risktaking_keys] >= 1) &
                                      (risktaking[risktaking_keys] <= 7)].sum(axis=1)

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        risktaking_score = (risktaking_score + (risktaking_unanswered * risktaking_score / (len(risktaking_keys)-risktaking_unanswered)))


        # Discard any value below 40 and above 280
        # risktaking_score = ['Discard' if x < 40 else 'Discard' if x > 280 else x for x in risktaking_score]

        risktakingall = pd.DataFrame(
            {'DOSPERT Risktaking Score': risktaking_score, 'DOSPERT Risktaking Left Blank': risktaking_leftblank,
             'DOSPERT Risktaking Prefer Not to Answer': risktaking_prefernotanswer})



        # ------------------------------------------------------------------------------
        # DOSPERT RISK PERCEPTION SCORE - ALL FORWARD, NO REVERSE

        # SCORES AND QUESTIONS UNANSWERED
        perception = input[riskperception_keys].apply(pd.to_numeric, args=('raise',))

        # Are there any values that don't fit in the value parameters
        perception_nofit = perception[(perception[riskperception_keys] != nonresp['dospert']) &
                                  (perception[riskperception_keys] > 7) |
                                  (perception[riskperception_keys] < 1)].count(axis=1)

        perception_leftblank = perception.apply(lambda x: sum(x.isnull().values), axis=1)
        perception_prefernotanswer = perception[perception[riskperception_keys] == nonresp['dospert']].count(axis=1)

        # TOTAL ANSWERS UNANSWERED
        perception_unanswered = perception_leftblank + perception_prefernotanswer

        # Total SCORE
        perception_score = perception[(perception[riskperception_keys] >= 1) &
                                      (perception[riskperception_keys] <= 7)].sum(axis=1)

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        perception_score = (perception_score + (perception_unanswered * perception_score / (len(riskperception_keys)-perception_unanswered)))

        perceptionall = pd.DataFrame(
            {'DOSPERT Risk Perception Score': perception_score, 'DOSPERT Risk Perception Left Blank': perception_leftblank,
             'DOSPERT Risk Perception Prefer Not to Answer': perception_prefernotanswer})

        # ------------------------------------------------------------------------------
        # Count the number of values that do not fit parameter values
        nofit = risktaking_nofit + perception_nofit
        # If there are any values that do not fit parameters, exit the code and make client find the values that did not work
        for x in nofit:
            if x >= 1:
                sys.exit("We found values that don't match parameter values for calculation in your DOSPERT dataset. "
                         "Please make sure your values range from 1-7 (see dospert script) and have only ONE prefer not to answer value.")


        # ------------------------------------------------------------------------------
        # Put the scores into one frame
        frames = [risktakingall, perceptionall]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print("We could not find the DOSPERT headers in your dataset. Please look at the dospert function in this package and put in the correct keys.")
    except ValueError:
        print("We found strings in your DOSPERT dataset. Please make sure there are no strings/letters in your input. Otherwise, we can't do our thang.")