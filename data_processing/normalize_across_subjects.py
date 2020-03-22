""" attempts to normalize data of different types for cross-subject comparison
"""
import pandas as pd

def normalize_outgoing_calls(
        data: pd.DataFrame,
    ) -> pd.DataFrame:
    mean_calls = pd.DataFrame(
        data.groupby('subject_id')['outgoing_calls'].mean()
    ).reset_index().rename(columns={'outgoing_calls': 'avg_calls'})
    with_avg = data.merge(
        mean_calls,
        how='inner',
        validate='m:1'
    )
    if with_avg.shape[0] != data.shape[0]:
        raise ValueError('Output not same length as input')
    with_avg['norm_outgoing_calls'] = with_avg['outgoing_calls']/with_avg['avg_calls']
    return with_avg

