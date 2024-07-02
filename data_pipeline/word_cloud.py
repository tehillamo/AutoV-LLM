from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

def generate_word_cloud(text, stop_words, output_dir):
    stop_words = ['Thank', 'Thank you', 'Thanks']
    text = repr(text).encode('ascii',errors='ignore').decode()

    STOPWORDS.update(stop_words)
    print(text)
    wordcloud = WordCloud(background_color="white").generate(text)

    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

    # Save the plot as a file
    plt.savefig(f"{output_dir}/word_cloud.png")