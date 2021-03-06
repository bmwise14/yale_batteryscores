#!/usr/bin/python

"""
Battery Scores Package for Processing Qualtrics CSV Files

@author: Bradley Wise
@email: bradley.wise@yale.edu
@version: 1.1
@date: 2017.01.13
"""

import pandas as pd
import sys

# input = the data you are using with with the keys listed below as headers
# nonresval = the Prefer Not To Answer Choice on your Questionnaire


def neoffi(input, nonresp):
    # Neuroticism-Extroversion-Openness Five Factor Inventory

    # RESOURCES USED:
    """GSP Scales Notebook - Holmes Lab"""
    """http://www.sigmaassessmentsystems.com/assessments/neo-five-factor-inventory-3/"""


    # SCORING:
    """
    1. Raw subscores are computed by summing each subscale. This battery will take your 1-5 range values in Qualtrics
     and replace them with range 0-4. Questions that should be reverse scored are reverse scored.

    2. How to handle missing values is not explicitly mentioned in the primary resources above, so
    if any value is left blank or prefer not to answer, those missing values will be replaced with the average
    score on that particular subscale and then added to the final subscore total (Avram).

    3. These are the minimum and maximum values for each subscale:
                                                        Min     Max
                                            NEO_N       0       48
                                            NEO_E       0       48
                                            NEO_O       0       48
                                            NEO_A       0       48
                                            NEO_C       0       48
    """

    try:
        # STRONGLY DISAGREE - DISAGREE - NEUTRAL - AGREE - STRONGLY AGREE - PREFER NOT TO ANSWER
        #        0               1         2        3          4                   YOUR #
        # ------------------------------------------------------------------------------
        neo_neuroticism_keys = ['neo_6', 'neo_11', 'neo_21', 'neo_26', 'neo_36', 'neo_41', 'neo_51', 'neo_56']
        neo_neuroticism_rev_keys = ['neo_1', 'neo_16', 'neo_31', 'neo_46']
        neo_extroversion_keys = ['neo_2', 'neo_7', 'neo_17', 'neo_22', 'neo_32', 'neo_37', 'neo_47', 'neo_52']
        neo_extroversion_rev_keys = ['neo_12', 'neo_27', 'neo_42', 'neo_57']
        neo_openness_keys = ['neo_13', 'neo_28', 'neo_43', 'neo_53', 'neo_58']
        neo_openness_rev_keys = ['neo_3', 'neo_8', 'neo_18', 'neo_23', 'neo_33', 'neo_38', 'neo_48']
        neo_agreeableness_keys = ['neo_4', 'neo_19', 'neo_34', 'neo_49']
        neo_agreeableness_rev_keys = ['neo_9', 'neo_14', 'neo_24', 'neo_29', 'neo_39', 'neo_44', 'neo_54', 'neo_59']
        neo_conscientiousness_keys = ['neo_5', 'neo_10', 'neo_20', 'neo_25', 'neo_35', 'neo_40', 'neo_50', 'neo_60']
        neo_conscientiousness_rev_keys = ['neo_15', 'neo_30', 'neo_45', 'neo_55']


        # ------------------------------------------------------------------------------
        # NEUROTOCISM SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        neuroticism_forward = input[neo_neuroticism_keys].apply(pd.to_numeric, args=('raise',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])

        # Are there any values that don't fit in the value parameters
        neuroticism_forward_nofit = neuroticism_forward[(neuroticism_forward[neo_neuroticism_keys] != nonresp['neo']) &
                                  (neuroticism_forward[neo_neuroticism_keys] > 4) |
                                  (neuroticism_forward[neo_neuroticism_keys] < 0)].count(axis=1)


        neuroticism_forward_leftblank = neuroticism_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        neuroticism_forward_prefernotanswer = neuroticism_forward[neuroticism_forward[neo_neuroticism_keys] == nonresp['neo']].count(axis=1)

        # sum all the forward scores
        neuroticism_forward_score = neuroticism_forward[(neuroticism_forward[neo_neuroticism_keys] >= 0) &
                                                        (neuroticism_forward[neo_neuroticism_keys] <= 4)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        neuroticism_rev = input[neo_neuroticism_rev_keys].apply(pd.to_numeric, args=('raise',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])

        # Are there any values that don't fit in the value parameters
        neuroticism_rev_nofit = neuroticism_rev[(neuroticism_rev[neo_neuroticism_rev_keys] != nonresp['neo']) &
                                  (neuroticism_rev[neo_neuroticism_rev_keys] > 4) |
                                  (neuroticism_rev[neo_neuroticism_rev_keys] < 0)].count(axis=1)

        # sum the number of reverse questions left blank or preferred not to answer
        neuroticism_reverse_leftblank = neuroticism_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        neuroticism_reverse_prefernotanswer = neuroticism_rev[neuroticism_rev[neo_neuroticism_rev_keys] == nonresp['neo']].count(axis=1)

        # sum all the reverse scores
        neuroticism_rev_score = neuroticism_rev[neuroticism_rev[neo_neuroticism_rev_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

        # Total SCORE
        total_neuroticism_score = neuroticism_forward_score + neuroticism_rev_score

        # TOTAL ANSWERS LEFT BLANK
        total_neuroticism_leftblank = neuroticism_forward_leftblank + neuroticism_reverse_leftblank

        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_neuroticism_prefernotanswer = neuroticism_forward_prefernotanswer + neuroticism_reverse_prefernotanswer

        # TOTAL ANSWERS UNANSWERED
        total_neuroticism_unanswered = total_neuroticism_leftblank + total_neuroticism_prefernotanswer

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        total_neuroticism_score = total_neuroticism_score + (total_neuroticism_unanswered * total_neuroticism_score /
                                                             (len(neo_neuroticism_keys)+len(neo_neuroticism_rev_keys)-total_neuroticism_unanswered))

        neuroall = pd.DataFrame(
            {'NEO_Neurotocism_Score': total_neuroticism_score, 'NEO_Neurotocism_Left_Blank': total_neuroticism_leftblank,
             'NEO_Neurotocism_Prefer_Not_to_Answer': total_neuroticism_prefernotanswer})


        # ------------------------------------------------------------------------------
        # EXTROVERSION SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        extroversion_forward = input[neo_extroversion_keys].apply(pd.to_numeric, args=('raise',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])

        # Are there any values that don't fit in the value parameters
        extroversion_forward_nofit = extroversion_forward[(extroversion_forward[neo_extroversion_keys] != nonresp['neo']) &
                                  (extroversion_forward[neo_extroversion_keys] > 4) |
                                  (extroversion_forward[neo_extroversion_keys] < 0)].count(axis=1)

        extroversion_forward_leftblank = extroversion_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        extroversion_forward_prefernotanswer = extroversion_forward[extroversion_forward[neo_extroversion_keys] == nonresp['neo']].count(axis=1)

        # sum all the forward scores
        extroversion_forward_score = extroversion_forward[(extroversion_forward[neo_extroversion_keys] >= 0) &
                                                          (extroversion_forward[neo_extroversion_keys] <= 4)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        extroversion_rev = input[neo_extroversion_rev_keys].apply(pd.to_numeric, args=('raise',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])

        # Are there any values that don't fit in the value parameters
        extroversion_rev_nofit = extroversion_rev[(extroversion_rev[neo_extroversion_rev_keys] != nonresp['neo']) &
                                  (extroversion_rev[neo_extroversion_rev_keys] > 4) |
                                  (extroversion_rev[neo_extroversion_rev_keys] < 0)].count(axis=1)

        # sum the number of reverse questions left blank or preferred not to answer
        extroversion_reverse_leftblank = extroversion_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        extroversion_reverse_prefernotanswer = extroversion_rev[extroversion_rev[neo_extroversion_rev_keys] == nonresp['neo']].count(axis=1)

        # sum all the reverse scores
        extroversion_rev_score = extroversion_rev[extroversion_rev[neo_extroversion_rev_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

        # Total SCORE
        total_extroversion_score = extroversion_forward_score + extroversion_rev_score

        # TOTAL ANSWERS LEFT BLANK
        total_extroversion_leftblank = extroversion_forward_leftblank + extroversion_reverse_leftblank

        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_extroversion_prefernotanswer = extroversion_forward_prefernotanswer + extroversion_reverse_prefernotanswer

        # TOTAL ANSWERS UNANSWERED
        total_extroversion_unanswered = total_extroversion_leftblank + total_extroversion_prefernotanswer


        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        total_extroversion_score = total_extroversion_score + (total_extroversion_unanswered * total_extroversion_score /
                                                               (len(neo_extroversion_keys)+len(neo_extroversion_rev_keys)-total_extroversion_unanswered))

        extroversall = pd.DataFrame(
            {'NEO_Extroversion_Score': total_extroversion_score, 'NEO_Extroversion_Left_Blank': total_extroversion_leftblank,
             'NEO_Extroversion_Prefer_Not_to_Answer': total_extroversion_prefernotanswer})



        # ------------------------------------------------------------------------------
        # OPENNESS SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        openness_forward = input[neo_openness_keys].apply(pd.to_numeric, args=('raise',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])

        # Are there any values that don't fit in the value parameters
        openness_forward_nofit = openness_forward[(openness_forward[neo_openness_keys] != nonresp['neo']) &
                                  (openness_forward[neo_openness_keys] > 4) |
                                  (openness_forward[neo_openness_keys] < 0)].count(axis=1)

        openness_forward_leftblank = openness_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        openness_forward_prefernotanswer = openness_forward[openness_forward[neo_openness_keys] == nonresp['neo']].count(axis=1)

        # sum all the forward scores
        openness_forward_score = openness_forward[(openness_forward[neo_openness_keys] >= 0) &
                                                  (openness_forward[neo_openness_keys] <= 4)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        openness_rev = input[neo_openness_rev_keys].apply(pd.to_numeric, args=('raise',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])

        # Are there any values that don't fit in the value parameters
        openness_rev_nofit = openness_rev[(openness_rev[neo_openness_rev_keys] != nonresp['neo']) &
                                  (openness_rev[neo_openness_rev_keys] > 4) |
                                  (openness_rev[neo_openness_rev_keys] < 0)].count(axis=1)

        # sum the number of reverse questions left blank or preferred not to answer
        openness_reverse_leftblank = openness_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        openness_reverse_prefernotanswer = openness_rev[openness_rev[neo_openness_rev_keys] == nonresp['neo']].count(axis=1)

        # sum all the reverse scores
        openness_rev_score = openness_rev[openness_rev[neo_openness_rev_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

        # Total SCORE
        total_openness_score = openness_forward_score + openness_rev_score

        # TOTAL ANSWERS LEFT BLANK
        total_openness_leftblank = openness_forward_leftblank + openness_reverse_leftblank

        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_openness_prefernotanswer = openness_forward_prefernotanswer + openness_reverse_prefernotanswer

        # TOTAL ANSWERS UNANSWERED
        total_openness_unanswered = total_openness_leftblank + total_openness_prefernotanswer


        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        total_openness_score = total_openness_score + (total_openness_unanswered * total_openness_score /
                                                       (len(neo_openness_keys)+len(neo_openness_rev_keys)-total_openness_unanswered))

        opennessall = pd.DataFrame(
            {'NEO_Openness_Score': total_openness_score, 'NEO_Openness_Left_Blank': total_openness_leftblank,
             'NEO_Openness_Prefer_Not_to_Answer': total_openness_prefernotanswer})



        # ------------------------------------------------------------------------------
        # AGREEABLENESS SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        agree_forward = input[neo_agreeableness_keys].apply(pd.to_numeric, args=('raise',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])

        # Are there any values that don't fit in the value parameters
        agree_forward_nofit = agree_forward[(agree_forward[neo_agreeableness_keys] != nonresp['neo']) &
                                  (agree_forward[neo_agreeableness_keys] > 4) |
                                  (agree_forward[neo_agreeableness_keys] < 0)].count(axis=1)

        agree_forward_leftblank = agree_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        agree_forward_prefernotanswer = agree_forward[agree_forward[neo_agreeableness_keys] == nonresp['neo']].count(axis=1)

        # sum all the forward scores
        agree_forward_score = agree_forward[(agree_forward[neo_agreeableness_keys] >= 0) &
                                            (agree_forward[neo_agreeableness_keys] <= 4)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        agree_rev = input[neo_agreeableness_rev_keys].apply(pd.to_numeric, args=('raise',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])

        # Are there any values that don't fit in the value parameters
        agree_rev_nofit = agree_rev[(agree_rev[neo_agreeableness_rev_keys] != nonresp['neo']) &
                                  (agree_rev[neo_agreeableness_rev_keys] > 4) |
                                  (agree_rev[neo_agreeableness_rev_keys] < 0)].count(axis=1)

        # sum the number of reverse questions left blank or preferred not to answer
        agree_reverse_leftblank = agree_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        agree_reverse_prefernotanswer = agree_rev[agree_rev[neo_agreeableness_rev_keys] == nonresp['neo']].count(axis=1)

        # sum all the reverse scores
        agree_rev_score = agree_rev[agree_rev[neo_agreeableness_rev_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

        # Total SCORE
        total_agree_score = agree_forward_score + agree_rev_score

        # TOTAL ANSWERS LEFT BLANK
        total_agree_leftblank = agree_forward_leftblank + agree_reverse_leftblank

        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_agree_prefernotanswer = agree_forward_prefernotanswer + agree_reverse_prefernotanswer

        # TOTAL ANSWERS UNANSWERED
        total_agree_unanswered = total_agree_leftblank + total_agree_prefernotanswer


        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        total_agree_score = total_agree_score + (total_agree_unanswered * total_agree_score /
                                                 (len(neo_agreeableness_keys)+len(neo_agreeableness_rev_keys)-total_agree_unanswered))

        agreeall = pd.DataFrame(
            {'NEO_Agreeableness_Score': total_agree_score, 'NEO_Agreeableness_Left_Blank': total_agree_leftblank,
             'NEO_Agreeableness_Prefer_Not_to_Answer': total_agree_prefernotanswer})



        # ------------------------------------------------------------------------------
        # CONSCIENTIOUSNESS SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        conscien_forward = input[neo_conscientiousness_keys].apply(pd.to_numeric, args=('raise',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])

        # Are there any values that don't fit in the value parameters
        conscien_forward_nofit = conscien_forward[(conscien_forward[neo_conscientiousness_keys] != nonresp['neo']) &
                                  (conscien_forward[neo_conscientiousness_keys] > 4) |
                                  (conscien_forward[neo_conscientiousness_keys] < 0)].count(axis=1)

        conscien_forward_leftblank = conscien_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        conscien_forward_prefernotanswer = conscien_forward[conscien_forward[neo_conscientiousness_keys] == nonresp['neo']].count(axis=1)

        # sum all the forward scores
        conscien_forward_score = conscien_forward[(conscien_forward[neo_conscientiousness_keys] >= 0) &
                                                  (conscien_forward[neo_conscientiousness_keys] <= 4)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        conscien_rev = input[neo_conscientiousness_rev_keys].apply(pd.to_numeric, args=('raise',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])

        # Are there any values that don't fit in the value parameters
        conscien_rev_nofit = conscien_rev[(conscien_rev[neo_conscientiousness_rev_keys] != nonresp['neo']) &
                                  (conscien_rev[neo_conscientiousness_rev_keys] > 4) |
                                  (conscien_rev[neo_conscientiousness_rev_keys] < 0)].count(axis=1)

        # sum the number of reverse questions left blank or preferred not to answer
        conscien_reverse_leftblank = conscien_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        conscien_reverse_prefernotanswer = conscien_rev[conscien_rev[neo_conscientiousness_rev_keys] == nonresp['neo']].count(axis=1)

        # sum all the reverse scores
        conscien_rev_score = conscien_rev[conscien_rev[neo_conscientiousness_rev_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

        # Total SCORE
        total_conscien_score = conscien_forward_score + conscien_rev_score

        # TOTAL ANSWERS LEFT BLANK
        total_conscien_leftblank = conscien_forward_leftblank + conscien_reverse_leftblank

        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_conscien_prefernotanswer = conscien_forward_prefernotanswer + conscien_reverse_prefernotanswer

        # TOTAL ANSWERS UNANSWERED
        total_conscien_unanswered = total_conscien_leftblank + total_conscien_prefernotanswer


        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the (total number of questions in the subscale - number of unanswered questions).
        # Add all of this to to the original score.
        total_conscien_score = total_conscien_score + (total_conscien_unanswered * total_conscien_score /
                                                       (len(neo_conscientiousness_keys)+len(neo_conscientiousness_rev_keys)-total_conscien_unanswered))


        conscienall = pd.DataFrame(
            {'NEO_Conscientiousness_Score': total_conscien_score, 'NEO_Conscientiousness_Left_Blank': total_conscien_leftblank,
             'NEO_Conscientiousness_Prefer_Not_to_Answer': total_conscien_prefernotanswer})


        # ------------------------------------------------------------------------------
        # Count the number of values that do not fit parameter values
        nofit = neuroticism_forward_nofit + neuroticism_rev_nofit + extroversion_forward_nofit + extroversion_rev_nofit + \
                openness_forward_nofit + openness_rev_nofit + agree_forward_nofit + agree_rev_nofit + conscien_forward_nofit + \
                conscien_rev_nofit

        # If there are any values that do not fit parameters, exit the code and make client find the values that did not work
        for x in nofit:
            if x >= 1:
                sys.exit("We found values that don't match parameter values for calculation in your NEOFFI dataset. "
                         "Please make sure your values range from 1-5 (see neoffi script) and have only ONE prefer not to answer value.")


        # ------------------------------------------------------------------------------
        # Put all the scores into one frame
        frames = [neuroall, extroversall, opennessall, agreeall, conscienall]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print("We could not find the NEOFFI headers in your dataset. Please look at the neoffi function in this package and put in the correct keys.")
    except TypeError:
        print("You need (1) the dataframe and (2) a numeric NEOFFI 'Prefer Not To Answer' choice (or stored variable) in your function arguments.")
    except ValueError:
        print("We found strings in your NEOFFI dataset. Please make sure there are no strings/letters in your dataset. "
              "Otherwise, we cannot calculate the score correctly.")