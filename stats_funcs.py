#functions for calculating stats
from scipy.stats import ttest_ind
import statistics as st
import numpy as np


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