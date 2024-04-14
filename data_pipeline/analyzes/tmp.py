import pandas as pd

df = pd.read_csv('./output_zero_shot.csv', delimiter=';')

empty_count = df['transcribed_text'].isnull().sum() + (df['transcribed_text'] == ' ').sum()

# count number of times transcribed_text is empty or is the empty string


print(empty_count)
