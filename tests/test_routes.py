from flaskr import create_app
import io
import os

correct_file = os.getcwd() + "/tests/test.wav"
incorrect_file = os.getcwd()  + "/tests/test.mp3"
def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing


def test_get(client):
    response = client.get('/text')
    assert b'Please use the post method to submit an audio file' in response.data


def test_without_sound_file(client):
    data = {
        'wrong_name' : ''
    }
    response = client.post('/text', data=data, content_type='multipart/form-data')
    assert b'"msg": "Failed"' in response.data
    assert b'"error": "Sound file not found. Please check if the file is include under the name sound_file"' in response.data

def test_wrong_extension(client):
    file = open(incorrect_file,'rb')
    fileb = file.read()
    file.close()
    data = {
        'sound_file' : (io.BytesIO(fileb), 'test.mp3')
    }
    response = client.post('/text', data=data, content_type='multipart/form-data')
    assert b'"msg": "Failed"' in response.data
    assert b'"error": "This file type is not allowed. Only .wav files are allowed"' in response.data


def test_post(client):
    file = open(correct_file,'rb')
    fileb = file.read()
    file.close()
    data = {
        'sound_file' : (io.BytesIO(fileb), 'test.wav')
    }
    response = client.post('/text', data=data, content_type='multipart/form-data')
    assert b'"msg": "Succes"' in response.data


def test_wrong_language(client):
    file = open(correct_file,'rb')
    fileb = file.read()
    file.close()
    data = {
        'sound_file' : (io.BytesIO(fileb), 'test.wav')
    }
    response = client.post('/text/fr-NL', data=data, content_type='multipart/form-data')
    assert b'"msg": "Failed"' in response.data
    assert b'"error": "This language is not accepted"' in response.data


def test_correct_language(client):
    file = open(correct_file,'rb')
    fileb = file.read()
    file.close()
    data = {
        'sound_file' : (io.BytesIO(fileb), 'test.wav')
    }
    response = client.post('/text/en-US', data=data, content_type='multipart/form-data')
    assert b'"msg": "Succes"' in response.data
