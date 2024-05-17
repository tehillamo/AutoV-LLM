import argparse
import os
from speech2text import transcribe
from embeddings import create_embeddings
from dimensionality_reduction import reduce
from merge_behavioral_data import merge_behavioral_data
from custom_scripts import resolve_slider_items, get_trial_type
from text_classification import text_classification
import random
import json
import pandas as pd
#"text_classes": ["certain", "uncertain", "sure", "unsure", "pretty sure", "maybe", "kind of", "i think so", "it feels like", "assume that", "definitely", "absolutely", "confidence", "suspect that must", "cannot be", "im positive", "i know", "i remember"]

def main():
    print("Starting data pipeline...")
    with open('./config.json') as handle:
        config = json.loads(handle.read())
        
    print(config)

    random.seed(543547)

    if config['transcribe_text']:
        print("Transcribing audio...")
        df = transcribe(config['input_path'], config['transcription_model'])
    else:
        df = pd.read_csv(config['input_path'], sep=';')
        if 'transcribed_text' not in df.columns:
            raise ValueError('"transcribed_text" column not found in input file!')
        
    if config['calculate_text_embeddings']:
        print("Calculating text embeddings...")
        df = create_embeddings(df, "transcribed_text", new_column_name = "embedding")

    if config["dimensionality_reduction"]:
        print("Reducing dimensionality...")
        for algorithm in config['reduction_algorithm']:
            df = reduce(df, "embedding", new_column_name = f"embedding_reduced_{algorithm}", reduction_algorithm = algorithm, dimension = config['dimension'])
        

    # specify behavioral data columns which should be merged
    behavioral_columns = config['behavioral_columns']
    print(behavioral_columns)

    if config['transcribe_text']:
        print("Merging behavioral data...")
        df = merge_behavioral_data(df, config['input_path'], behavioral_columns)

    # custom scripts to create needed features
    df = get_trial_type(df)
    df = resolve_slider_items(df)

    if config['word_cloud']:
        # ??? TODO
        pass

    if config['text_classification']:
        print("Classifying text...")
        df = text_classification(df, ["certain", "uncertain", "sure", "unsure", "pretty sure", "maybe", "kind of", "i think so", "it feels like", "assume that", "definitely", "absolutely", "confidence", "suspect that must", "cannot be", "im positive", "i know", "i remember"])


    cols_embeddings = []
    for i in range(config['dimension']):
        cols_embeddings = cols_embeddings + [f"embedding_reduced_pca_{i+1}", f"embedding_reduced_tsne_{i+1}", f"embedding_reduced_both_{i+1}"]
        
    cols = ["uuid", "trial_number", "transcribed_text", "embedding"] + ['slider_items', 'trial_type'] + behavioral_columns + cols_embeddings
    df.to_csv(os.path.join(config['output_path'], "output.csv"), sep=';', index=False, columns=cols)




if __name__ == "__main__":
    main()

