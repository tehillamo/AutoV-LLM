from sentence_transformers import SentenceTransformer

def create_embeddings(df, column, new_column_name = None):
    model = SentenceTransformer('all-MiniLM-L6-v2') 
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

    



    
