import requests
import time
import hashlib
import base64
import json
from pydub import AudioSegment
from io import BytesIO
from .constants import *

def getHeader(type, param):
    curTime = str(int(time.time()))
    paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
    m2 = hashlib.md5()
    m2.update((API_KEY[type] + curTime + paramBase64).encode('utf-8'))
    checkSum = m2.hexdigest()
    header = {
        'X-CurTime': curTime,
        'X-Param': paramBase64,
        'X-Appid': APP_ID,
        'X-CheckSum': checkSum,
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    return header

def audio2pcm(file):
    sound = AudioSegment.from_mp3(BytesIO(file.read()))
    f = BytesIO()
    sound.export(f, format="s16le", codec="pcm_s16le", parameters=["-ac", "1", "-ar", "16000"])
    return f.read()

def getBody(file):
    data = {'audio': base64.b64encode(audio2pcm(file))}
    return data

def getParam(type, language):
    if type == "A2T":
        param = {
            "engine_type": ENGINE_TYPE[language],
            "aue": "raw"
        }
    if type == "T2A":
        param = {
            "auf": "audio/L16;rate=16000",
            "aue": "raw",
            "voice_name": VOICE_NAME[language],
            "speed": "50",
            "volume": "50",
            "pitch": "50",
            "engine_type": "intp65",
            "text_type": "text"
        }
    return json.dumps(param)
