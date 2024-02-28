from preprocessing import preprocessing
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import os
import random
from adjustText import adjust_text


def embedding_type(df, x_column, y_column, name="embedding_type.png", alpha = 0.8):
    color_mapping = {
        "R0-R0": 'red',
        "U0-U0": 'blue',
        "U0-R0": 'green',
        "R1-R0": 'orange',
        "R0-U1": 'pink',
        "R1-U0": 'brown',
        "U1-U0": 'gray',
    }

    X = df[x_column]
    Y = df[y_column]
    class_labels = df['type']
    
    for label in set(class_labels):
        indices = class_labels == label
        plt.scatter(X[indices], Y[indices], label=label, color=color_mapping[label], alpha = alpha)
    # Add labels and legend
    plt.xlabel('Embedding Dimension 1')
    plt.ylabel('Embedding Dimension 1')
    plt.legend()

    # Save the figure as an image
    plt.savefig(os.path.join('./images', name))   
    plt.clf()

def embedding_text(df, x_column, y_column, text_column, name="embedding_type", alpha = 0.8):
    class_labels = df['type']  

    for label in set(class_labels):
        fig, ax = plt.subplots()
        texts = []
        participants = set(df['uuid'])
        for participant in participants:
            all = df.loc[(df['uuid'] == participant) & (df['type'] == label)]
            x = all[x_column].values
            y = all[y_column].values
            text = all[text_column].values

            plt.scatter(x, y, alpha = alpha, label=participant)

            for i, txt in enumerate(x):
                if random.uniform(0,1) > 0.9 and len(text[i]) < 100:
                    texts.append(plt.text(x[i], y[i], text[i]))
                    #ax.annotate(text[i], (x[i], y[i]))
            # Add labels and legend
        plt.xlabel('Embedding Dimension 1')
        plt.ylabel('Embedding Dimension 2')
        plt.title(label)
        # Save the figure as an image
        adjust_text(texts, only_move={'points':'y', 'texts':'y'}, arrowprops=dict(arrowstyle="->", color='k', lw=0.5))
        plt.savefig(os.path.join('./images', f'{name}_{label}.svg'), bbox_inches="tight")   
        plt.clf()
        fig.clf()

def embedding_simiar_word(df, x_column, y_column,  name="embedding_similar_word", alpha = 0.8):
    class_labels = df['type']  

    word_to_value = {
        "definitely":17, 
        "absolutely":16, 
        "certain":15, 
        "confidence": 14.5,
        "suspect that must": 14,
        "sure":13 , 
        "im positive":12, 
        "i know":11, 
        "i remember":10, 
        "pretty sure":9, 
        "maybe":8, 
        "kind of":7, 
        "i think so":6, 
        "assume that":5, 
        "it feels like":4, 
        "unsure":3, 
        "uncertain":2, 
        "cannot be":1
    }

    words = [      
        "definitely", 
        "certain", 
        "suspect that must",
        #"im positive",  
        "i remember", 
        "maybe" ,
        "i think so" ,
        "it feels like" ,
        "uncertain",
        "uncertain"]
    words.reverse()

    for label in set(class_labels):
        fig, ax = plt.subplots()
        all = df.loc[df['type'] == label]
        x = all[x_column].values
        y = all[y_column].values
        word_value = list(map(lambda x: word_to_value[x], all['highest_similarity'].values))

        p2 = ax.scatter(x, y, alpha = alpha, c=word_value)

        # Add labels and legend
        plt.xlabel('Embedding Dimension 1')
        plt.ylabel('Embedding Dimension 2')
        plt.title(label)


        #plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
        cbar = fig.colorbar(p2, ax=ax, label='Confidence Level')
        cbar.set_ticklabels(words)
        # Save the figure as an image
        plt.savefig(os.path.join('./images', f'{name}_{label}.svg'), bbox_inches="tight")   
        plt.clf()
        fig.clf()

def embedding_type_3d(df, x_column, y_column, z_column, name="embedding_type.png", x = None, y = None, z = None):
    color_mapping = {
        "R0-R0": 'red',
        "U0-U0": 'blue',
        "U0-R0": 'green',
        "R1-R0": 'orange',
        "R0-U1": 'pink',
        "R1-U0": 'brown',
        "U1-U0": 'gray',
    }

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    X = df[x_column]
    Y = df[y_column]
    Z = df[z_column]
    class_labels = df['type']
    print(set(class_labels))
    for label in set(class_labels):
        indices = class_labels == label
        ax.scatter(X[indices], Y[indices], Z[indices], label=label, color=color_mapping[label], marker='o')
    # Add labels and legend
    ax.set_xlim(x)
    ax.set_ylim(y)
    ax.set_zlim(z)

    ax.set_xlabel('X Label')
    ax.set_ylabel('Y Label')
    ax.set_zlabel('Z Label')
    plt.legend()

    # Save the figure as an image
    plt.savefig(os.path.join('./images', name))   
    plt.clf()

def clustering(df, n_clusters=3):
    X = df['embedding'].to_numpy()
    X = np.array(list(map(lambda x: np.array(x), X)))
    kmeans = KMeans(n_clusters=n_clusters)
    kmeans.fit(X)
    labels = kmeans.predict(X)
    plt.scatter(df['embedding_reduced_1'], df['embedding_reduced_2'], c=labels, cmap='viridis')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.savefig('clustering.png')
    plt.clf()

""" df = pd.read_csv('../../output/output_all.csv', delimiter=';')
df = preprocessing(df) """
#embedding_type(df)
#Explained variance from PCA: [0.23471752 0.05519923]
#embedding_type_3d(df, "embedding_reduced_pca_1", "embedding_reduced_pca_2", "embedding_reduced_pca_3", name="embedding_type_pca.png", x = [-0.4,-0.2], y= [0,0.5] ,z = [-0.04,0])
""" embedding_type_3d(df, "embedding_reduced_pca_1", "embedding_reduced_pca_2", "embedding_reduced_pca_3", name="embedding_type_pca.png")
embedding_type_3d(df, "embedding_reduced_tsne_1", "embedding_reduced_tsne_2", "embedding_reduced_tsne_3", name="embedding_type_tsne.png")
embedding_type_3d(df, "embedding_reduced_both_1", "embedding_reduced_both_2", "embedding_reduced_both_3", name="embedding_type_both.png") """
#clustering(df, n_clusters=2)

""" embedding_type(df, "embedding_reduced_pca_1", "embedding_reduced_pca_2", name="embedding_type_pca.png")
embedding_type(df, "embedding_reduced_tsne_1", "embedding_reduced_tsne_2", name="embedding_type_tsne.png")
embedding_type(df, "embedding_reduced_both_1", "embedding_reduced_both_2", name="embedding_type_both.png") """
#embedding_text(df, "embedding_reduced_pca_1", "embedding_reduced_pca_2", "transcribed_text", name="embedding_type_pca")
#embedding_text(df, "embedding_reduced_tsne_1", "embedding_reduced_tsne_2", "transcribed_text", name="embedding_type_tsne")

df_new = pd.read_csv('./output.csv', delimiter=';')
#df_new = preprocessing(df_new)
embedding_simiar_word(df_new, "embedding_reduced_tsne_1", "embedding_reduced_tsne_2", name="embedding_similar_word_tsne")
#embedding_text(df, "embedding_reduced_both_1", "embedding_reduced_both_2", "transcribed_text", name="embedding_type_both")
