""" Functions to reshape dataframes
"""
import re
import pandas as pd
import data_processing.map_data_dict as map_data


def melt_occurrances(
        col_base: str,
        data: pd.DataFrame,
        keep_cols: list = [],
) -> pd.DataFrame:
    """ Reshape columns of format col_base_n to long format
    Example: mbrep_pain_sev_1, ..., mbrep_pain_sev_4 would
    be turned to mbrep_pain
    
    Arguments:
        col_base {str} -- base of column before _[int]
        data {pd.DataFrame} -- pandas data frame
    
    Keyword Arguments:
        keep_cols {list} -- data columns to retain after melt
            (default: {[]})
    
    Returns:
        pd.DataFrame -- melted dataframe
    """
    loc_cols = [
        col for col in data.columns
        if re.match(col_base+r'_\d+$', col)
    ]
    melt_df = data[['Date', 'subject_id'] + loc_cols + keep_cols]

    melt_df = melt_df.melt(
        id_vars=['Date', 'subject_id'] + keep_cols,
        value_vars=loc_cols,
        var_name='n',
        value_name=col_base
    )
    melt_df['n'] = melt_df['n'].str.split('_').str[-1].astype(int)
    return melt_df.dropna()


def explode_list_col(col_base, data, map_to_str):
    data[col_base] = data[col_base].str.split(',')
    exploded = data.explode(column=col_base)
    exploded[col_base] = exploded[col_base].astype(float)
    if map_to_str:
        exploded[col_base + '_str'] = map_data.map_value_from_data_dict(
            exploded,
            col_base
        )
    return exploded
