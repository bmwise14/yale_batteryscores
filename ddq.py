#!/usr/bin/python

"""
Battery Scores Package for Processing Qualtrics CSV Files

@author: Bradley Wise
@email: bradley.wise@yale.edu
@version: 1.1
@date: 2016.12.06
"""

import pandas as pd
from math import log
import sys

# input = the data you are using with with the keys listed below as headers


def ddq(input):
    # DELAY DISCOUNTING QUESTIONNAIRE

    # RESOURCES USED:
    """GSP Scales Notebook - Holmes Lab"""
    # READ THESE TOP 4 PAPERS #
    """http://psycnet.apa.org/journals/xge/128/1/78.pdf"""
    """https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4418201/"""
    """https://www.ncbi.nlm.nih.gov/pmc/articles/PMC3746343/"""
    """https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4388189/"""


    # OTHER REFERENCES #
    """http://link.springer.com/article/10.3758/BF03210748"""
    """http://link.springer.com/article/10.3758/PBR.16.3.457"""
    """http://www.sciencedirect.com/science/article/pii/S0005791610000261"""
    """http://psych.wustl.edu/lengreen/publications/Discounting%20of%20delayed%20rewards%20(1994).pdf"""
    """https://web.williams.edu/Psychology/Faculty/Kirby/"""

    # SCORING:
    # IMMEDIATE REWARD  DELAYED REWARD
    #        1               2
    """
    1. V = A/(1+kD)
    2. V = amount of the immediate reward
    3. A = amount of the delayed reward
    4. D = the amount of days delayed for the delayed reward
    5. k = impulsiveness parameter, such that as k increases, impulsivity increases

    SOLVE FOR K:
    k = ((A/V)-1)/D

    6. Input into Console or Command Line. This computes the k-value at which a participant is indifferent to a choice:
    ddq1A = float(55)
    ddq1V = float(54)
    ddq1D = float(117)
    ddq1k = round(((ddq1A/ddq1V)-1)/ddq1D, 5)
    ddq1k = 0.00016


    7. k = the value at which the participant is indifferent toward either option. However, since a participant has to
    choose a value, the k value will fall above or below the indifference value, depending on what reward is chosen.
    If they choose the immediate smaller reward, the k value will be higher than the indifference k.
    If they choose the larger, delayed reward, the k value will be lower than the indifference k.

    8. Below is the continuum for indifference k. There are 27 total DDQ Questions.
    However, there are only 9 indifference k values because there are 3 different reward magnitudes:
    small, medium, and large.
    Each reward magnitude is scored separately.

    If you were indifferent to a choice, your response would represent one of these values based on the question.


                                0        1       2       3       4      5      6      7     8
            indifferencek = [0.00016, 0.0004, 0.0010, 0.0025, 0.0060, 0.016, 0.041, 0.10, 0.25]


    Each participant is given a k-bin below based on their choice of each of the 9 questions as a whole.
    These k assignments are the geometric mean of two values above with two endpoints being 0.00016 and 0.2500.
    There are 10 K bins. We will assign one bin to each participant depending on the percentage of immediate rewards
    they choose.


                      0         1        2       3        4        5       6        7         8      9
          kbins = [0.00016, 0.00025, 0.00063, 0.00158, 0.00387, 0.0098, 0.02561, 0.06403, 0.15811, 0.2500]



    9. Example, in words:
    If someone chooses OPTION 1 (immediate reward) on Question 13, that means their k value is greater than 0.00016,
    and they are assigned the k-bin between 0.00016 and 0.0004, which is 0.0025.

    If someone chooses OPTION 2 (delayed reward) on Question 13, that means their k value is less than 0.00016,
    and they are assigned the k-bin value of 0.00016.


    10. However, since people's choices are not perfectly consistent with any single value of k, the code below
    calculates the percentage of immediate choices to total choices for each reward magnitude.

    CALCULATION EXAMPLE:

    If someone chose 4 of 9 immediate choices, or 44.44% immediate choices, they would be assigned to kbin[4], or 0.00387,
    which is the geometric mean of 0.0025 and 0.0060. This calculation is the same for all reward magnitudes.

    PERCENTAGE IMMEDIATE CHOSEN to K-BIN ESTIMATE ASSIGNMENT
    0% = 0.00016
    11.11% = 0.00025
    22.22% = 0.00063
    33.33% = 0.00158
    44.44% = 0.00387
    55.55% = 0.0098
    66.66% = 0.02561
    77.77% = 0.06403
    88.88% = 0.15811
    100% = 0.2500


    The coding below may have some error because calculating percentage doesn't represent the point at which you switch.
    This is just an estimate (Kirby, Petry, & Bickel 1999).


    11. TOTAL K-VALUE PENDING. PLAN IS TO TAKE THE GEOMETRIC MEAN OF THE SMALL, MEDIUM, and LARGE REWARD K-BINS.

    """
    try:
        # ------------------------------------------------------------------------------
        # These keys are ordered by indifference k in ascending order.
        smalldr_keys = ['DDQ_13', 'DDQ_20', 'DDQ_26', 'DDQ_22', 'DDQ_3', 'DDQ_18', 'DDQ_5', 'DDQ_7', 'DDQ_11']
        mediumdr_keys = ['DDQ_1', 'DDQ_6', 'DDQ_24', 'DDQ_16', 'DDQ_10', 'DDQ_21', 'DDQ_14', 'DDQ_8', 'DDQ_27']
        largedr_keys = ['DDQ_9', 'DDQ_17', 'DDQ_12', 'DDQ_15', 'DDQ_2', 'DDQ_25', 'DDQ_23', 'DDQ_19', 'DDQ_4']



        # these k bin assignments are the geometric mean of two values with two endpoints being 0.00016 and 0.2500.
        kbins = [0.00016, 0.00025, 0.00063, 0.00158, 0.00387, 0.0098, 0.02561, 0.06403, 0.15811, 0.2500]

        # -----------------------------------------------------------------------------------------------------------------#
        # Converts keys to numeric values
        smalldr = input[smalldr_keys].apply(pd.to_numeric, args=('raise',))

        # Counts the number of delayed reward choices and immediate choices among the small delayed reward keys
        smalldr_delayedreward = smalldr[smalldr[smalldr_keys] == 2].count(axis=1)
        smalldr_didnotdelay = smalldr[smalldr[smalldr_keys] == 1].count(axis=1)

        # Totals the number of total rewards chosen
        totalsmalldr = smalldr_didnotdelay + smalldr_delayedreward

        # Creates a percentage of immediate choices to total choices given
        smalldrimmediatepercentage = smalldr_didnotdelay / totalsmalldr * 100

        # Fills any N/A values to 99999
        smalldrimmediatepercentage.fillna(value=99999)


        # List Comprehension bins each person into their appropriate k-value (see kbins) based
        # on their percentage of immediate choices to total choices.
        # This will put a 0 on all other percentages.
        # Any other percentage than the ones below means a participant skipped a question.
        smallrewards = [kbins[0] if x ==0.0
        else kbins[1] if x>=11 and x<=12
        else kbins[2] if x>=22 and x<=23
        else kbins[3] if x>=33 and x<=34
        else kbins[4] if x>=44 and x<=45
        else kbins[5] if x>=55 and x<=56
        else kbins[6] if x>=66 and x<=67
        else kbins[7] if x>=77 and x<=78
        else kbins[8] if x>=88 and x<=89
        else kbins[9] if x == 100
        else 0 for x in smalldrimmediatepercentage]


        # Drops the 0 values because it means that the participant skipped at least 1 question.
        smallrewardks = ['DISCARD' if x == 0 else x for x in smallrewards]
        # List Comprehension that takes the log10 of each k-bin value and rounds to the 5th decimal place.
        # This also drops any discount rate where a 0 value is given
        smalllogdiscountrate = [round(log(y, 10), 5) if y > 0 and y <= 1 else 'DISCARD' for y in smallrewards]

        # Puts the k-values into a dataframe
        smallldr = pd.DataFrame(
            {'Small_Reward_k-value': smallrewardks, 'Log10_Small_DiscountRate': smalllogdiscountrate})
        smallldr.index +=1

        # -----------------------------------------------------------------------------------------------------------------#
        # see smalldr comments. Exact same computation.
        mediumdr = input[mediumdr_keys].apply(pd.to_numeric, args=('raise',))

        mediumdr_delayedreward = mediumdr[mediumdr[mediumdr_keys] == 2].count(axis=1)
        mediumdr_didnotdelay = mediumdr[mediumdr[mediumdr_keys] == 1].count(axis=1)

        totalmediumdr = mediumdr_didnotdelay + mediumdr_delayedreward

        mediumdrimmediatepercentage = mediumdr_didnotdelay / totalmediumdr * 100
        mediumdrimmediatepercentage.fillna(value=99999)

        mediumrewards = [kbins[0] if x == 0.0
        else kbins[1] if x >= 11 and x <= 12
        else kbins[2] if x>=22 and x<=23
        else kbins[3] if x>=33 and x<=34
        else kbins[4] if x>=44 and x<=45
        else kbins[5] if x>=55 and x<=56
        else kbins[6] if x>=66 and x<=67
        else kbins[7] if x>=77 and x<=78
        else kbins[8] if x>=88 and x<=89
        else kbins[9] if x == 100
        else 0 for x in mediumdrimmediatepercentage]

        mediumrewardks = ['DISCARD' if x == 0 else x for x in mediumrewards]
        midlogdiscountrate = [round(log(y, 10), 5) if y > 0 and y <= 1 else 'DISCARD' for y in mediumrewards]

        mediumldr = pd.DataFrame(
            {'Medium_Reward_k-value': mediumrewardks, 'Log10_Medium_DiscountRate': midlogdiscountrate})
        mediumldr.index +=1

        # -----------------------------------------------------------------------------------------------------------------#
        # see smalldr comments. Exact same computation.
        largedr = input[largedr_keys].apply(pd.to_numeric, args=('raise',))

        largedr_delayedreward = largedr[largedr[largedr_keys] == 2].count(axis=1)
        largedr_didnotdelay = largedr[largedr[largedr_keys] == 1].count(axis=1)


        totallargedr = largedr_didnotdelay + largedr_delayedreward

        largedrimmediatepercentage = largedr_didnotdelay / totallargedr * 100
        largedrimmediatepercentage.fillna(value=99999)

        largerewards = [kbins[0] if x == 0.0
        else kbins[1] if x >= 11 and x <= 12
        else kbins[2] if x>=22 and x<=23
        else kbins[3] if x>=33 and x<=34
        else kbins[4] if x>=44 and x<=45
        else kbins[5] if x>=55 and x<=56
        else kbins[6] if x>=66 and x<=67
        else kbins[7] if x>=77 and x<=78
        else kbins[8] if x>=88 and x<=89
        else kbins[9] if x == 100
        else 0 for x in largedrimmediatepercentage]



        largerewardks = ['DISCARD' if x==0 else x for x in largerewards]
        largelogdiscountrate = [round(log(y, 10), 5) if y > 0 and y <= 1 else 'DISCARD' for y in largerewards]

        largeldr = pd.DataFrame(
            {'Large_Reward_k-value': largerewardks, 'Log10_Large_DiscountRate': largelogdiscountrate})
        largeldr.index +=1
        # -----------------------------------------------------------------------------------------------------------------#
        # THIS COMPUTES THE TOTAL K-VALUE BY COMBINING ALL 3 SCORES

        # Converts each k-bin set to pandas dataframe
        small = pd.DataFrame(smallrewards)
        medium = pd.DataFrame(mediumrewards)
        large = pd.DataFrame(largerewards)

        # puts the bins into one variable
        kframes = [small, medium, large]

        # function for calculating the geometric mean of a set of data
        geomean = lambda n: reduce(lambda x, y: x * y, n) ** (1.0 / len(n))

        # creates a variable for calculating the geometric mean of the k-bin set across rows
        # make sure you have no missing questions in your data.
        totalk = geomean(kframes)

        # renames the column in pandas dataframe from 0 to Total_k-value
        totalk = totalk.rename(columns = {0: 'Total_k-value'})
        totalk.index+=1

        # gets the log10 and rounds if the values in the dataframe are between 0 and less than or equal to 1.
        # Otherwise, if the value is 0 or greater than 1, the value, and therefore, the participant, is dropped.
        totallogdiscountrate = [round(log(y, 10), 5) if y > 0 and y <= 1 else 'DISCARD' for y in totalk['Total_k-value']]
        totaldiscountrate = pd.DataFrame({'Total_Discount_Rate': totallogdiscountrate})
        totaldiscountrate.index += 1

        # -----------------------------------------------------------------------------------------------------------------#

        frames = [smallldr, mediumldr, largeldr, totalk, totaldiscountrate]
        result = pd.concat(frames, axis=1)
        return result
    except KeyError:
        print("We could not find the DDQ headers in your dataset. "
              "Please look at the ddq function in this package and put in the correct keys.")
    except ValueError:
        print("We found strings in your DDQ dataset. Please make sure there are no strings/letters in your input. Otherwise, we can't do our thang.")