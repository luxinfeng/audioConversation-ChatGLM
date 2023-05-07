import json
import subprocess

from paddlespeech.cli.asr.infer import ASRExecutor
from paddlespeech.cli.tts.infer import TTSExecutor
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware


import requests
import uvicorn
import paddle

origins = [
    '*'
]


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
text2audio = TTSExecutor()
audio2text = ASRExecutor()



@app.post("/chat")
async def chat(audio_file: UploadFile):
    """处理语音聊天请求"""

    print(audio_file.filename)

    """将上传的音频数据保存到临时文件"""
    with open("tmp.webm", "wb") as f:
        f.write(await audio_file.read())

    transformAudio('tmp.webm', 'tmp.wav')

    # 识别语音数据
    request_text = recognize_speech("tmp.wav")

    response_text = generateResponse(request_text)

    # 合成回复语音数据
    speech_data = generate_speech(response_text)

    # 返回回复语音数据
    return FileResponse(speech_data, media_type="audio/wav")



def generateResponse(message):
    url = "http://127.0.0.1:8000/"

    payload = {"prompt": message, "history": [["please speak in english, no more than 15 words", "ok"]]}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

    response_text = response.text

    data2 = json.loads(response_text)

    print(data2['response'])

    return data2['response']


def recognize_speech(audio_data):
    result = audio2text(audio_file=audio_data, lang='en', device=paddle.get_device(), model='transformer_librispeech')
    return result


def generate_speech(message_text):
    message_audio = text2audio(message_text, lang='en', am = 'fastspeech2_vctk', voc='hifigan_vctk', device=paddle.get_device(), spk_id=7)
    return message_audio


def transformAudio(web_file, wav_file):
    command = ['rm', '-rf', wav_file]
    subprocess.run(command)
    command = ['ffmpeg', '-i', web_file, '-ac', '1', '-ar', '16000', wav_file]
    subprocess.run(command, stdout=subprocess.PIPE, stdin=subprocess.PIPE)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=7060, workers=1)
