import torch
import pandas as pd
from sentence_transformers import SentenceTransformer, util
from preprocessing import preprocessing
import matplotlib.pyplot as plt
import numpy as np
from transformers import pipeline
import warnings

counter = 0


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

def keyword_similarity_zero_shot(df, keywords, threshold = 0.14, finetuned_model = None):
    global counter
    counter = 0
    if finetuned_model is not None:
        pipe = pipeline("text-classification", model=finetuned_model)
    else:
        # Load the zero-shot classification model
        pipe = pipeline(model="facebook/bart-large-mnli")
    df['transcribed_text'].fillna('', inplace=True)
    print(f"{len(df)} entries to classify")
    #df['highest_similarity'] = df['transcribed_text'].apply(lambda x: zero_shot(x, pipe, keywords, threshold))
    
    warnings.filterwarnings('ignore')

    # get all indices where the transcribed_text is not empty
    indices_with_text = df[df['transcribed_text'].str.strip() != ''].index

    # only classify entries with text
    df['highest_similarity'] = [("unknown", 0.0)] * len(df)


    if finetuned_model is not None:
        print("Using finetuned model")
        df.loc[indices_with_text, 'highest_similarity'] = pipe(df.loc[indices_with_text, 'transcribed_text'].astype(str).tolist())
        df.loc[indices_with_text, 'highest_similarity'] = df.loc[indices_with_text, 'highest_similarity'].apply(lambda x: (x["label"], x["score"]))
    else:
        df.loc[indices_with_text, 'highest_similarity'] = pipe(df.loc[indices_with_text, 'transcribed_text'].astype(str).tolist(), candidate_labels=keywords)
        df.loc[indices_with_text, 'highest_similarity'] = df.loc[indices_with_text, 'highest_similarity'].apply(lambda x: (x["labels"][0], x["scores"][0]))

    df.loc[indices_with_text, 'highest_similarity'] = df.loc[indices_with_text, 'highest_similarity'].apply(lambda x: x if x[1] > threshold else ('unknown', x[1]))


    return df

def zero_shot(x, pipe, keywords, threshold = 0.14):
    global counter
    print(f"Zero shot: {counter}")
    counter = counter + 1
    if len(x) == 0:
        return ('unknown', 0)
    result = pipe(x, candidate_labels=keywords)
    return (result['labels'][0], result['scores'][0])

def toTensor(string):
    string = string.replace("\n", "")
    string = string[1:-1].split(" ")
    string_filtered = [x for x in string if x]
    splitted = list(map(lambda x: float(x), string_filtered))
    return torch.tensor(splitted, dtype=torch.float)

def text_classification(df, text_classes, treshold, finetuned_model=None):
    df = preprocessing(df)
    df = keyword_similarity_zero_shot(df, text_classes, treshold, finetuned_model)
    return df

