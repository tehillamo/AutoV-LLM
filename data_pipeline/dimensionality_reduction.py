import pandas as pd 
from sklearn.decomposition import PCA
import numpy as np
from sklearn.manifold import TSNE


def reduce(df, column, reduction_algorithm = "PCA", dimension = 3, new_column_name = None, per_participant = False):
    if per_participant:
        participants = df['uuid'].unique()
        for participant in participants:
            print(f"Reducing dimensionality for participant {participant} using {reduction_algorithm}...")
            df_participant = df[df['uuid'] == participant]
            df_participant = reduce(df_participant, column, reduction_algorithm, dimension, new_column_name, per_participant=False)
            df.loc[df['uuid'] == participant, :] = df_participant
        return df
    
    if new_column_name == None:
        new_column_name = f"{column}_reduced_{reduction_algorithm}"
    if reduction_algorithm == "PCA":
        return pca(df, column, dimension, new_column_name)
    if reduction_algorithm == "TSNE":
        return tsne(df, column, dimension, new_column_name)
    if reduction_algorithm == "both":
        return both(df, column, dimension, new_column_name)

def pca(df, column, dimension, new_column_name):
    pca = PCA(n_components=dimension)
    vals = np.asarray([np.array(x) for x in df[column].values])
    pca.fit(vals)
    print(f"Explained variance from PCA: {pca.explained_variance_ratio_}")
    for i in range(dimension):
        df[f"{new_column_name}_{i+1}"] = df.apply(lambda row: pca.transform(np.asarray(row[column].reshape(1, -1)))[0][i], axis=1)
    return df


def tsne(df, column, dimension, new_column_name):
    vals = np.asarray([np.array(x) for x in df[column].values])
    tsne = TSNE(n_components=dimension, learning_rate='auto', init='random', perplexity=5)
    transformed = tsne.fit_transform(vals)
    transformed = [np.asarray(x) for x in transformed]
    df[f'{new_column_name}_tmp'] = transformed
    for i in range(dimension):
        df[f"{new_column_name}_{i+1}"] = df.apply(lambda row: row[f'{new_column_name}_tmp'][i], axis=1)
    return df.drop(f'{new_column_name}_tmp', axis=1)

def both(df ,column, dimension, new_column_name):
    n_comp = min(dimension, df.shape[0], df.shape[1])
    pca = PCA(n_components=n_comp)
    vals = np.asarray([np.array(x) for x in df[column].values])
    transformed_pca = pca.fit_transform(vals)
    tsne = TSNE(n_components=dimension, learning_rate='auto', init='random', perplexity=5)
    transformed_tsne = tsne.fit_transform(transformed_pca)
    transformed_tsne = [np.asarray(x) for x in transformed_tsne]
    df[f'{new_column_name}_tmp'] = transformed_tsne
    for i in range(dimension):
        df[f"{new_column_name}_{i+1}"] = df.apply(lambda row: row[f'{new_column_name}_tmp'][i], axis=1)
    return df.drop(f'{new_column_name}_tmp', axis=1)
    



    
