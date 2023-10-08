import argparse
import os
import speech2text
import embeddings

""" s2text = speech2text.Speech2Text("../ressources", "base")
df = s2text.transcribe()
create_embeddings = embeddings.Embeddings()
df = create_embeddings.create_embeddings(df, "transcribed_text")
df.to_csv("../output/output.csv", sep=';', index=False, columns=["uuid", "trial_number", "transcribed_text", "transcribed_text_embedding_reduced"]) """

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="Path to the ressources folder.", type=str, required=True)
    parser.add_argument("--output", help="Path to the output file.", type=str, required=True)
    parser.add_argument("--reduction_algorithm", help="Reduction algorithm to use.",choices=["PCA", "TSNE"], type=str, default = "PCA")
    parser.add_argument("--dimension", type=int, help="Dimension to reduce to.", default = 2)
    args = parser.parse_args()
    s2text = speech2text.Speech2Text(args.path, "base")
    df = s2text.transcribe()
    create_embeddings = embeddings.Embeddings()
    df = create_embeddings.create_embeddings(df, "transcribed_text", dimension=args.dimension, reduction_algorithm=args.reduction_algorithm)
    df.to_csv(os.path.join(args.output, "output.csv"), sep=';', index=False, columns=["uuid", "trial_number", "transcribed_text", "transcribed_text_embedding_reduced"])

if __name__ == "__main__":
    main()
