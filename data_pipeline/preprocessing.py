import json
import torch

def get_type_from_pair(pair):
    pair = pair.replace("'", '"')
    json_data = json.loads(pair)
    pair_1 = list(json_data['pairs_1'].keys())[0]
    pair_2 = list(json_data['pairs_2'].keys())[0]
    return f'{pair_1}-{pair_2}'

def convert_to_tensor(df, column):
    df[column] = df[column].apply(lambda x: toTensor(x))
    return df


def toTensor(string):
    string = string.replace("\n", "")
    string = string[1:-1].split(" ")
    string_filtered = [float(x) for x in string if x]
    #splitted = list(map(lambda x: float(x), string_filtered))
    return string_filtered



def preprocessing(df):
    df = df.loc[df['trial_type'] == 'slider']
    df['type'] = df['pair'].apply(lambda c: get_type_from_pair(c))
    df = df[df["transcribed_text"].str.contains('Thank you') == False]

    #df = convert_to_tensor(df, 'embedding')
    return df








        





