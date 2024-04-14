import os
from argparse import ArgumentParser
import csv
import whisper
import pandas as pd
from utils import get_uuids
import re
import torch


SAMPLING_RATE = 16000
__file_ending = ".wav"


def transcribe(path, model):       
    """
    Transcribes audio files located in the specified path.
    
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
        transcribed = _transcribe_audios(paths, model)
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

def _transcribe_audios(paths, model):
    """
    Transcribes a list of audio files using the Whisper library.

    Args:
        paths (List[str]): A list of file paths to audio files.
        model (str): The model to use for transcribing

    Returns:
        List[str]: A list of transcribed text for each audio file.
    """
    # parameter which model to use
    model = whisper.load_model(model)

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
        wav = read_audio(os.path.join(path), sampling_rate=SAMPLING_RATE)
        # get speech timestamps from full audio file
        speech_timestamps = get_speech_timestamps(wav, model_silence_detection, sampling_rate=SAMPLING_RATE)
        if len(speech_timestamps) == 0:
            print(f"no speech detected for {path}")
            res = ''
        else:
            # if files are too small then we get an error. This is a workaround
            try:
                res = model.transcribe(os.path.join(path), fp16=False)
                res = res['text']
            except Exception as e:
                print(e)
                print('File is too small to transcribe (path: ' + path + ')')

        match = re.search(pattern, path)
        number = match.group(1)
        transcribed.append((res, number))
    return transcribed

