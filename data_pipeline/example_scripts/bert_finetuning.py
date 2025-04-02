# pip install transformers==4.45.2 sentence-transformers==3.1.1
# https://github.com/UKPLab/sentence-transformers/issues/3021

""" 
This script allows you to fine-tune the SentenceBERT model to obtain better sentence embeddings for your specific dataset.
"""
import pandas as pd
from datasets import Dataset
from sentence_transformers import (
    SentenceTransformer,
    SentenceTransformerTrainer,
    SentenceTransformerTrainingArguments,
    InputExample
)
from sentence_transformers.losses import ContrastiveTensionLoss
from sentence_transformers.losses import ContrastiveTensionDataLoader
from torch.utils.data import DataLoader
import logging
import math

# Load the data
df = pd.read_csv('../../output/output_raw.csv', sep=';') # Input Data
texts = df['transcribed_text'].fillna('').tolist()
texts = [str(text) for text in texts if text is not None and len(text) > 10]  # Ensure no empty strings
# Filter out NoneType values from the texts list
texts = [text for text in texts if text is not None]
print(f"Dataset size: {len(texts)}")

dataset = ContrastiveTensionDataLoader(
    texts, batch_size=8, pos_neg_ratio=8
)

# Load pre-trained model
model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name)

loss = ContrastiveTensionLoss(model)

# Train the model
model.fit(
    train_objectives=[(dataset, loss)],
    epochs=1,
    optimizer_params={"lr": 5e-5},
    checkpoint_path='models/miniLM-finetuned',
    show_progress_bar=True,
    use_amp=False,  # Set to True, if your GPU supports FP16 cores
)

# Save the fine-tuned model
model.save('models/miniLM-finetuned')

# Load the fine-tuned model
fine_tuned_model = SentenceTransformer('models/miniLM-finetuned')

# Test and load the fine-tuned model
test_texts = ["This is a test sentence.", "Another example sentence."]
embeddings = fine_tuned_model.encode(test_texts)
print(embeddings)
print("Embeddings generated for test texts.")