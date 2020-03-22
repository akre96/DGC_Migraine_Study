""" Functions to map items from data dictionary to values in data file
"""
import re
import pandas as pd
from data_processing.load_env import load_env

def map_value_from_data_dict(
        data: pd.DataFrame,
        value_col: str,
    ) -> pd.Series:
    """ Maps data in value col based on data dictionary from environment file

    Arguments:
        data {pd.DataFrame} -- input data
        value_col {str} -- column with data to map

    Raises:
        ValueError: Could not find mapping dictionary for value_col
        ValueError: More than 1 mapping dictionary found for value_col

    Returns:
        pd.Series -- mapped series from value columns
    """
    env = load_env()
    data_dict = pd.read_csv(env['data_dictionary_file'])

    dict_field = value_col
    if re.match(r'\w+_\d+$', value_col):
        dict_field = '_'.join(value_col.split('_')[:-1])
        print('Multi-value data detected, searching data dictionary for', dict_field)

    val_df = data_dict.loc[
        data_dict['Variable / Field Name'] == dict_field,
        'Choices, Calculations, OR Slider Labels'
    ]
    if val_df.empty:
        raise ValueError('Value column not found in data dictionary: ' + dict_field)
    if len(val_df) != 1:
        print(val_df)
        raise ValueError('More than 1 data dictionary item matched')

    dict_str = list(val_df)[0]
    map_dict = {
        int(val.split(', ')[0]): ', '.join(val.split(', ')[1:])
        for val in dict_str.split(' | ')
    }
    return data[value_col].map(map_dict)
