from keybert import KeyBERT
import pandas as pd

def extract_keywords_keybert(df, column, output_column, top_n_keywords=5):
    kw_model = KeyBERT()
    df[output_column] = None
    indices_with_text = df[df[column].str.strip() != ''].index
    
    keywords = kw_model.extract_keywords(df.loc[indices_with_text, column].tolist(), top_n=top_n_keywords)

    # If there's only one document, make sure keywords is a list of lists
    if len(keywords) > 0 and isinstance(keywords[0], tuple):
        keywords = [keywords]  # Wrap in a list

    df.loc[indices_with_text, output_column] = pd.Series(keywords, index=indices_with_text)
    return df




