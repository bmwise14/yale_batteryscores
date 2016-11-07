#!/usr/bin/python


import pandas as pd


# input = the data you are using with with the keys listed below as headers


def shipley(input):
    # SHIPLEY INSTITUTE OF LIVING SCALE (SHIPLEY VOCABULARY) - (SHIPLEY 2)

    # RESOURCES USED:
    """GSP Scales Notebook - Holmes Lab"""
    """Thesaurus - Will need someone to double check my answers"""

    # SCORING:
    """
    1. Sum Correct Answers per Participant.

    2. Sum any items left blank

    3. Raw Score = number correct + (items left blank/4)

    """
    try:
        # If there is a Prefer Not Answer, use it
        # -----------------------------------------------------------------------
        choice1 = ['Shipley2_4', 'Shipley2_7', 'Shipley2_13', 'Shipley2_17', 'Shipley2_19', 'Shipley2_22', 'Shipley2_23', 'Shipley2_31', 'Shipley2_34', 'Shipley2_35', 'Shipley2_38']
        choice2 = ['Shipley2_3', 'Shipley2_6', 'Shipley2_10', 'Shipley2_18', 'Shipley2_21', 'Shipley2_26', 'Shipley2_28', 'Shipley2_32', 'Shipley2_40']
        choice3 = ['Shipley2_1', 'Shipley2_2', 'Shipley2_12', 'Shipley2_14', 'Shipley2_15', 'Shipley2_16', 'Shipley2_20',
                   'Shipley2_29', 'Shipley2_33', 'Shipley2_37']
        choice4 = ['Shipley2_5', 'Shipley2_8', 'Shipley2_9', 'Shipley2_11', 'Shipley2_24', 'Shipley2_25', 'Shipley2_27', 'Shipley2_30', 'Shipley2_36', 'Shipley2_39']



        # CREATE A COUNT FOR EACH ITEM GUESSED CORRECTLY

        # COUNTS # OF QUESTIONS IN choice 1 WITH FIRST CHOICE AS CORRECT ANSWER
        c1 = input[choice1].apply(pd.to_numeric, args=('coerce',))
        c1_leftblank = c1.apply(lambda x: sum(x.isnull().values), axis=1)
        c1_score = c1[c1[choice1] == 1].count(axis=1)


        # COUNTS # OF QUESTIONS IN choice 2 WITH SECOND CHOICE AS CORRECT ANSWER
        c2 = input[choice2].apply(pd.to_numeric, args=('coerce',))
        c2_leftblank = c2.apply(lambda x: sum(x.isnull().values), axis=1)
        c2_score = c2[c2[choice2] == 2].count(axis=1)


        # COUNTS # OF QUESTIONS IN choice 3 WITH SECOND CHOICE AS CORRECT ANSWER
        c3 = input[choice3].apply(pd.to_numeric, args=('coerce',))
        c3_leftblank = c3.apply(lambda x: sum(x.isnull().values), axis=1)
        c3_score = c3[c3[choice3] == 3].count(axis=1)


        # COUNTS # OF QUESTIONS IN choice 4 WITH SECOND CHOICE AS CORRECT ANSWER
        c4 = input[choice4].apply(pd.to_numeric, args=('coerce',))
        c4_leftblank = c4.apply(lambda x: sum(x.isnull().values), axis=1)
        c4_score = c4[c4[choice4] == 4].count(axis=1)



        # Adds up all the questions that were left blank
        leftblank_all = c1_leftblank + c2_leftblank + c3_leftblank + c4_leftblank

        # Adds up the overall score, with left blank / 4
        overall_score = c1_score + c2_score + c3_score + c4_score + (leftblank_all/4)


        shipleyresult = pd.DataFrame({'Shipley2 Score' : overall_score, 'Shipley2 Left Blank' : leftblank_all})


        # Put the scores into one frame
        frames = [shipleyresult]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print("We could not find the SHIPLEY headers in your dataset. Please look at the shipley function in this package and put in the correct keys.")