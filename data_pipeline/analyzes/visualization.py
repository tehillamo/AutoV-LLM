import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import os
import random
from adjustText import adjust_text
import matplotlib.patches as mpatches


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
        plt.savefig(os.path.join('./images', f'{name}_{label}.svg'), bbox_inches="tight", dpi=600)   
        plt.clf()
        fig.clf()

def embedding_simiar_word(df, x_column, y_column,  name="embedding_similar_word", alpha = 0.8, standardize = False):
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

    ticks = [17, 15,13,11,9,7,5,3,1]

    words = [      
        "definitely", 
        "certain",
        "sure",
        "i know",
        "pretty sure",
        "kind of",
        "assume that",
        "unsure",
        "cannot be"
    ]

    words.reverse()
    ticks.reverse()

    for label in set(class_labels):
        fig, ax = plt.subplots()
        all = df.loc[df['type'] == label]
        x = all[x_column].values
        y = all[y_column].values

        if standardize:
            x = (x - x.mean()) / x.std()
            y = (y - y.mean()) / y.std()

        word_value = list(map(lambda x: word_to_value[x], all['most_similar_word'].values))

        p2 = ax.scatter(x, y, alpha = alpha, c=word_value, vmin=1, vmax=17)

        # Add labels and legend
        plt.xlabel('Embedding Dimension 1')
        plt.ylabel('Embedding Dimension 2')
        plt.title(label)


        #plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1))
        cbar = fig.colorbar(p2, ax=ax, label='Confidence Level')
        cbar.set_ticks(ticks)
        cbar.set_ticklabels(words)
        cbar.ax.set_ylim(1, 17)
        # Save the figure as an image
        plt.savefig(os.path.join('./images/gradient/', f'{name}_{label}.png'), bbox_inches="tight", dpi=600)   
        plt.clf()
        fig.clf()

def embedding_simiar_word_no_gradient(df, x_column, y_column,  name="embedding_similar_word", alpha = 0.8, standardize = False):
    class_labels = df['type']  

    word_to_color = {
        "definitely": "lime",
        "absolutely": "green",
        "certain": "mediumseagreen",
        "confidence": "springgreen",
        "suspect that must": "forestgreen",
        "sure": "darkgreen",
        "im positive": "seagreen",
        "i know": "limegreen",
        "i remember": "chartreuse",
        "pretty sure": "gold",
        "maybe": "khaki",
        "kind of": "darkgoldenrod",
        "i think so": "orange",
        "assume that": "coral",
        "it feels like": "orangered",
        "unsure": "peru",
        "uncertain": "firebrick",
        "cannot be": "red"
    }

    words_all = [
        "definitely",
        "absolutely",
        "certain",
        "confidence",
        "suspect that must",
        "sure", 
        "im positive", 
        "i know", 
        "i remember", 
        "pretty sure", 
        "maybe", 
        "kind of", 
        "i think so", 
        "assume that", 
        "it feels like", 
        "unsure", 
        "uncertain", 
        "cannot be"
    ]

    for label in set(class_labels):
        fig, ax = plt.subplots()
        all = df.loc[df['type'] == label]
        x = all[x_column].values
        y = all[y_column].values

        if standardize:
            x = (x - x.mean()) / x.std()
            y = (y - y.mean()) / y.std()

        words = all['most_similar_word'].values

        legend_labels = []

        for word_label in set(words):
            indices = words == word_label
            plt.scatter(x[indices], y[indices], alpha = alpha, c=word_to_color[word_label])
        
        for word_label in words_all:
            legend_labels.append(mpatches.Patch(color=word_to_color[word_label], label=word_label))

        

        #plt.scatter(x, y, alpha = alpha, c=word_value, vmin=1, vmax=17, label=all['most_similar_word'].values)

        # Add labels and legend
        plt.xlabel('Embedding Dimension 1')
        plt.ylabel('Embedding Dimension 2')
        plt.title(label)


        plt.legend(loc='upper left', bbox_to_anchor=(1.02, 1), handles=legend_labels)
        # Save the figure as an image
        plt.savefig(os.path.join('./images/color_per_label', f'{name}_{label}.png'), bbox_inches="tight", dpi=600)   
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


df = pd.read_csv('./output_zero_shot_new_post.csv', delimiter=';')


df['most_similar_word'] = df['highest_similarity'].str.extract(r"\('([^']*)',\s*([^)]*)\)")[0]
df['similarity_score'] = df['highest_similarity'].str.extract(r"\('([^']*)',\s*([^)]*)\)")[1]


for mode in ["city", "country", "body"]:
    df_mode = df.loc[df['word_type'] == mode]   
    embedding_simiar_word_no_gradient(df_mode, "embedding_reduced_tsne_1", "embedding_reduced_tsne_2", name=f"embedding_similar_word_tsne_{mode}", standardize=True)
    embedding_simiar_word_no_gradient(df_mode, "embedding_reduced_pca_1", "embedding_reduced_pca_2", name=f"embedding_similar_word_pca_{mode}", standardize=True)
    embedding_simiar_word_no_gradient(df_mode, "embedding_reduced_both_1", "embedding_reduced_both_2", name=f"embedding_similar_word_both_{mode}", standardize=True)
    embedding_simiar_word(df_mode, "embedding_reduced_tsne_1", "embedding_reduced_tsne_2", name=f"embedding_similar_word_tsne_{mode}", standardize=True)
    embedding_simiar_word(df_mode, "embedding_reduced_pca_1", "embedding_reduced_pca_2", name=f"embedding_similar_word_pca_{mode}", standardize=True)
    embedding_simiar_word(df_mode, "embedding_reduced_both_1", "embedding_reduced_both_2", name=f"embedding_similar_word_both_{mode}", standardize=True)

embedding_simiar_word_no_gradient(df, "embedding_reduced_tsne_1", "embedding_reduced_tsne_2", name="embedding_similar_word_tsne", standardize=True)
embedding_simiar_word_no_gradient(df, "embedding_reduced_pca_1", "embedding_reduced_pca_2", name="embedding_similar_word_pca", standardize=True)
embedding_simiar_word_no_gradient(df, "embedding_reduced_both_1", "embedding_reduced_both_2", name="embedding_similar_word_both", standardize=True)
embedding_simiar_word(df, "embedding_reduced_tsne_1", "embedding_reduced_tsne_2", name="embedding_similar_word_tsne", standardize=True)
embedding_simiar_word(df, "embedding_reduced_pca_1", "embedding_reduced_pca_2", name="embedding_similar_word_pca", standardize=True)
embedding_simiar_word(df, "embedding_reduced_both_1", "embedding_reduced_both_2", name="embedding_similar_word_both", standardize=True)



