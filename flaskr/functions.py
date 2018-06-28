from google.cloud import speech
from google.cloud.speech import types
from google.cloud.speech import enums
import io
import struct
import os

from flask import (
    request
)
def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['wav'])
    if('.' in filename):
        if(filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS):
            return True
    return False


def check_post(request, language = "en-US" ):
    data = {}
    if('sound_file' not in request.files):
        data["msg"] = "Failed"
        data["error"] = "Sound file not found. Please check if the file is include under the name sound_file"
        return data
    sound_file = request.files['sound_file']
    if(sound_file.filename == ''):
        data["msg"] = "Failed"
        data["error"] = "No sound file submitted"
        return data
    if(allowed_file(sound_file.filename)):
        return speech_to_text(sound_file,language)
    else:
        data["msg"] = "Failed"
        data["error"] = "This file type is not allowed. Only .wav files are allowed"
        return data


def speech_to_text(sound_file,language ):
    client = speech.SpeechClient()
    content = sound_file.read()
    audio = types.RecognitionAudio(content=content)
    sample_rate = struct.unpack('<L', content[24:28])[0]

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=language,
        sample_rate_hertz=sample_rate,
        )
    data = {}
    try:
        operation = client.long_running_recognize(config, audio)
        response = operation.result(timeout=90)
        r ="";
        for result in response.results:
            #r += 'Confidence: {}'.format(result.alternatives[0].confidence)
            #r += ' ; '
            r += result.alternatives[0].transcript
        r.replace('\\','')
        data["msg"] = "Succes"
        data["result"] =  r
    except Exception as e:
        data["msg"] = "Failed"
        data["error"] =  "Something went wrong with translating the speech to text"
    return data
