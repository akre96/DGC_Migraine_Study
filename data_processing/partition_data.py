""" Creates segments of longitudinal data for aggregation
"""
from typing import List
import pandas as pd
import data_processing.reshape_data as rd


def two_week_subsets(
        subject_data: pd.DataFrame,
        min_len: int = 0,
        verbose: bool = True,
) -> List[pd.DataFrame]:
    """ Split longitudinal data for a subject in to chunks between CAT-MH

    Arguments:
        subject_data {pd.DataFrame} -- Longitudinal data for a subject

    Keyword Arguments:
        min_len {int} -- minimum length (days) for chunks to include (default: {0})
        verbose {bool} -- print information if skipping chunks(default: {True})

    Raises:
        ValueError: input data has more than 1 subject

    Returns:
        List[pd.DataFrame] -- List of data chunks
    """

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
            if verbose:
                print('No Depression Severity', s_id)
            continue
        if first_row.catmh_dep_severity_1.isna().any():
            if verbose:
                print('No Depression Severity', s_id)
            continue
        if first_row.empty or last_row.empty:
            continue

        if (first_row.shape[0] > 1) or (last_row.shape[0] > 1):
            print('Warning: multiple entries for first or last row, using first')
            print(first_row.shape[0], last_row.shape[0])

        chunk = subject_data.iloc[first_row.index[0]:last_row.index[0]]
        next_week = subject_data.iloc[last_row.index[0]: last_row.index[0] + 7]
        if next_week.shape[0] != 7:
            if next_week.shape[0] < 7:
                if verbose:
                    print(
                        'Skipping -- No Week After Chunk:',
                        start, 'to', end, s_id,
                        next_week.shape
                    )
                continue
        if chunk.shape[0] >= min_len:
            next_mig_count = rd.melt_occurrances(
                'mbrep_start_date', next_week
            ).dropna().mbrep_start_date.count()
            chunk.loc[:, 'end_mig_freq'] = next_mig_count/next_week.shape[0]
            chunk.loc[:, 'start'] = start
            chunk.loc[:, 'end'] = end
            chunk.loc[:, 'end_sev'] = last_row.catmh_dep_severity_1.tolist()[0]
            chunk.loc[:, 'start_sev'] = first_row.catmh_dep_severity_1.tolist()[0]
            chunk.loc[:, 'start_anx'] = first_row.catmh_anx_severity_1.tolist()[0]
            subsets.append(chunk)

    return subsets


def split_half(data) -> (pd.DataFrame, pd.DataFrame):
    """ Split dataframe in half

    Arguments:
        data {pd.DataFrame} -- pandas dataframe

    Returns:
        (pd.DataFrame, pd.DataFrame) -- Dataframes for first and second half
    """
    half = int(data.shape[0]/2)
    h_1 = data.iloc[:half]
    h_2 = data.iloc[half:]
    return h_1, h_2
