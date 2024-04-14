import pandas as pd
import numpy as np
import ast, json


words_cities = ["sydney", "los angeles", "bucharest", "chicago", "auckland",
                      "london", "tokyo", "delhi", "mumbai", "shanghai", "moscow", 
                      "seoul", "new york", "hanoi", "bangkok", "berlin", "madrid", 
                      "amsterdam", "athens", "baghdad", "beirut", "cairo", "budapest",
                      "copenhagen", "dublin", "helsinki", "jakarta", "jerusalem",     
                      "kiev", "lisbon", "manila", "oslo", "ottawa", "paris","prague", 
                      "rome", "stockholm", "taipei", "jordan", "istanbul", "toronto",
                      "munich", "kyoto", "seattle", "beijing", "barcelona", "brussels", "dubai"]

words_countries = ["canada", "france", "mexico", "england", "germany", 
                      "spain", "italy", "china", "japan", "russia", 
                      "brazil", "ireland", "australia", "iraq", "finland", 
                      "argentina", "india", "switzerland", "sweden", "africa", 
                      "chile", "britain", "iran", "portugal", "greece", 
                      "scotland", "egypt", "israel", "peru", "belgium", 
                      "korea", "norway", "denmark", "lebanon", "malaysia", 
                      "poland", "taiwan", "romania", "serbia", "singapore", 
                      "indonesia", "taiwan", "turkey", "vietnam", "thailand", 
                      "philippines", "pakistan", "netherlands"]

words_body = ["leg", "arm", "nail", "muscle", "feet", "finger", "head", 
                  "toe", "eye", "hand", "nose", "ear", "mouth", "stomach", 
                  "heart", "knee", "neck", "brain", "hair", "elbow", 
                  "shoulder", "chest", "spine", "hip", "lip", "thigh", 
                  "ankle", "face", "liver", "lung", "tongue", "teeth", 
                  "torso", "wrist", "bone", "palm", "forearm", "eyebrow", 
                  "throat", "earlobe", "jaw", "nostril", "forehead", 
                  "knuckle", "heel", "skin", "cheeks", "eyelid"]

def word_type(trial_number):
    if trial_number in range(80, 200):
        return "city"
    if trial_number in range(200, 370):
        return "body"
    if trial_number in range(400, 580):
        return "country"
    

def fix(row):
    pass

def get_left_word(pair):
    key = list(pair['pairs_1'].keys())[0]
    return pair['pairs_1'][key]

def get_right_word(pair):
    key = list(pair['pairs_2'].keys())[0]
    return pair['pairs_2'][key]


df = pd.read_csv('./output_zero_shot_new_post.csv', delimiter=';')

df = df[df['uuid'] == '03e6a84d-0067-4677-973f-27c8c56efa04']

df['pair'] = df['pair'].str.replace("'",'"')
df['pair'] = df['pair'].apply(json.loads)

# match with regex
df['left_word'] = df['pair'].apply(get_left_word)
df['right_word'] = df['pair'].apply(get_right_word)

# filter for word_type=country
# U0
df_country = df[((df['type'] == 'U0-U0') |  (df['type'] == 'U0-R0') )]
new_words = df_country['left_word'].to_numpy()
df_country = df[((df['type'] == 'U0-U0') | (df['type'] == 'R1-U0') | (df['type'] == 'U1-U0') )]
new_words = np.concatenate((new_words,df_country['right_word'].to_numpy()))
print(new_words)

# U1
df_country = df[((df['type'] == 'U1-U0') )]
old_words = df_country['left_word'].to_numpy()
df_country = df[((df['type'] == 'R0-U1') )]
old_words = np.concatenate((old_words,df_country['right_word'].to_numpy()))
print(old_words)

to_decide = df[(df['word_type'] == 'country') & (df['type'] == 'U0-U0')]

to_decide['is_U1-U0'] = to_decide['left_word'].apply(lambda x: x in old_words)
to_decide['is_U1-U0'] = to_decide['right_word'].apply(lambda x: x in new_words)
print(to_decide['left_word'])
print(to_decide['right_word'])


# parse as json object




#df['word_type'] = df['trial_number'].apply(word_type)
#print(df['word_type'].value_counts())
#print(df['word_type'])

#save file
#df.to_csv('./output_zero_shot_new_post_.csv', sep=';', index=False)

