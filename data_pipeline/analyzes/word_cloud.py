from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("../../output/output_medium_en.csv", delimiter=";")
df = df.loc[df['trial_type'] == 'slider']
df['transcribed_text'].fillna('', inplace=True)

text = df['transcribed_text'].astype(str).values.sum()
stop_words = ['Thank', 'Thank you', 'Thanks']
STOPWORDS.update(stop_words)
wordcloud = WordCloud(background_color="white").generate(text)

plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")

# Save the plot as a file
plt.savefig("word_cloud.png")

