import argparse
import os
from speech2text import transcribe
from embeddings import create_embeddings
from dimensionality_reduction import reduce
from merge_behavioral_data import merge_behavioral_data
from custom_scripts import resolve_slider_items, get_trial_type
from text_classification import text_classification
from word_cloud import generate_word_cloud
import random
import json
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
from preprocessing import convert_to_tensor
from keywords import extract_keywords_keybert
from summarization import summarize
from openai_script import openai_prompting, openai_embeddings
from prompts import post_asr_correction_prompt
#"text_classes": ["certain", "uncertain", "sure", "unsure", "pretty sure", "maybe", "kind of", "i think so", "it feels like", "assume that", "definitely", "absolutely", "confidence", "suspect that must", "cannot be", "im positive", "i know", "i remember"]
#"text_classes": ["absolutely uncertain", "very uncertain", "somewhat uncertain", "a little uncertain", "a little certain", "somewhat certain", "very certain", "absolutely certain"]

def main():

    parser = argparse.ArgumentParser(description="")
    parser.add_argument('--device', type=str, default="cpu", help="Device to run the whisper model on")
    args = parser.parse_args()

    print("Starting data pipeline...")
    with open('./config.json') as handle:
        config = json.loads(handle.read())
        
    print(config)

    random.seed(543547)

    if config['transcribe_text']:
        print("Transcribing audio...")
        df = transcribe(config['input_path'], config['transcription_model'], args.device)
    else:
        df = pd.read_csv(config['input_path'], sep=',')
        if 'transcribed_text' not in df.columns:
            raise ValueError('"transcribed_text" column not found in input file!')
        
    if config['calculate_text_embeddings']:
        if config['use_openai_embeddings']:
            print("Calculating text embeddings using OpenAI...")
            df = openai_embeddings(df, "transcribed_text", "embedding", config['openai_embeddings_model'], config['openai_api_key'])
        else:
            print("Calculating text embeddings...")
            df = create_embeddings(df, "transcribed_text", new_column_name = "embedding", model_name = config['bert_finetuned_model'])

    if config["dimensionality_reduction"]:
        print("Reducing dimensionality...")
        if config['calculate_text_embeddings'] == False:
            raise ValueError("Cannot reduce dimensionality without calculating text embeddings!")
        for algorithm in config['reduction_algorithm']:
            df = reduce(df, "embedding", new_column_name = f"embedding_reduced_{algorithm}", reduction_algorithm = algorithm, 
                        dimension = config['dimension'], per_participant = config['reduction_per_participant'])

    # specify behavioral data columns which should be merged
    behavioral_columns = config['behavioral_columns']
    print(behavioral_columns)

    if config['merge_behavioral_data']:
        print("Merging behavioral data...")
        df = merge_behavioral_data(df, config['input_path'], behavioral_columns)

    if config['post_asr_correction']:
        print("Applying post-ASR correction...")
        df = openai_prompting(df, "transcribed_text", "transcribed_text_corrected", post_asr_correction_prompt(), config['openai_model'], config['openai_api_key'])

    # custom scripts to create needed features
    #df = get_trial_type(df)
    #df = resolve_slider_items(df)

    if config['word_cloud']:
        generate_word_cloud(df['transcribed_text'], config['ignore_words_in_word_cloud'], config['output_path'])

    if config['text_classification']:
        print("Classifying text...")
        df = text_classification(df, config['text_classes'], config['text_classification_threshold'], config['zero_shot_text_finetuned_model'])

    cols_embeddings = []
    for i in range(config['dimension']):
        cols_embeddings = cols_embeddings + [f"embedding_reduced_pca_{i+1}", f"embedding_reduced_tsne_{i+1}", f"embedding_reduced_both_{i+1}"]

    if config['keywords']:
        print("Extracting keywords...")
        df = extract_keywords_keybert(df, "transcribed_text", "keywords", top_n_keywords=config["top_n_keywords"])

    if config['summarize']:
        print("Summarizing text...")
        df = summarize(df, config['max_length_summary'], config['min_length_summary'])

    if config['use_openai_prompting']:
        print("Using OpenAI prompting...")
        df = openai_prompting(df, "transcribed_text", "openai_response", config['developer_prompt'], config['openai_model'], config['openai_api_key'])

    df.to_csv(os.path.join(config['output_path'], config['output_name']), sep=';', index=False)




if __name__ == "__main__":
    main()

