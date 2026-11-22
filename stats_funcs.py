#functions for calculating stats
from scipy.stats import ttest_ind
from scipy.stats import f_oneway
import statistics as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# participant_data = matrix of condition matrices which hold vectors for each angle
# participant_data size = 3x9x5 (3 conditions(depth), 9 angles (rows), 5 points per angle (cols))
def avg_angles(participant_data): 
    """avg_angles takes in a 3D matrix: participant_data which includes 3 conditions(depth),
    9 angles (rows), and 5 points per angle (cols). This function takes the average of each
    row and returns the 2D matrix: participant_avg containing 3 conditions (rows) and 9 average
    angles (cols)."""
    #determine size 
    depth = len(participant_data)
    rows = len(participant_data[0])
    cols = len(participant_data[0][0])

    participant_avg = np.zeros((depth, rows))   #creating output matrix

    #loop through to find average angles
    for i in range(depth):
        for j in range(rows):
            participant_avg[i][j] = st.mean(participant_data[i][j])

    return participant_avg

def untrained_avgs(p1, p2, p3, p4, p5):
    """untrained_avgs takes in the 5 untrained 2D matrices: p1-p5 which each include the 
    3 conditions (rows) and 9 avg angles (columns). This function creates a new vector for each
    angle and condition containing the corresponding value from each participant and returns this 
    in a 3D matrix: untrained_matrix containing 3 conditions (depth), 9 angles (rows), and 5 
    participant avgs (cols)."""
    #determine size
    depth = len(p1)
    rows = len(p1[0])
    cols = 5 #based on # of input matrices

    untrained_matrix = np.zeros((depth, rows, cols))  #creating output matrix
    for i in range(depth):
        for j in range(rows):
            untrained_matrix[i][j] = [p1[i][j], p2[i][j], p3[i][j], p4[i][j], p5[i][j]]

    return untrained_matrix

def trained_avgs(p1, p2, p3, p4, p5, p6, p7, p8, p9):
    """trained_avgs takes in the 9 trained 2D matrices: p1-p9 which each include the 
    3 conditions (rows) and 9 avg angles (columns). This function creates a new vector for each
    angle and condition containing the corresponding value from each participant and returns this 
    in a 3D matrix: trained_matrix containing 3 conditions (depth), 9 angles (rows), and 9 
    participant avgs (cols)."""
    #determine size
    depth = len(p1)
    rows = len(p1[0])
    cols = 9 #based on # of input matrices

    trained_matrix = np.zeros((depth, rows, cols))  #creating output matrix
    for i in range(depth):
        for j in range(rows):
            trained_matrix[i][j] = [p1[i][j], p2[i][j], p3[i][j], p4[i][j], p5[i][j], p6[i][j], p7[i][j], p8[i][j], p9[i][j]]

    return trained_matrix

def between_t_testing(untrained_matrix, trained_matrix):
    """between_t_testing takes in the untrained_matrix and trained_matrix which are 3D matrices that hold 3 conditions (depth), 9 angles
     (rows), and participant averages: 5 for untrained, 9 for trained (cols). This function takes the two-sided t-test of each angle for
     each depth, between trained and untrained. The null hypothesis is that there is no statistical difference between the two. It extracts
     the p-value from each test and outputs a 2D matrix, p_values: 3 conditions (rows), 9 angles (cols)
      """
    #determine size 
    depth = len(untrained_matrix)
    rows = len(untrained_matrix[0])

    p_values = np.zeros((depth, rows))   #creating output matrix
    for i in range(depth):
        for j in range(rows):
            result = ttest_ind(untrained_matrix[i][j], trained_matrix[i][j])
            p_values[i][j] = result.pvalue

    return p_values

def within_ANOVA(participant_data):
    """within_ANOVA takes in a 3D matrix: participant_data which includes 3 conditions(depth),
        9 angles (rows), and 5 points per angle (cols). This function takes the one_way ANOVA 
        between the 3 weight conditions for each angle type and returns the vector: ANOVA_p_values 
        containing the resulting p values for each angle type.
    """
    #determine size 
    depth = len(participant_data) # each condition
    rows = len(participant_data[0]) # each angle type
    cols = len(participant_data[0][0]) # each max angle

    ANOVA_p_values = np.zeros(rows)   #creating output vector

    #loop through to find p values using one-sided ANOVA test
    for j in range(rows):
        anova_result = f_oneway(participant_data[0][j], participant_data[1][j], participant_data[2][j])
        ANOVA_p_values[j] = anova_result.pvalue

    return ANOVA_p_values

def within_t_testing(participant_data, ANOVA_p_values):
    """within_t_testing takes in a 3D matrix: participant_data which includes 3 conditions(depth),
    9 angles (rows), and 5 points per angle (cols). It also takes in the vector: ANOVA_p_values,
    which contains the p values obtained from the ANOVA test for each angle. This function takes 
    the two-sided t-test of each angle between each weight condition pair. The null hypothesis is 
    that there is no statistical difference between the two. It extracts the p-value from each test 
    and outputs a 2D matrix, ttest_p_values: 9 angle types (rows), 3 weight comparisons (cols)"""
    #determine size 
    depth = len(participant_data) # each condition
    rows = len(participant_data[0]) # each angle type
    cols = len(participant_data[0][0]) # each max angle

    ttest_p_values = np.zeros((rows, depth))   #creating output matrix
    # will be of the form: each angle type is a row, each ttest is a column

    # for each angle type
    for j in range(rows):
        if ANOVA_p_values[j] < 0.05: # conduct 3 t-tests if significant
            result_uw_10p = ttest_ind(participant_data[0][j], participant_data[1][j])
            result_10p_25p = ttest_ind(participant_data[1][j], participant_data[2][j])
            result_uw_25p = ttest_ind(participant_data[0][j], participant_data[2][j])
            ttest_p_values[j] = [result_uw_10p.pvalue, result_10p_25p.pvalue, result_uw_25p.pvalue]
        else:
            ttest_p_values[j] = [100, 100, 100] # high values for insignificant p

    ttest_p_values = ttest_p_values*3 # Bonferroni Adjustment (for conservative threshold)

    return ttest_p_values

def between_bar_charts(avg_untrained_matrix, avg_trained_matrix, p_values):
    """
    """
    #determine size 
    rows = len(avg_untrained_matrix) # each condition
    cols = len(avg_untrained_matrix[0]) # each angle type
    
    #extract significant data
    count = np.zeros(rows)
    for i in range(rows):
        count[i] = np.sum(p_values[i] < 0.05)

    significant_untrained_uw = np.zeros(count[0])
    significant_untrained_10p = np.zeros(count[1])
    significant_untrained_25p = np.zeros(count[2])
    significant_trained_uw = np.zeros(count[0])
    significant_trained_10p = np.zeros(count[1])
    significant_trained_25p = np.zeros(count[2])
    counter = [0, 0, 0]

    for j in range(cols):
        if p_values[0][j] < 0.05:
            significant_untrained_uw[counter[0]] = avg_untrained_matrix[0][j]
            significant_trained_uw[counter[0]] = avg_trained_matrix[0][j]
            counter[0] += 1
        if p_values[1][j] < 0.05:
            significant_untrained_10p[counter[1]] = avg_untrained_matrix[1][j]
            significant_trained_10p[counter[1]] = avg_trained_matrix[1][j]
            counter[1] += 1
        if p_values[2][j] < 0.05:
            significant_untrained_25p[counter[2]] = avg_untrained_matrix[2][j]
            significant_trained_25p[counter[2]] = avg_trained_matrix[2][j]
            counter[2] += 1
        else:
            continue

    #make bar chart for unweighted condition
    df_uw = pd.DataFrame({
            'Untrained': significant_untrained_uw,
            'Trained': significant_trained_uw
            }, index=['Q1', 'Q2', 'Q3'])
    # Automatically groups columns side-by-side per index row
    ax_uw = df_uw.plot(kind='bar', width=0.8, rot=0)
    ax_uw.set_ylabel('Angle (degrees)')
    ax_uw.set_title('Trained vs. Untrained Angles for Unweighted Condition')
    plt.show()

    #make bar chart for 10% condition
    df_10p = pd.DataFrame({
                'Untrained': significant_untrained_10p,
                'Trained': significant_trained_10p
                }, index=['Q1', 'Q2', 'Q3'])
    # Automatically groups columns side-by-side per index row
    ax_10p = df_10p.plot(kind='bar', width=0.8, rot=0)
    ax_10p.set_ylabel('Angle (degrees)')
    ax_10p.set_title('Trained vs. Untrained Angles for 10% Loading Condition')
    plt.show()

    #make bar chart for 25% condition
    df_25p = pd.DataFrame({
                'Untrained': significant_untrained_25p,
                'Trained': significant_trained_25p
                }, index=['Q1', 'Q2', 'Q3'])
    # Automatically groups columns side-by-side per index row
    ax_25p = df_25p.plot(kind='bar', width=0.8, rot=0)
    ax_25p.set_ylabel('Angle (degrees)')
    ax_25p.set_title('Trained vs. Untrained Angles for 25% Loading Condition')
    plt.show()

    return