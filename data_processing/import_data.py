""" Functions for the importing and initial preprocessing of data
"""
import os
import pandas as pd
from data_processing.load_env import load_env


def import_longitudinal_file(
        file_path: str,
        clean_only: bool,
    ) -> pd.DataFrame:
    data = pd.read_excel(file_path)
    if clean_only:
        last_row = data[data['redcap_event_name_1'] == 'followup_assessmen_arm_1']
        if last_row.empty:
            last_row = data[data['redcap_event_name_2'] == 'followup_assessmen_arm_1']
        return data.iloc[:last_row.index[0]+1]
    return data


def import_all_longitudinal_files(clean_only: bool = False, add_demog: bool = False) -> pd.DataFrame:
    """ Wrapper function to import all longitudinal data files
    
    Keyword Arguments:
        clean_only {bool} -- Only import data from patients
            with demographic information (default: {False})
    
    Returns:
        pd.DataFrame -- concatenated data of particpants
    """
    env = load_env()
    subject_data_dir = os.path.join(
        env['data_root'],
        env['longitudinal_data_folder']
    )
    print('IMPORTING LONGITUDINAL DATA FROM:\n\t' + subject_data_dir)

    files = os.listdir(subject_data_dir)

    if add_demog or clean_only:
        demog_df = import_demographic_file()

    if clean_only:
        print(
            '\t' +
            'Only importing patients with demographic information, and data until end of study'
        )
        subjects = demog_df.subject_id.unique()
        with_demog = [
            f for f in files if f.split('_Migraine')[0] in subjects
        ]
        print(
            '\tRemoved',
            len(files) - len(with_demog),
            'subjects',
            len(with_demog),
            'remain'
        )
        files = with_demog

    file_paths = [os.path.join(subject_data_dir, f) for f in files if f[0] == 'm']
    long_files = [import_longitudinal_file(f, clean_only) for f in file_paths]

    all_data_df = pd.concat(long_files, sort=False)
    all_data_df['Date'] = pd.to_datetime(all_data_df['Date'])
    if add_demog:
        print('\tAdding Demographic information to longitudinal data')
        with_demog = all_data_df.merge(
            demog_df,
            how='inner',
            validate='m:1'
        )
        if with_demog.shape[0] != all_data_df.shape[0]:
            print('\tWARNING - With demog Length:', with_demog.shape[0], 'difference:', with_demog.shape[0] - all_data_df.shape[0])
        return with_demog
        
    return all_data_df

def import_demographic_file() -> pd.DataFrame:
    env = load_env()
    demog_path = env['demographic_file']
    demog = pd.read_excel(demog_path)
    return demog.rename(columns={
        'record_id': 'subject_id'
        })
