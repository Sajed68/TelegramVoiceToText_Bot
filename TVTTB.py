import os
import requests
import time
import speech_recognition as sr
from pydub import AudioSegment

# You Can Use Whisper, but it need to Download large weight:
#import whisper
#model = whisper.load_model("large")


BOT_TOKEN = "Your_TOKEN"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}" # If bot will be used for telegram
FILE_URL = f"https://api.telegram.org/file/bot{BOT_TOKEN}/"


DOWNLOAD_DIR = "/tmp/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

recognizer = sr.Recognizer()

# If you need proxy to connect to the telegram api, change this line:
#proxies = None
proxies = {'http': 'http://localhost:2080', 'https': 'http://localhost:2080'}

def get_updates(offset=None, timeout=20):
    url = f"{API_URL}/getUpdates"
    params = {"timeout":timeout, "offset":offset}
    response = requests.get(url, params=params, proxies=proxies)
    return response.json()
    
def get_file(file_id):
    url = f"{API_URL}/getFile"
    params = {"file_id": file_id}
    response = requests.get(url, params=params, proxies=proxies).json()
    return response['result']['file_path']
    
def download_file(file_path, save_as):
    file_url = FILE_URL + file_path
    response = requests.get(file_url, proxies=proxies)
    with open(save_as, "wb") as f:
        f.write(response.content)
    
def convert_to_wav(input_file, output_file):
    audio = AudioSegment.from_file(input_file, format="ogg")
    audio = audio.set_frame_rate(16000).set_channels(1)
    audio.export(output_file, format='wav')
    
def speech_to_text(wav_file, model=None):
    if model is None:
        with sr.AudioFile(wav_file) as source:
            audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language='fa-IR')
            return text
        except sr.RequestError as e:
            return f"error:{e}"
        except:
            return "I cannot recognize your voice"
    else: # Using Whisper Model
        result = model.transcribe(wav_file, language="fa")
        return result["text"].strip()
        
def send_message(chat_id, text):
    url = f"{API_URL}/sendMessage"
    requests.post(url, json={"chat_id":chat_id, "text":text}, proxies=proxies)
    
def main():
    print("Bot started. Wait for voice messages...")
    offset = None
    while True:
        updates = get_updates(offset=offset)
        if "result" in updates:
            for update in updates["result"]:
                offset = update["update_id"] + 1
                message = update.get("message")
                if not message:
                    continue
                    time.sleep(100)
                if "voice" in message:
                    chat_id = message["chat"]["id"]
                    voice = message["voice"]
                    file_id = voice["file_id"]
                    
                    file_path = get_file(file_id)
                    ogg_file = os.path.join(DOWNLOAD_DIR, f"{file_id}.ogg")
                    wav_file = os.path.join(DOWNLOAD_DIR, f"{file_id}.wav")
                    download_file(file_path, ogg_file)
                    
                    convert_to_wav(ogg_file, wav_file)
                    # pass model as second input, to use whisper
                    text = speech_to_text(wav_file)
                    
                    send_message(chat_id, text)
                    print(f"user said: {text}")
        time.sleep(1)
        
    
    
if __name__ == "__main__":
    main()
        
