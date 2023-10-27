from sentence_transformers import SentenceTransformer
import pandas as pd 
from sklearn.decomposition import PCA
import numpy as np
from sklearn.manifold import TSNE

class Embeddings:

    def __init__(self):
        pass

    def create_embeddings(self, df, column, reduce_dimension = True, reduction_algorithm = "PCA", dimension = 3):
        model = SentenceTransformer('all-MiniLM-L6-v2') 
        embeddings = self._embedding(df, column, model)
        if reduce_dimension == False:
            return embeddings
        if reduction_algorithm == "PCA":
            return self._pca(embeddings, f"{column}_embedding", dimension)
        if reduction_algorithm == "TSNE":
            return self._tsne(embeddings, f"{column}_embedding", dimension)
        if reduction_algorithm == "both":
            return self._both(embeddings, f"{column}_embedding", dimension)

    def _embedding(self, df, column, model):
        df[f"{column}_embedding"] = df.apply(lambda row: self._get_embedding(row, column, model), axis=1)
        return df

    def _get_embedding(self, row, column, model):
        embedding = model.encode(row[column])
        return embedding
    
    def _pca(self, df, column, dimension):
        pca = PCA(n_components=dimension)
        vals = np.asarray([np.array(x) for x in df[column].values])
        pca.fit(vals)
        df[f"{column}_reduced_pca"] = df.apply(lambda row: pca.transform(np.asarray(row[column].reshape(1, -1)))[0], axis=1)
        return df


    def _tsne(self, df, column, dimension):
        vals = np.asarray([np.array(x) for x in df[column].values])
        tsne = TSNE(n_components=dimension, learning_rate='auto', init='random', perplexity=5)
        transformed = tsne.fit_transform(vals)
        transformed = [np.asarray(x) for x in transformed]
        print(transformed)
        #df[f"{column}_reduced_tsne"] = np.asarray(transformed)
        df[f"{column}_reduced_tsne"] = transformed
        return df
    
    def _both(self,df ,column, dimension):
        n_comp = min(dimension, df.shape[0], df.shape[1])
        pca = PCA(n_components=n_comp)
        vals = np.asarray([np.array(x) for x in df[column].values])
        transformed_pca = pca.fit_transform(vals)
        tsne = TSNE(n_components=dimension, learning_rate='auto', init='random', perplexity=5)
        transformed_tsne = tsne.fit_transform(transformed_pca)
        transformed_tsne = [np.asarray(x) for x in transformed_tsne]
        df[f"{column}_reduced_both"] = transformed_tsne
        return df
        

    

        
