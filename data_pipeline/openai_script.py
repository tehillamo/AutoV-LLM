from openai import OpenAI
import os                                                                                                                                                                                                          
from dotenv import load_dotenv
from pathlib import Path
import random
import time
import concurrent.futures

def load_openai_client(api_key):
    if api_key is None:
        raise ValueError("API key not found. Please set the OPENAI_API_KEY variable.")
    client = OpenAI(api_key=api_key)
    return client

def openai_embeddings(df, df_col, df_result_col, model, api_key, max_workers=5):
    client = load_openai_client(api_key)
    texts = df[df_col].tolist()
    if not texts:
        raise ValueError(f"Column '{df_col}' is empty or not found in the DataFrame.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(lambda prompt: send_request_with_retry(prompt, client, model, type="embedding"), texts))

    df[df_result_col] = results
    return df

def openai_prompting(df, df_col, df_result_col, developer_prompt, model, api_key, max_workers=5):
    client = load_openai_client(api_key)
    texts = df[df_col].tolist()
    if not texts:
        raise ValueError(f"Column '{df_col}' is empty or not found in the DataFrame.")
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(lambda prompt: send_request_with_retry(prompt, client, model, type="completion", developer_prompt=developer_prompt), texts))

    df[df_result_col] = results
    return df

def send_request_with_retry(text, client, model, type=None, developer_prompt=None, max_retries=10):
    text = str(text)
    for attempt in range(max_retries):
        try:
            if type == "embedding":
                response = client.embeddings.create(
                    input=text,
                    model=model
                )
                return response.data[0].embedding
            elif type == "completion":
                response = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": developer_prompt},
                        {"role": "user", "content": text}
                    ]
                )
                return response.choices[0].message.content
        
        except Exception as e:
            print(e)
            wait_time = (2 ** attempt) + random.uniform(0, 1)  # Exponential backoff
            print(f"Attempt {attempt + 1} failed for prompt: {text[:30]}... Retrying in {wait_time:.2f} sec")
            time.sleep(wait_time)

    return "error"