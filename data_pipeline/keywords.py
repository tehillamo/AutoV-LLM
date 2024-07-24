import pandas as pd
from keybert import KeyBERT
import os

def extract_keywords_keybert(df, column, output_column):
    kw_model = KeyBERT()
    df[output_column] = ''
    df[output_column] = kw_model.extract_keywords(df[column])
    return df




