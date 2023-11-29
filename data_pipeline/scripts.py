import argparse
import os
from speech2text import transcribe
from embeddings import create_embeddings
from dimensionality_reduction import reduce
from merge_behavioral_data import merge_behavioral_data
from custom_scripts import resolve_slider_items, get_trial_type
import random

def main():
    random.seed(543547)
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="Path to the ressources folder.", type=str, required=True)
    parser.add_argument("--output", help="Path to the output file.", type=str, required=True)
    parser.add_argument("--reduction_algorithm", help="Reduction algorithm to use.",choices=["PCA", "TSNE", "both"], type=str, default = "PCA")
    parser.add_argument("--dimension", type=int, help="Dimension to reduce to.", default = 2)
    args = parser.parse_args()

    

    df = transcribe(args.path, "large-v3")
    #df = transcribe(args.path, "tiny")
    df = create_embeddings(df, "transcribed_text", new_column_name = "embedding")
    df = reduce(df, "embedding", new_column_name = "embedding_reduced_pca", reduction_algorithm = "PCA", dimension = args.dimension)
    df = reduce(df, "embedding", new_column_name = "embedding_reduced_tsne", reduction_algorithm = 'TSNE', dimension = args.dimension)
    df = reduce(df, "embedding", new_column_name = "embedding_reduced_both", reduction_algorithm = 'both', dimension = args.dimension)

    behavioral_columns = ['stimulus', 'response', 'rt', 'pair']
    df = merge_behavioral_data(df, args.path, behavioral_columns)

    # custom scripts to create needed features
    df = get_trial_type(df)
    df = resolve_slider_items(df)

    cols_embeddings = []
    for i in range(args.dimension):
        cols_embeddings = cols_embeddings + [f"embedding_reduced_pca_{i+1}", f"embedding_reduced_tsne_{i+1}", f"embedding_reduced_both_{i+1}"]
        
    cols = ["uuid", "trial_number", "transcribed_text", "embedding"] + ['slider_items', 'trial_type'] + behavioral_columns + cols_embeddings
    df.to_csv(os.path.join(args.output, "output.csv"), sep=';', index=False, columns=cols)


if __name__ == "__main__":
    main()

