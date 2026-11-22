from processing_utils import * # extract_participant_data

subject_path = "Data\OpenCapData_2b13ffb5-df7e-4873-a2fc-4d2ad88bfc8e"
squat_conditions = ["unweighted.mot", "weighted_10p.mot", "weighted_25p.mot"]

all_stats = {}
for condition in squat_conditions:
    all_stats[condition] = extract_participant_data(subject_path, condition)
stats = extract_participant_data(subject_path, condition)