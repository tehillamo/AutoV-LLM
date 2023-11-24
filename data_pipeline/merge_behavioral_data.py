import os 
import json
from utils import get_uuids
import pandas as pd


def merge_behavioral_data(df, path_ressources, columns):
    """
    Merges behavioral data from multiple files into a DataFrame.

    Parameters:
    - df (DataFrame): The DataFrame to merge the data into.
    - path_ressources (str): The path to the directory containing the data files.
    - columns (list): A list of column names to merge the data into.

    Returns:
    - df (DataFrame): The DataFrame with the merged data.
    """
    for column in columns:
        df[column] = ''

    uuids = get_uuids(path_ressources)

    for uuid in uuids:
        with open(os.path.join(path_ressources, uuid,  'trial_data.txt'), 'r') as file:
            data = file.read().replace('\n', '')
            json_data = json.loads(data)

            for trial in json_data:
                for column in columns:
                    # check if column exists in trial
                    if column not in trial.keys():
                        data = "undefined"
                    else:
                        data = trial[column]
                    # convert to string if needed
                    if type(data) is dict or type(data) is list:
                        data = str(data)
                    df.loc[(df['uuid'] == uuid) & (df['trial_number'] == trial['trial_index']), column] = data

    return df

