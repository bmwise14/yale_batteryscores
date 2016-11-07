#!/usr/bin/python

import pandas as pd

# input = the data you are using with with the keys listed below as headers
# nonresval = the Prefer Not To Answer Choice on your Questionnaire


def neoffi(input, nonresp):
    # Neuroticism-Extroversion-Openness Five Factor Inventory

    # RESOURCES USED:
    """GSP Scales Notebook - Holmes Lab"""
    """http://www.sigmaassessmentsystems.com/assessments/neo-five-factor-inventory-3/"""


    # SCORING:
    """
    1. Raw subscores are computed by summing each subscale. This scale replaces your Qualtrics Scale with the Scale below.
       Questions that should be reverse scored are reverse scored.

    2. Any Prefer Not To Answer selection was not counted toward final score.

    3. Any Question left blank was not counted toward the subscale or final score.
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
        neuroticism_forward = input[neo_neuroticism_keys].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])


        neuroticism_forward_leftblank = neuroticism_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        neuroticism_forward_prefernotanswer = neuroticism_forward[neuroticism_forward[neo_neuroticism_keys] == nonresp['neo']].count(axis=1)
        neuroticism_forward_unanswered = neuroticism_forward_leftblank + neuroticism_forward_prefernotanswer

        # sum all the forward scores
        neuroticism_forward_score = neuroticism_forward[(neuroticism_forward[neo_neuroticism_keys] >= 0) &
                                                        (neuroticism_forward[neo_neuroticism_keys] <= 4)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        neuroticism_rev = input[neo_neuroticism_rev_keys].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])

        # sum the number of reverse questions left blank or preferred not to answer
        neuroticism_reverse_leftblank = neuroticism_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        neuroticism_reverse_prefernotanswer = neuroticism_rev[neuroticism_rev[neo_neuroticism_rev_keys] == nonresp['neo']].count(axis=1)
        neuroticism_reverse_unanswered = neuroticism_reverse_leftblank + neuroticism_reverse_prefernotanswer

        # sum all the reverse scores
        neuroticism_rev_score = neuroticism_rev[neuroticism_rev[neo_neuroticism_rev_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

        # Total SCORE
        total_neuroticism_score = neuroticism_forward_score + neuroticism_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_neuroticism_unanswered = neuroticism_forward_unanswered + neuroticism_reverse_unanswered

        # TOTAL ANSWERS LEFT BLANK
        total_neuroticism_leftblank = neuroticism_forward_leftblank + neuroticism_reverse_leftblank

        neurodropit = ['DISCARD' if x > 2 else 'KEEP' for x in total_neuroticism_leftblank]

        neurodrop = pd.DataFrame({'Drop_Neurotocism_Score': neurodropit})
        neurodrop.index+=1


        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_neuroticism_prefernotanswer = neuroticism_forward_prefernotanswer + neuroticism_reverse_prefernotanswer


        neuroall = pd.DataFrame(
            {'NEO_Neurotocism_Score': total_neuroticism_score, 'NEO_Neurotocism_Left_Blank': total_neuroticism_leftblank,
             'NEO_Neurotocism_Prefer_Not_to_Answer': total_neuroticism_prefernotanswer})


        # ------------------------------------------------------------------------------
        # EXTROVERSION SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        extroversion_forward = input[neo_extroversion_keys].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])
        extroversion_forward_leftblank = extroversion_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        extroversion_forward_prefernotanswer = extroversion_forward[extroversion_forward[neo_extroversion_keys] == nonresp['neo']].count(axis=1)
        extroversion_forward_unanswered = extroversion_forward_leftblank + extroversion_forward_prefernotanswer

        # sum all the forward scores
        extroversion_forward_score = extroversion_forward[(extroversion_forward[neo_extroversion_keys] >= 0) &
                                                          (extroversion_forward[neo_extroversion_keys] <= 4)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        extroversion_rev = input[neo_extroversion_rev_keys].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])

        # sum the number of reverse questions left blank or preferred not to answer
        extroversion_reverse_leftblank = extroversion_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        extroversion_reverse_prefernotanswer = extroversion_rev[extroversion_rev[neo_extroversion_rev_keys] == nonresp['neo']].count(axis=1)
        extroversion_reverse_unanswered = extroversion_reverse_leftblank + extroversion_reverse_prefernotanswer

        # sum all the reverse scores
        extroversion_rev_score = extroversion_rev[extroversion_rev[neo_extroversion_rev_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

        # Total SCORE
        total_extroversion_score = extroversion_forward_score + extroversion_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_extroversion_unanswered = extroversion_forward_unanswered + extroversion_reverse_unanswered

        # TOTAL ANSWERS LEFT BLANK
        total_extroversion_leftblank = extroversion_forward_leftblank + extroversion_reverse_leftblank

        extrodropit = ['DISCARD' if x > 2 else 'KEEP' for x in total_extroversion_leftblank]

        extrodrop = pd.DataFrame({'Drop_Extroversion_Score': extrodropit})
        extrodrop.index+=1



        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_extroversion_prefernotanswer = extroversion_forward_prefernotanswer + extroversion_reverse_prefernotanswer


        extroversall = pd.DataFrame(
            {'NEO_Extroversion_Score': total_extroversion_score, 'NEO_Extroversion_Left_Blank': total_extroversion_leftblank,
             'NEO_Extroversion_Prefer_Not_to_Answer': total_extroversion_prefernotanswer})



        # ------------------------------------------------------------------------------
        # OPENNESS SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        openness_forward = input[neo_openness_keys].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])
        openness_forward_leftblank = openness_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        openness_forward_prefernotanswer = openness_forward[openness_forward[neo_openness_keys] == nonresp['neo']].count(axis=1)
        openness_forward_unanswered = openness_forward_leftblank + openness_forward_prefernotanswer

        # sum all the forward scores
        openness_forward_score = openness_forward[(openness_forward[neo_openness_keys] >= 0) &
                                                  (openness_forward[neo_openness_keys] <= 4)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        openness_rev = input[neo_openness_rev_keys].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])

        # sum the number of reverse questions left blank or preferred not to answer
        openness_reverse_leftblank = openness_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        openness_reverse_prefernotanswer = openness_rev[openness_rev[neo_openness_rev_keys] == nonresp['neo']].count(axis=1)
        openness_reverse_unanswered = openness_reverse_leftblank + openness_reverse_prefernotanswer

        # sum all the reverse scores
        openness_rev_score = openness_rev[openness_rev[neo_openness_rev_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

        # Total SCORE
        total_openness_score = openness_forward_score + openness_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_openness_unanswered = openness_forward_unanswered + openness_reverse_unanswered

        # TOTAL ANSWERS LEFT BLANK
        total_openness_leftblank = openness_forward_leftblank + openness_reverse_leftblank
        opendropit = ['DISCARD' if x > 2 else 'KEEP' for x in total_openness_leftblank]

        opendrop = pd.DataFrame({'Drop_Openness_Score': opendropit})
        opendrop.index+=1


        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_openness_prefernotanswer = openness_forward_prefernotanswer + openness_reverse_prefernotanswer


        opennessall = pd.DataFrame(
            {'NEO_Openness_Score': total_openness_score, 'NEO_Openness_Left_Blank': total_openness_leftblank,
             'NEO_Openness_Prefer_Not_to_Answer': total_openness_prefernotanswer})



        # ------------------------------------------------------------------------------
        # AGREEABLENESS SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        agree_forward = input[neo_agreeableness_keys].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])
        agree_forward_leftblank = agree_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        agree_forward_prefernotanswer = agree_forward[agree_forward[neo_agreeableness_keys] == nonresp['neo']].count(axis=1)
        agree_forward_unanswered = agree_forward_leftblank + agree_forward_prefernotanswer

        # sum all the forward scores
        agree_forward_score = agree_forward[(agree_forward[neo_agreeableness_keys] >= 0) &
                                            (agree_forward[neo_agreeableness_keys] <= 4)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        agree_rev = input[neo_agreeableness_rev_keys].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])

        # sum the number of reverse questions left blank or preferred not to answer
        agree_reverse_leftblank = agree_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        agree_reverse_prefernotanswer = agree_rev[agree_rev[neo_agreeableness_rev_keys] == nonresp['neo']].count(axis=1)
        agree_reverse_unanswered = agree_reverse_leftblank + agree_reverse_prefernotanswer

        # sum all the reverse scores
        agree_rev_score = agree_rev[agree_rev[neo_agreeableness_rev_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

        # Total SCORE
        total_agree_score = agree_forward_score + agree_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_agree_unanswered = agree_forward_unanswered + agree_reverse_unanswered

        # TOTAL ANSWERS LEFT BLANK
        total_agree_leftblank = agree_forward_leftblank + agree_reverse_leftblank
        agreedropit = ['DISCARD' if x > 2 else 'KEEP' for x in total_agree_leftblank]

        agreedrop = pd.DataFrame({'Drop_Agreeableness_Score': agreedropit})
        agreedrop.index+=1


        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_agree_prefernotanswer = agree_forward_prefernotanswer + agree_reverse_prefernotanswer

        agreeall = pd.DataFrame(
            {'NEO_Agreeableness_Score': total_agree_score, 'NEO_Agreeableness_Left_Blank': total_agree_leftblank,
             'NEO_Agreeableness_Prefer_Not_to_Answer': total_agree_prefernotanswer})



        # ------------------------------------------------------------------------------
        # CONSCIENTIOUSNESS SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        conscien_forward = input[neo_conscientiousness_keys].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])
        conscien_forward_leftblank = conscien_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        conscien_forward_prefernotanswer = conscien_forward[conscien_forward[neo_conscientiousness_keys] == nonresp['neo']].count(axis=1)
        conscien_forward_unanswered = conscien_forward_leftblank + conscien_forward_prefernotanswer

        # sum all the forward scores
        conscien_forward_score = conscien_forward[(conscien_forward[neo_conscientiousness_keys] >= 0) &
                                                  (conscien_forward[neo_conscientiousness_keys] <= 4)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        conscien_rev = input[neo_conscientiousness_rev_keys].apply(pd.to_numeric, args=('coerce',)).replace(to_replace=[1, 2, 3, 4, 5], value=[0, 1, 2, 3, 4])

        # sum the number of reverse questions left blank or preferred not to answer
        conscien_reverse_leftblank = conscien_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        conscien_reverse_prefernotanswer = conscien_rev[conscien_rev[neo_conscientiousness_rev_keys] == nonresp['neo']].count(axis=1)
        conscien_reverse_unanswered = conscien_reverse_leftblank + conscien_reverse_prefernotanswer

        # sum all the reverse scores
        conscien_rev_score = conscien_rev[conscien_rev[neo_conscientiousness_rev_keys] <= 4].rsub(4).sum(axis=1, skipna=True)

        # Total SCORE
        total_conscien_score = conscien_forward_score + conscien_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_conscien_unanswered = conscien_forward_unanswered + conscien_reverse_unanswered


        # TOTAL ANSWERS LEFT BLANK
        total_conscien_leftblank = conscien_forward_leftblank + conscien_reverse_leftblank
        condropit = ['DISCARD' if x > 2 else 'KEEP' for x in total_conscien_leftblank]

        consciendrop = pd.DataFrame({'Drop_Conscientousness_Score': condropit})
        consciendrop.index+=1

        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_conscien_prefernotanswer = conscien_forward_prefernotanswer + conscien_reverse_prefernotanswer

        conscienall = pd.DataFrame(
            {'NEO_Conscientousness_Score': total_conscien_score, 'NEO_Conscientousness_Left_Blank': total_conscien_leftblank,
             'NEO_Conscientousness_Prefer_Not_to_Answer': total_conscien_prefernotanswer})


        # ------------------------------------------------------------------------------
        # Put all the scores into one frame
        frames = [neuroall, extroversall, opennessall, agreeall, conscienall, neurodrop, consciendrop]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print("We could not find the NEOFFI headers in your dataset. Please look at the neoffi function in this package and put in the correct keys.")