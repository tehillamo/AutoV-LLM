import pandas as pd
import re

def resolve_slider_items(df):
    df['slider_items'] = ''
    df['slider_items'] = df.apply(lambda row: get_slider_items(row), axis = 1)
    return df

def get_slider_items(row):
    if row['trial_type'] != "slider":
        return "undefined"
    
    pattern = re.compile(r'<p>(.*?)<\/p>')
    matches = pattern.findall(row['stimulus'])[1:]

    return {
        'left': matches[0],
        'right': matches[1]
    }

def get_trial_type(df):
    df['trial_type'] = ''
    df['trial_type'] = df['stimulus'].apply(lambda x: trial_type(x))
    return df

def trial_type(x):
    if "Use the response scale to indicate which word you remember, and how confident you are in your response." in x:
        return "slider"
    if ">+<" in x:
        return "cross"
    if "font-size: 60px;font-family: Monospace" in x:
        return "word"
    if "font-size:60px;font-family: Monospace" in x:
        return "number"
    return "else"


