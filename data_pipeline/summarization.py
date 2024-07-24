from transformers import pipeline


def summarize(df, max_length=130, min_length=30):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    df['summary'] = ''
    df['summary'] = summarizer(df['transcribed_text'].astype(str).tolist(), max_length=max_length, min_length=min_length, do_sample=False)
    df['summary'] = df['summary'].apply(lambda x: x['summary_text'])
    return df


    

    

        
