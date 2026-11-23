from processing_utils import * # extract_participant_data

# subject_path = "Data\OpenCapData_2b13ffb5-df7e-4873-a2fc-4d2ad88bfc8e"
# squat_conditions = ["unweighted.mot", "weighted_10p.mot", "weighted_25p.mot"]

# all_stats = {}
# for condition in squat_conditions:
#     all_stats[condition] = extract_participant_data(subject_path, condition)
# stats = extract_participant_data(subject_path, condition)

participants = {'A':'OpenCapData_ce734903-11c7-42e5-883b-1896e7a884bc',
                'B':'OpenCapData_57058542-0829-44f0-a325-9acd356548e5',
                'C':'OpenCapData_44759cf8-6e09-44fd-a3b1-098a737dcd64',
                'D':'OpenCapData_3ea9b379-e1a5-47e8-b716-0ecdb9ab5b01',
                'E':'OpenCapData_8bac1f46-4140-4b3e-81f0-aea6436fa3f6',
                'F':'OpenCapData_db8e954a-8226-4388-9aaa-4db398d4fd26',
                'G':'OpenCapData_236b1009-ff67-4357-8c4d-6602160f1d13',
                'H':'OpenCapData_80b6c3b3-e148-4563-9d47-58cf1a5ef5d7',
                'I':'OpenCapData_4ceea288-8f4b-4304-897f-e4721a96ca0d',
                'J':'OpenCapData_66c4d455-aeb5-4b2b-86a8-15d2fec5ad2d',
                'K':'OpenCapData_2b13ffb5-df7e-4873-a2fc-4d2ad88bfc8e',
                'L':'OpenCapData_dfafe0fc-6dcc-47bb-ab78-96eef1eb37f0',
                'M':'OpenCapData_092dcbf9-59a3-456f-a321-f72af449426f',
                'N':'OpenCapData_81e0d5ee-3aa9-4869-95cd-8298fa1438bb'}

for name, participant in participants.items():
    participants[name] = extract_des_angles(participant)

