#!/usr/bin/python

import pandas as pd

# input = the data you are using with with the keys listed below as headers
# nonresval = the Prefer Not To Answer Choice on your Questionnaire


def tci(input, nonresp):
    # TEMPERAMENT AND CHARACTER INVENTORY - REVISED - 140 SCORING KEY

    # RESOURCES USED:
    """GSP Scales - Holmes Lab"""

    """http://psycnet.apa.org/journals/jpa/27/2/73.pdf"""
    """https://www.ncbi.nlm.nih.gov/pmc/articles/PMC2810834/#R14"""

    # SCORING:
    """
    1. Typically Scores from 1-5 with no prefer not to answer choice. This qualtrics data scores with range from 1-6.

    2. Scores are the sum of each subscale. Questions that should be reverse scored are reverse scored.

    3. There are 4 validity items on TCI-140. For participants who missed 3 or more check questions, scores were discarded (Zohar and Cloninger, 2011).

    4. How to handle missing values is not explicitly mentioned in the primary resources above, so
    if any value is left blank or prefer not to answer, those missing values will be replaced with the average
    score on that particular subscale and then added to the final subscore total (Avram).

    5. If the score is below a minimum value range or above a maximum value range for the subscale, it will be discarded.
                                                        Min     Max
                                        TCI_Novel       20      100
                                        TCI_HarmAvoid   20      100
                                        TCI_RewDep      20      100
                                        TCI_Pers        20      100
                                        TCI_SelfDir     20      100
                                        TCI_Coop        20      100
                                        TCI_SelfTran    16      80
    """

    try:
        # DEFINITELY FALSE - MOSTLY OR PROBABLY FALSE - NEITHER TRUE NOR FALSE, OR ABOUT EQUALLY TRUE OR FALSE
        #        1                    2                                         3
        #
        # MOSTLY OR PROBABLY TRUE - DEFINITELY TRUE - PREFER NOT TO ANSWER
        #         4                     5                   6
        # ------------------------------------------------------------------------------
        tci_novelty_keys = ['tci_1', 'tci_10', 'tci_24', 'tci_44', 'tci_51', 'tci_59', 'tci_71', 'tci_102', 'tci_104',
                            'tci_109', 'tci_122', 'tci_135']
        tci_novelty_rev_keys = ['tci_14', 'tci_47', 'tci_53', 'tci_63', 'tci_77', 'tci_105', 'tci_123', 'tci_139']


        tci_harmavoidance_keys = ['tci_9', 'tci_16', 'tci_19', 'tci_30', 'tci_46', 'tci_70', 'tci_82', 'tci_113', 'tci_136']
        tci_harmavoidance_rev_keys = ['tci_2', 'tci_38', 'tci_61', 'tci_64', 'tci_78', 'tci_81',
                                      'tci_86', 'tci_98', 'tci_103', 'tci_121', 'tci_131']


        tci_rewarddependence_keys = ['tci_15', 'tci_20', 'tci_31', 'tci_54', 'tci_80', 'tci_97', 'tci_116', 'tci_125', 'tci_130']
        tci_rewarddependence_rev_keys = ['tci_11', 'tci_26', 'tci_39', 'tci_65', 'tci_79', 'tci_85', 'tci_92', 'tci_96',
                                         'tci_110', 'tci_127', 'tci_138']


        tci_persistence_keys = ['tci_5', 'tci_8', 'tci_22', 'tci_37', 'tci_45', 'tci_55', 'tci_60', 'tci_62', 'tci_72',
                                'tci_76', 'tci_94', 'tci_111', 'tci_114', 'tci_117', 'tci_119', 'tci_126', 'tci_137']
        tci_persistence_rev_keys = ['tci_129', 'tci_134', 'tci_140']


        tci_selfdirectedness_keys = ['tci_35', 'tci_57']
        tci_selfdirectedness_rev_keys = ['tci_3', 'tci_6', 'tci_17', 'tci_21', 'tci_23', 'tci_34', 'tci_48', 'tci_49', 'tci_58',
                                         'tci_66', 'tci_69', 'tci_83', 'tci_87', 'tci_90', 'tci_100', 'tci_107', 'tci_108', 'tci_115']


        tci_cooperativeness_keys = ['tci_4', 'tci_7', 'tci_40', 'tci_41', 'tci_50', 'tci_74', 'tci_89']
        tci_cooperativeness_rev_keys = ['tci_13','tci_18', 'tci_27', 'tci_28', 'tci_33', 'tci_67', 'tci_75', 'tci_84',
                                        'tci_88', 'tci_93', 'tci_124', 'tci_128', 'tci_133']


        tci_selftranscendence_keys = ['tci_12', 'tci_25', 'tci_29', 'tci_42', 'tci_43', 'tci_52', 'tci_56', 'tci_68', 'tci_73',
                                      'tci_91', 'tci_95', 'tci_99', 'tci_106', 'tci_112', 'tci_118']
        tci_selftranscendence_rev_keys = ['tci_32']

        validity1 = ['tci_36']
        validity2 = ['tci_101']
        validity3 = ['tci_120']
        validity4 = ['tci_132']



        # ------------------------------------------------------------------------------
        # CHECK QUESTIONS
        # If a participant consistently selects the wrong check choice, it probably means they weren't paying attention
        # At what point should one drop the score?


        check1 = input[validity1].apply(pd.to_numeric, args=('coerce',))
        check1_wrong = check1[check1[validity1] != 4].count(axis=1)
        check1_null = check1.apply(lambda x: sum(x.isnull().values), axis=1)

        check2 = input[validity2].apply(pd.to_numeric, args=('coerce',))
        check2_wrong = check2[check2[validity2] != 1].count(axis=1)
        check2_null = check2.apply(lambda x: sum(x.isnull().values), axis=1)

        check3 = input[validity3].apply(pd.to_numeric, args=('coerce',))
        check3_wrong = check3[check3[validity3] != nonresp['tci']].count(axis=1)
        check3_null = check3.apply(lambda x: sum(x.isnull().values), axis=1)

        check4 = input[validity4].apply(pd.to_numeric, args=('coerce',))
        check4_wrong = check4[check4[validity4] != 2].count(axis=1)
        check4_null = check4.apply(lambda x: sum(x.isnull().values), axis=1)

        tot_check_wrong = check1_wrong + check2_wrong + check3_wrong + check4_wrong + check1_null + check2_null + check3_null + check4_null

        # tot_check_wrong = ['Missed > 2' if x > 2 else x for x in tot_check_wrong]


        checks = pd.DataFrame(
            {'Check_Questions_Answered_Wrong': tot_check_wrong})
        # checks.index +=1

        # ------------------------------------------------------------------------------
        # NOVELTY SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        novelty_forward = input[tci_novelty_keys].apply(pd.to_numeric, args=('coerce',))
        novelty_forward_leftblank = novelty_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        novelty_forward_prefernotanswer = novelty_forward[novelty_forward[tci_novelty_keys] == nonresp['tci']].count(axis=1)
        novelty_forward_unanswered = novelty_forward_leftblank + novelty_forward_prefernotanswer

        # sum all the forward scores
        novelty_forward_score = novelty_forward[(novelty_forward[tci_novelty_keys] >= 1) &
                                                (novelty_forward[tci_novelty_keys] <= 5)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        novelty_rev = input[tci_novelty_rev_keys].apply(pd.to_numeric, args=('coerce',))

        # sum the number of reverse questions left blank or preferred not to answer
        novelty_reverse_leftblank = novelty_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        novelty_reverse_prefernotanswer = novelty_rev[novelty_rev[tci_novelty_rev_keys] == nonresp['tci']].count(axis=1)
        novelty_reverse_unanswered = novelty_reverse_leftblank + novelty_reverse_prefernotanswer

        # sum all the reverse scores
        novelty_rev_score = novelty_rev[novelty_rev[tci_novelty_rev_keys] <= 5].rsub(6).sum(axis=1, skipna=True)

        # Total SCORE
        total_novelty_score = novelty_forward_score + novelty_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_novelty_unanswered = novelty_forward_unanswered + novelty_reverse_unanswered

        # TOTAL ANSWERS LEFT BLANK
        total_novelty_leftblank = novelty_forward_leftblank + novelty_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_novelty_prefernotanswer = novelty_forward_prefernotanswer + novelty_reverse_prefernotanswer

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the total number of questions in the subscale.
        # Add all of this to to the original drive score.
        total_novelty_score = total_novelty_score + (total_novelty_unanswered * total_novelty_score / (len(tci_novelty_keys) + len(tci_novelty_rev_keys)))

        # Discard any value below 20 and above 80
        # total_novelty_score = ['Discard (<20)' if x < 20 else 'Discard (>80)' if x > 80 else x for x in total_novelty_score]


        noveltyall = pd.DataFrame(
            {'TCI_Novelty_Score': total_novelty_score, 'TCI_Novelty_Left_Blank': total_novelty_leftblank,
             'TCI_Novelty_Prefer_Not_to_Answer': total_novelty_prefernotanswer})




        # ------------------------------------------------------------------------------
        # HARM AVOIDANCE SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        harmavoidance_forward = input[tci_harmavoidance_keys].apply(pd.to_numeric, args=('coerce',))
        harmavoidance_forward_leftblank = harmavoidance_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        harmavoidance_forward_prefernotanswer = harmavoidance_forward[harmavoidance_forward[tci_harmavoidance_keys] == nonresp['tci']].count(axis=1)
        harmavoidance_forward_unanswered = harmavoidance_forward_leftblank + harmavoidance_forward_prefernotanswer

        # sum all the forward scores
        harmavoidance_forward_score = harmavoidance_forward[(harmavoidance_forward[tci_harmavoidance_keys] >= 1) &
                                                            (harmavoidance_forward[tci_harmavoidance_keys] <= 5)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        harmavoidance_rev = input[tci_harmavoidance_rev_keys].apply(pd.to_numeric, args=('coerce',))

        # sum the number of reverse questions left blank or preferred not to answer
        harmavoidance_reverse_leftblank = harmavoidance_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        harmavoidance_reverse_prefernotanswer = harmavoidance_rev[harmavoidance_rev[tci_harmavoidance_rev_keys] == nonresp['tci']].count(axis=1)
        harmavoidance_reverse_unanswered = harmavoidance_reverse_leftblank + harmavoidance_reverse_prefernotanswer

        # sum all the reverse scores
        harmavoidance_rev_score = harmavoidance_rev[harmavoidance_rev[tci_harmavoidance_rev_keys] <= 5].rsub(6).sum(axis=1, skipna=True)

        # Total SCORE
        total_harmavoidance_score = harmavoidance_forward_score + harmavoidance_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_harmavoidance_unanswered = harmavoidance_forward_unanswered + harmavoidance_reverse_unanswered

        # TOTAL ANSWERS LEFT BLANK
        total_harmavoidance_leftblank = harmavoidance_forward_leftblank + harmavoidance_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_harmavoidance_prefernotanswer = harmavoidance_forward_prefernotanswer + harmavoidance_reverse_prefernotanswer

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the total number of questions in the subscale.
        # Add all of this to to the original drive score.
        total_harmavoidance_score = total_harmavoidance_score + (total_harmavoidance_unanswered * total_harmavoidance_score / (len(tci_harmavoidance_keys) + len(tci_harmavoidance_rev_keys)))

        # Discard any value below 20 and above 80
        # total_harmavoidance_score = ['Discard (<20)' if x < 20 else 'Discard (>80)' if x > 80 else x for x in total_harmavoidance_score]


        harmall = pd.DataFrame(
            {'TCI_Harm-Avoidance_Score': total_harmavoidance_score, 'TCI_Harm-Avoidance_Left_Blank': total_harmavoidance_leftblank,
             'TCI_Harm-Avoidance_Prefer_Not_to_Answer': total_harmavoidance_prefernotanswer})




        # ------------------------------------------------------------------------------
        # REWARD DEPENDENCE SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        rewarddependence_forward = input[tci_rewarddependence_keys].apply(pd.to_numeric, args=('coerce',))
        rewarddependence_forward_leftblank = rewarddependence_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        rewarddependence_forward_prefernotanswer = rewarddependence_forward[rewarddependence_forward[tci_rewarddependence_keys] == nonresp['tci']].count(axis=1)
        rewarddependence_forward_unanswered = rewarddependence_forward_leftblank + rewarddependence_forward_prefernotanswer

        # sum all the forward scores
        rewarddependence_forward_score = rewarddependence_forward[(rewarddependence_forward[tci_rewarddependence_keys] >= 1) &
                                                                  (rewarddependence_forward[tci_rewarddependence_keys] <= 5)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        rewarddependence_rev = input[tci_rewarddependence_rev_keys].apply(pd.to_numeric, args=('coerce',))

        # sum the number of reverse questions left blank or preferred not to answer
        rewarddependence_reverse_leftblank = rewarddependence_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        rewarddependence_reverse_prefernotanswer = rewarddependence_rev[rewarddependence_rev[tci_rewarddependence_rev_keys] == nonresp['tci']].count(axis=1)
        rewarddependence_reverse_unanswered = rewarddependence_reverse_leftblank + rewarddependence_reverse_prefernotanswer

        # sum all the reverse scores
        rewarddependence_rev_score = rewarddependence_rev[rewarddependence_rev[tci_rewarddependence_rev_keys] <= 5].rsub(6).sum(axis=1, skipna=True)

        # Total SCORE
        total_rewarddependence_score = rewarddependence_forward_score + rewarddependence_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_rewarddependence_unanswered = rewarddependence_forward_unanswered + rewarddependence_reverse_unanswered

        # TOTAL ANSWERS LEFT BLANK
        total_rewarddependence_leftblank = rewarddependence_forward_leftblank + rewarddependence_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_rewarddependence_prefernotanswer = rewarddependence_forward_prefernotanswer + rewarddependence_reverse_prefernotanswer

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the total number of questions in the subscale.
        # Add all of this to to the original drive score.
        total_rewarddependence_score = total_rewarddependence_score + (total_rewarddependence_unanswered * total_rewarddependence_score / (len(tci_rewarddependence_keys) + len(tci_rewarddependence_rev_keys)))

        # Discard any value below 20 and above 100
        # total_rewarddependence_score = ['Discard (<20)' if x < 20 else 'Discard (>100)' if x > 100 else x for x in total_rewarddependence_score]


        rewardall = pd.DataFrame(
            {'TCI_Reward-Dependence_Score': total_rewarddependence_score, 'TCI_Reward-Dependence_Left_Blank': total_rewarddependence_leftblank,
             'TCI_Reward-Dependence_Prefer_Not_to_Answer': total_rewarddependence_prefernotanswer})




        # ------------------------------------------------------------------------------
        # PERSISTENCE SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        persistence_forward = input[tci_persistence_keys].apply(pd.to_numeric, args=('coerce',))
        persistence_forward_leftblank = persistence_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        persistence_forward_prefernotanswer = persistence_forward[persistence_forward[tci_persistence_keys] == nonresp['tci']].count(axis=1)
        persistence_forward_unanswered = persistence_forward_leftblank + persistence_forward_prefernotanswer

        # sum all the forward scores
        persistence_forward_score = persistence_forward[(persistence_forward[tci_persistence_keys] >= 1) &
                                                        (persistence_forward[tci_persistence_keys] <= 5)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        persistence_rev = input[tci_persistence_rev_keys].apply(pd.to_numeric, args=('coerce',))

        # sum the number of reverse questions left blank or preferred not to answer
        persistence_reverse_leftblank = persistence_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        persistence_reverse_prefernotanswer = persistence_rev[persistence_rev[tci_persistence_rev_keys] == nonresp['tci']].count(axis=1)
        persistence_reverse_unanswered = persistence_reverse_leftblank + persistence_reverse_prefernotanswer

        # sum all the reverse scores
        persistence_rev_score = persistence_rev[persistence_rev[tci_persistence_rev_keys] <= 5].rsub(6).sum(axis=1, skipna=True)

        # Total SCORE
        total_persistence_score = persistence_forward_score + persistence_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_persistence_unanswered = persistence_forward_unanswered + persistence_reverse_unanswered

        # TOTAL ANSWERS LEFT BLANK
        total_persistence_leftblank = persistence_forward_leftblank + persistence_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_persistence_prefernotanswer = persistence_forward_prefernotanswer + persistence_reverse_prefernotanswer

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the total number of questions in the subscale.
        # Add all of this to to the original drive score.
        total_persistence_score = total_persistence_score + (total_persistence_unanswered * total_persistence_score / (len(tci_persistence_keys) + len(tci_persistence_rev_keys)))

        # Discard any value below 20 and above 100
        # total_persistence_score = ['Discard (<20)' if x < 20 else 'Discard (>100)' if x > 100 else x for x in total_persistence_score]



        persistall = pd.DataFrame(
            {'TCI_Persistence_Score': total_persistence_score, 'TCI_Persistence_Left_Blank': total_persistence_leftblank,
             'TCI_Persistence_Prefer_Not_to_Answer': total_persistence_prefernotanswer})




        # ------------------------------------------------------------------------------
        # SELF-DIRECTEDNESS SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        selfdirectedness_forward = input[tci_selfdirectedness_keys].apply(pd.to_numeric, args=('coerce',))
        selfdirectedness_forward_leftblank = selfdirectedness_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        selfdirectedness_forward_prefernotanswer = selfdirectedness_forward[selfdirectedness_forward[tci_selfdirectedness_keys] == nonresp['tci']].count(axis=1)
        selfdirectedness_forward_unanswered = selfdirectedness_forward_leftblank + selfdirectedness_forward_prefernotanswer

        # sum all the forward scores
        selfdirectedness_forward_score = selfdirectedness_forward[(selfdirectedness_forward[tci_selfdirectedness_keys] >= 1) &
                                                                  (selfdirectedness_forward[tci_selfdirectedness_keys] <= 5)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        selfdirectedness_rev = input[tci_selfdirectedness_rev_keys].apply(pd.to_numeric, args=('coerce',))

        # sum the number of reverse questions left blank or preferred not to answer
        selfdirectedness_reverse_leftblank = selfdirectedness_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        selfdirectedness_reverse_prefernotanswer = selfdirectedness_rev[selfdirectedness_rev[tci_selfdirectedness_rev_keys] == nonresp['tci']].count(axis=1)
        selfdirectedness_reverse_unanswered = selfdirectedness_reverse_leftblank + selfdirectedness_reverse_prefernotanswer

        # sum all the reverse scores
        selfdirectedness_rev_score = selfdirectedness_rev[selfdirectedness_rev[tci_selfdirectedness_rev_keys] <= 5].rsub(6).sum(axis=1, skipna=True)

        # Total SCORE
        total_selfdirectedness_score = selfdirectedness_forward_score + selfdirectedness_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_selfdirectedness_unanswered = selfdirectedness_forward_unanswered + selfdirectedness_reverse_unanswered

        # TOTAL ANSWERS LEFT BLANK
        total_selfdirectedness_leftblank = selfdirectedness_forward_leftblank + selfdirectedness_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_selfdirectedness_prefernotanswer = selfdirectedness_forward_prefernotanswer + selfdirectedness_reverse_prefernotanswer

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the total number of questions in the subscale.
        # Add all of this to to the original drive score.
        total_selfdirectedness_score = total_selfdirectedness_score + (total_selfdirectedness_unanswered * total_selfdirectedness_score / (len(tci_selfdirectedness_keys) + len(tci_selfdirectedness_rev_keys)))

        # Discard any value below 20 and above 100
        # total_selfdirectedness_score = ['Discard (<20)' if x < 20 else 'Discard (>100)' if x > 100 else x for x in total_selfdirectedness_score]


        directednessall = pd.DataFrame(
            {'TCI_Self-Directedness_Score': total_selfdirectedness_score, 'TCI_Self-Directedness_Left_Blank': total_selfdirectedness_leftblank,
             'TCI_Self-Directedness_Prefer_Not_to_Answer': total_selfdirectedness_prefernotanswer})



        # ------------------------------------------------------------------------------
        # COOPERATIVENESS SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        cooperativeness_forward = input[tci_cooperativeness_keys].apply(pd.to_numeric, args=('coerce',))
        cooperativeness_forward_leftblank = cooperativeness_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        cooperativeness_forward_prefernotanswer = cooperativeness_forward[cooperativeness_forward[tci_cooperativeness_keys] == nonresp['tci']].count(axis=1)
        cooperativeness_forward_unanswered = cooperativeness_forward_leftblank + cooperativeness_forward_prefernotanswer

        # sum all the forward scores
        cooperativeness_forward_score = cooperativeness_forward[(cooperativeness_forward[tci_cooperativeness_keys] >= 1) &
                                                                (cooperativeness_forward[tci_cooperativeness_keys] <= 5)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        cooperativeness_rev = input[tci_cooperativeness_rev_keys].apply(pd.to_numeric, args=('coerce',))

        # sum the number of reverse questions left blank or preferred not to answer
        cooperativeness_reverse_leftblank = cooperativeness_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        cooperativeness_reverse_prefernotanswer = cooperativeness_rev[cooperativeness_rev[tci_cooperativeness_rev_keys] == nonresp['tci']].count(axis=1)
        cooperativeness_reverse_unanswered = cooperativeness_reverse_leftblank + cooperativeness_reverse_prefernotanswer

        # sum all the reverse scores
        cooperativeness_rev_score = cooperativeness_rev[cooperativeness_rev[tci_cooperativeness_rev_keys] <= 5].rsub(6).sum(axis=1, skipna=True)

        # Total SCORE
        total_cooperativeness_score = cooperativeness_forward_score + cooperativeness_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_cooperativeness_unanswered = cooperativeness_forward_unanswered + cooperativeness_reverse_unanswered

        # TOTAL ANSWERS LEFT BLANK
        total_cooperativeness_leftblank = cooperativeness_forward_leftblank + cooperativeness_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_cooperativeness_prefernotanswer = cooperativeness_forward_prefernotanswer + cooperativeness_reverse_prefernotanswer

        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the total number of questions in the subscale.
        # Add all of this to to the original drive score.
        total_cooperativeness_score = total_cooperativeness_score + (total_cooperativeness_unanswered * total_cooperativeness_score / (len(tci_cooperativeness_keys) + len(tci_cooperativeness_rev_keys)))

        # Discard any value below 20 and above 100
        # total_cooperativeness_score = ['Discard (<20)' if x < 20 else 'Discard (>100)' if x > 100 else x for x in total_cooperativeness_score]


        cooperativeall = pd.DataFrame(
            {'TCI_Cooperativeness_Score': total_cooperativeness_score, 'TCI_Cooperativeness_Left_Blank': total_cooperativeness_leftblank,
             'TCI_Cooperativeness_Prefer_Not_to_Answer': total_cooperativeness_prefernotanswer})



        # ------------------------------------------------------------------------------
        # SELF-TRANSCENDENCE SCORE

        # FORWARD SCORES AND FORWARD QUESTIONS UNANSWERED
        selftranscendence_forward = input[tci_selftranscendence_keys].apply(pd.to_numeric, args=('coerce',))
        selftranscendence_forward_leftblank = selftranscendence_forward.apply(lambda x: sum(x.isnull().values), axis=1)
        selftranscendence_forward_prefernotanswer = selftranscendence_forward[selftranscendence_forward[tci_selftranscendence_keys] == nonresp['tci']].count(axis=1)
        selftranscendence_forward_unanswered = selftranscendence_forward_leftblank + selftranscendence_forward_prefernotanswer

        # sum all the forward scores
        selftranscendence_forward_score = selftranscendence_forward[(selftranscendence_forward[tci_selftranscendence_keys] >= 1) &
                                                                    (selftranscendence_forward[tci_selftranscendence_keys] <= 5)].sum(axis=1)

        # REVERSE SCORES AND REVERSE QUESTIONS UNANSWERED
        selftranscendence_rev = input[tci_selftranscendence_rev_keys].apply(pd.to_numeric, args=('coerce',))

        # sum the number of reverse questions left blank or preferred not to answer
        selftranscendence_reverse_leftblank = selftranscendence_rev.apply(lambda x: sum(x.isnull().values), axis=1)
        selftranscendence_reverse_prefernotanswer = selftranscendence_rev[selftranscendence_rev[tci_selftranscendence_rev_keys] == nonresp['tci']].count(axis=1)
        selftranscendence_reverse_unanswered = selftranscendence_reverse_leftblank + selftranscendence_reverse_prefernotanswer

        # sum all the reverse scores
        selftranscendence_rev_score = selftranscendence_rev[selftranscendence_rev[tci_selftranscendence_rev_keys] <= 5].rsub(6).sum(axis=1, skipna=True)

        # Total SCORE
        total_selftranscendence_score = selftranscendence_forward_score + selftranscendence_rev_score
        # TOTAL ANSWERS UNANSWERED
        total_selftranscendence_unanswered = selftranscendence_forward_unanswered + selftranscendence_reverse_unanswered

        # TOTAL ANSWERS LEFT BLANK
        total_selftranscendence_leftblank = selftranscendence_forward_leftblank + selftranscendence_reverse_leftblank
        #TOTAL ANSWERS PREFER NOT TO ANSWER
        total_selftranscendence_prefernotanswer = selftranscendence_forward_prefernotanswer + selftranscendence_reverse_prefernotanswer


        # If there are values missing, multiply the number of unanswered questions by the total subscale score.
        # Then divide that by the total number of questions in the subscale.
        # Add all of this to to the original drive score.
        total_selftranscendence_score = total_selftranscendence_score + (total_selftranscendence_unanswered * total_selftranscendence_score / (len(tci_selftranscendence_keys) + len(tci_selftranscendence_rev_keys)))

        # Discard any value below 20 and above 100
        # total_selftranscendence_score = ['Discard (<20)' if x < 20 else 'Discard (>100)' if x > 100 else x for x in total_selftranscendence_score]


        selftranscendall = pd.DataFrame(
            {'TCI_Self-Transcendence_Score': total_selftranscendence_score, 'TCI_Self-Transcendence_Left_Blank': total_selftranscendence_leftblank,
             'TCI_Self-Transcendence_Prefer_Not_to_Answer': total_selftranscendence_prefernotanswer})



        # ------------------------------------------------------------------------------
        # Put all the scores into one frame
        frames = [noveltyall, harmall, rewardall, persistall, directednessall, cooperativeall, selftranscendall, checks]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print("We could not find the TCI headers in your dataset. Please look at the tci function in this package and put in the correct keys.")