from transformers import pipeline
import pandas as pd

def keyword_similarity_zero_shot(df):
    threshold = 0.14
    keywords = ["certain", "uncertain", "sure", "unsure", "pretty sure", "maybe", "kind of", "i think so", "it feels like", "assume that", "definitely", "absolutely", "confidence", "suspect that must", "cannot be", "im positive", "i know", "i remember"]
    pipe = pipeline(model="facebook/bart-large-mnli")
    df['transcribed_text'].fillna('', inplace=True)
    df['highest_similarity'] = zero_shot(df['transcribed_text'].values, pipe, keywords, threshold)
    return df

def zero_shot(x, pipe, keywords, threshold = 0.14):
    if len(x) == 0:
        return 'unknown'
    result = pipe(x, candidate_labels=keywords)
    if result['scores'][0] > threshold:
        return result['labels'][0]
    else:
        return 'unknown'
    

def zero_shot(x, pipe, keywords, threshold = 0.14):
    res = []
    if len(x) == 0:
        return 'unknown'
    print(x)
    result = pipe(x, candidate_labels=keywords)
    print(result)

    for i in range(len(result['scores'])):
        if result['scores'][i] > threshold:
            res.append(result['labels'][i])
        else:
            res.append('unknown')
    
    print(res)
    

df = pd.DataFrame(['maybe test', 'certain', 'sure'], columns=['transcribed_text'])
print(keyword_similarity_zero_shot(df))