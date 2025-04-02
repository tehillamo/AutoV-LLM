from datasets import load_dataset
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from datasets import ClassLabel
import torch

"""
This script allows you to fine-tune a BART model for zero-shot classification using the Hugging Face Transformers library.
It loads a dataset from CSV files, tokenizes the text, and trains the model using the Trainer API.

The training data is assumed to be in a CSV format with the following columns:
- 'text': The text to be classified.
- 'label': The label for the text. This should be a string that can be converted to a ClassLabel.

To assess the model's performance, you must provide a test dataset in the same format.
Note that all labels must be present in the training dataset.

Make sure to have the required libraries installed:
pip install transformers datasets torch pandas
"""

PATH_TO_TRAIN = "train.csv"  # Path to the training dataset
PATH_TO_TEST = "test.csv"  # Path to the test dataset

device = "cuda" if torch.cuda.is_available() else "cpu"
device = 'cpu'
print(f"Using device: {device}")

# Load dataset from CSV
dataset = load_dataset("csv", data_files={"train": PATH_TO_TRAIN, "test": PATH_TO_TEST}, sep=";")

# Load tokenizer
model_name = "facebook/bart-large-mnli"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Tokenization function
def tokenize_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length")

# Apply tokenization
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Extract unique labels
labels = list(set(dataset["train"]["label"]))
num_labels = len(labels)

# Convert labels to IDs
label2id = {label: i for i, label in enumerate(labels)}
id2label = {i: label for label, i in label2id.items()}

# Apply transformation
def encode_labels(example):
    example["label"] = label2id[example["label"]]
    return example

tokenized_datasets = tokenized_datasets.map(encode_labels)

print("Loaded and preprocessed dataset")

model = AutoModelForSequenceClassification.from_pretrained(
    model_name, num_labels=num_labels, id2label=id2label, label2id=label2id
).to(device)

from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="./models",
    eval_strategy="epoch",
    save_strategy="epoch",
    per_device_train_batch_size=4, # Tweak this based on your GPU memory
    per_device_eval_batch_size=4, # Tweak this based on your GPU memory
    num_train_epochs=1,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    tokenizer=tokenizer
)

print("Starting training")
trainer.train()
print("Training completed")
trainer.save_model("./models/bart-large-mnli_finetuned")
print("Model saved to ./models/bart-large-mnli_finetuned")