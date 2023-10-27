import argparse
import os
import speech2text
import embeddings
import random

def main():
    random.seed(543547)
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="Path to the ressources folder.", type=str, required=True)
    parser.add_argument("--output", help="Path to the output file.", type=str, required=True)
    parser.add_argument("--reduction_algorithm", help="Reduction algorithm to use.",choices=["PCA", "TSNE", "both"], type=str, default = "PCA")
    parser.add_argument("--dimension", type=int, help="Dimension to reduce to.", default = 2)
    args = parser.parse_args()
    s2text = speech2text.Speech2Text(args.path, "base")
    df = s2text.transcribe()
    create_embeddings = embeddings.Embeddings()
    df = create_embeddings.create_embeddings(df, "transcribed_text", dimension=args.dimension, reduction_algorithm=args.reduction_algorithm)
    df.to_csv(os.path.join(args.output, "output.csv"), sep=';', index=False, columns=["uuid", "trial_number", "transcribed_text", "transcribed_text_embedding_reduced_pca"])

if __name__ == "__main__":
    main()
