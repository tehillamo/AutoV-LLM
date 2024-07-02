from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("./output_zero_shot_new_post.csv", delimiter=";")
df = df.loc[df['trial_type'] == 'slider']
df['transcribed_text'].fillna('', inplace=True)

df_modus = df
text = df_modus['transcribed_text'].astype(str).values.sum()
stop_words = ['Thank', 'Thank you', 'Thanks', 'KFNN', 'Kjell', 'Krona', 'Krona Kjell', 'Kjell Krona']
STOPWORDS.update(stop_words)
wordcloud = WordCloud(background_color="white").generate(text)

plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")

# Save the plot as a file
plt.savefig(f"word_clouds/word_cloud.png")

for word_type in ["city", "country", "body"]:
    for modus in ["R0-R0","U0-U0","U0-R0","R1-R0","R0-U1","R1-U0","U1-U0"]:
        #filter df for modus
        df_modus = df.loc[(df['type'] == modus) & (df['word_type'] == word_type)]
        #df_modus = df_modus.loc[df_modus['word_type'] == word_type]
        text = df_modus['transcribed_text'].astype(str).values.sum()
        text = repr(text).encode('ascii',errors='ignore').decode()
        print(word_type, modus)

        STOPWORDS.update(stop_words)
        print(text)
        wordcloud = WordCloud(background_color="white").generate(text)

        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")

        # Save the plot as a file
        plt.savefig(f"word_clouds/word_cloud_{word_type}_{modus}.png")


for modus in ["R0-R0","U0-U0","U0-R0","R1-R0","R0-U1","R1-U0","U1-U0"]:
    #filter df for modus
    df_modus = df.loc[df['type'] == modus]
    text = df_modus['transcribed_text'].astype(str).values.sum()
    STOPWORDS.update(stop_words)
    wordcloud = WordCloud(background_color="white").generate(text)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

    # Save the plot as a file
    plt.savefig(f"word_clouds/word_cloud_{modus}.png")

