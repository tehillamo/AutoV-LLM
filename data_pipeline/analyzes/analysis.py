import torch
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from preprocessing import preprocessing
import matplotlib.pyplot as plt
import numpy as np
from transformers import pipeline


def keyword_similarity(df):
    keywords = ["certain", "uncertain", "sure", "unsure", "pretty sure", "maybe", "kind of", "i think so", "it feels like", "assume that", "definitely", "absolutely", "confidence", "suspect that must", "cannot be", "im positive", "i know", "i remember"]
    columns = [f'{keyword}_similarity' for keyword in keywords]
    model = SentenceTransformer('all-MiniLM-L6-v2') 
    keywords_embedding = list(map(lambda x: model.encode(x, convert_to_tensor=True).cpu(), keywords))

    for i, keyword in enumerate(keywords):
        df[f'{keyword}_similarity'] = df['embedding'].apply(lambda x: util.cos_sim(torch.tensor(x), keywords_embedding[i])[0][0].item())
    tmp = df[columns]
    df['highest_similarity'] = tmp.idxmax(axis=1)
    df['highest_similarity'] = df['highest_similarity'].apply(lambda x: x.replace('_similarity',''))
    return df, keywords

def keyword_similarity_zero_shot(df):
    threshold = 0.14
    keywords = ["certain", "uncertain", "sure", "unsure", "pretty sure", "maybe", "kind of", "i think so", "it feels like", "assume that", "definitely", "absolutely", "confidence", "suspect that must", "cannot be", "im positive", "i know", "i remember"]
    pipe = pipeline(model="facebook/bart-large-mnli")
    df['transcribed_text'].fillna('', inplace=True)
    df['highest_similarity'] = df['transcribed_text'].apply(lambda x: zero_shot(x, pipe, keywords, threshold))
    return df

def zero_shot(x, pipe, keywords, threshold = 0.14):
    if len(x) == 0:
        return 'unknown'
    result = pipe(x, candidate_labels=keywords)
    if result['scores'][0] > threshold:
        return result['labels'][0]
    else:
        return 'unknown'

def toTensor(string):
    string = string.replace("\n", "")
    string = string[1:-1].split(" ")
    string_filtered = [x for x in string if x]
    splitted = list(map(lambda x: float(x), string_filtered))
    return torch.tensor(splitted, dtype=torch.float)


df = pd.read_csv('../../output/output_medium_en.csv', delimiter=';')
print('Start preprocessing')
df = preprocessing(df)
print('length df ', len(df))
print('Finished preprocessing')
print('Start keyword similarity')
df = keyword_similarity_zero_shot(df)

cols =  ['transcribed_text', 'highest_similarity'] 
df.to_csv("./output_zero_shot.csv", sep=';', index=False, columns=cols)