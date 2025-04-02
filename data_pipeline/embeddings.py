from sentence_transformers import SentenceTransformer

def create_embeddings(df, column, new_column_name = None, model_name = None):
    if model_name is None:
        model_name = 'all-MiniLM-L6-v2'
    else:
        print(f"Using SentenceBERT model: {model_name}")
    model = SentenceTransformer(model_name) 
    if new_column_name == None:
        new_column_name = f"{column}_embedding"
    embeddings = _embedding(df, column, model, new_column_name)
    return embeddings

def _embedding(df, column, model, new_column_name):
    df[column] = df[column].astype(str)
    df[new_column_name] = df.apply(lambda row: _get_embedding(row, column, model), axis=1)
    return df

def _get_embedding( row, column, model):
    embedding = model.encode(row[column])
    return embedding

    



    
