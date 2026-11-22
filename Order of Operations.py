#Order of Operations!
#First, we run Annette code --> get out 3D matrix for each participants
#Then we use (TBD function) --> extract relevant angles to get participant_data 3D matrix

#For between testing:
#Run avg_angles using participant_data --> get participant_avg 
#  (run for each of 14 participants)
#Run untrained_avgs using 5 untrained participant_avg matrices --> get untrained_matrix
#Run trained_avgs using 9 trained participant_avg matrices --> get trained_matrix
#Run between_t_testing using untrained_matrix & trained matrix --> get p_values matrix
#Run avg_angles using untrained_matrix --> get avg_untrained_matrix
#Run avg_angles using trained_matrix --> get avg_trained_matrix
#Run (TBD function) using avg_untrained_matrix, avg_trained_matrix, & p_values 
#    to make histograms for significant p-values

#For within testing:
#Run within_ANOVA using participant_data --> get ANOVA_p_values
#   (run for each of 14 participants)
#Run within_t_testing using participant_data & ANOVA_p_values --> get ttest_p_values
#POST-HOC??
#Run (TBD function) using participant_avg & ttest_p_values 
#    to make histograms for significant p-values