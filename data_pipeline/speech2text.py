import os
from argparse import ArgumentParser
import csv
import json
import pandas as pd
from utils import get_uuids
import re
import torch



#print(torch.cuda.is_available(), flush=True)

SAMPLING_RATE = 16000
__file_ending = ".wav"


def transcribe(path, model, device):       
    """
    Transcribes audio files located in the specified path.
    Parameters:
        path (str):
        model (str): The model to use for transcribing
        device (str: "cuda", "cpu"): hardware device to run the model on

    :return: A pandas DataFrame containing the transcribed text for each audio file.
    """
    # find all uuids in ressource path
    uuids = get_uuids(path)

    print('Transcribing audio...')

    uuids = get_uuids(path)

    df = pd.DataFrame(columns=['uuid', 'trial_number', 'transcribed_text'])
    # For each uuid transcribe all trial audio recordings
    for uuid in uuids:
        print(uuid)
        paths = _get_all_cutted_audios(os.path.join(path, uuid))
        transcribed = _transcribe_audios(paths, model, device)
        for text, i in transcribed:
            new_row = {
                'uuid': str(uuid),
                'trial_number': int(i),
                'transcribed_text': str(text).strip()
            }
            new_row_df = pd.DataFrame(new_row, index=[0])
            df = pd.concat([df, new_row_df], ignore_index=True)
    return df
    
def _get_all_cutted_audios(path):
    """
    Retrieves a list of all the cut audio files in the specified directory.

    Parameters:
        path (str): The path to the directory containing the audio files.

    Returns:
        list: A list of file paths for all the cut audio files in the directory.
    """
    files = []
    for file in os.listdir(path):
        if file.endswith(__file_ending):
            files.append(os.path.join(path, file))
    return files

def _transcribe_audios(paths, model, device):
    """
    Transcribes a list of audio files using the Whisper library.

    Args:
        paths (List[str]): A list of file paths to audio files.
        model (str): The model to use for transcribing
        device (str: "cuda", "cpu"): hardware device to run the model on

    Returns:
        List[str]: A list of transcribed text for each audio file.
    """

    with open('./config.json') as handle:
        config = json.loads(handle.read())

    # parameter which model to use
    model_name = model
    if model.startswith('whisper-'):
        import whisper
        model_name = model.split('whisper-')[1]
        model = whisper.load_model(model_name, device=device, download_root=config["cache_path"])
    elif model.startswith('whisperx-'):
        import whisperx
        compute_type = "float32" if torch.cuda.is_available() else "int8"
        model_name = model.split('whisperx-')[1]
        model = whisperx.load_model(model_name, device, compute_type=compute_type, download_root=config["cache_path"])
    else:
        raise ValueError(f"Model {model} not supported.")


    if config['use_silence_detection']:
        model_silence_detection, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                                    model='silero_vad',
                                    force_reload=True,
                                    onnx=False)

        (get_speech_timestamps,
        save_audio,
        read_audio,
        VADIterator,
        collect_chunks) = utils

    transcribed = []

    pattern = r'audio_(\d+)\.wav'

    for path in paths:
        res = ''
        # silence detection
        print(path)
        speech_timestamps = [0]
        if config['use_silence_detection']:
            wav = read_audio(os.path.join(path), sampling_rate=SAMPLING_RATE)
            # get speech timestamps from full audio file
            speech_timestamps = get_speech_timestamps(wav, model_silence_detection, sampling_rate=SAMPLING_RATE)
        if len(speech_timestamps) == 0:
            print(f"no speech detected for {path}")
            res = ''
        else:
            # if files are too small then we get an error. This is a workaround
            try:
                if model_name.startswith('whisper-'):
                    res = model.transcribe(os.path.join(path), fp16=False, verbose=True)
                    res = res['text']
                elif model_name.startswith('whisperx-'):
                    audio = whisperx.load_audio(os.path.join(path))
                    result = model.transcribe(audio, batch_size=16)
                    res = result["segments"][0]['text']
            except Exception as e:
                print(e)
                print('File is too small to transcribe (path: ' + path + ')')

        match = re.search(pattern, path)
        number = match.group(1)
        transcribed.append((res, number))
    return transcribed

