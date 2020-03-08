import pandas as pd
from typing import List

def two_week_subsets(
        subject_data: pd.DataFrame,
        min_len: int = 0
    ) -> List[pd.DataFrame]:

    if subject_data.subject_id.nunique() != 1:
        raise ValueError(
            'More than 1 subject found: '
            + str(subject_data.subject_id.unique())
        )
    
    phases = [
        'baseline_arm_1',
        'remote_cat_1_arm_1',
        'remote_cat_2_arm_1',
        'remote_cat_3_arm_1',
        'remote_cat_4_arm_1',
        'remote_cat_5_arm_1',
        'remote_cat_6_arm_1',
        'followup_assessmen_arm_1'
    ]

    subsets = []
    s_id = subject_data.subject_id.unique()[0]
    for i in range(len(phases)-1):
        start = phases[i]
        end = phases[i+1]
        first_row = subject_data[subject_data.redcap_event_name_1 == start]
        last_row = subject_data[subject_data.redcap_event_name_1 == end]
        if last_row.catmh_dep_severity_1.isna().any():
            print('No Depression Severity', s_id)
            continue
        if first_row.catmh_dep_severity_1.isna().any():
            print('No Depression Severity', s_id)
            continue
        if first_row.empty or last_row.empty:
            continue

        if (first_row.shape[0] > 1) or (last_row.shape[0] > 1):
            print('Warning: multiple entries for first or last row, using first')
            print(first_row.shape[0], last_row.shape[0])

        chunk = subject_data.iloc[first_row.index[0]:last_row.index[0]] 
        if chunk.shape[0] >= min_len:
            chunk.loc[:, 'start'] = start
            chunk.loc[:, 'end'] = end
            chunk.loc[:, 'end_sev'] = last_row.catmh_dep_severity_1.tolist()[0]
            chunk.loc[:, 'start_sev'] = first_row.catmh_dep_severity_1.tolist()[0]
            subsets.append(chunk)

    return subsets

def split_half(data) -> pd.DataFrame:
    half = int(data.shape[0]/2)
    h_1 = data.iloc[:half]
    h_2 = data.iloc[half:]
    return h_1, h_2

