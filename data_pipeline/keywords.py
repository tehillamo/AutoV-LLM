import pandas as pd
from keybert import KeyBERT
import os

def extract_keywords_keybert(df, column, output_column):
    kw_model = KeyBERT()
    df[output_column] = ''
    df = df[column].apply(lambda c: kw_model.extract_keywords(str(c)))
    df.to_csv("./output.csv", sep=';', index=False)


df = pd.read_csv("../output/output_medium_en.csv", delimiter=";")
extract_keywords_keybert(df, "transcribed_text", "keywords")


