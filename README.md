# TelegramVoiceToText_Bot  
Do you have friends who insist on sending **voice messages** instead of text — even when it’s just a single word? 😅  
This bot helps you out by automatically converting their voice messages into text, making communication faster and easier.  
The bot is written in **Python** and supports two transcription backends:  

- [`SpeechRecognition`](https://pypi.org/project/SpeechRecognition/) — lightweight, uses Google Web Speech API, works well for short audios.  
- [OpenAI Whisper](https://github.com/openai/whisper) — more powerful, supports longer and noisier audios, but requires downloading large model files and more resources.  

For everyday usage, `SpeechRecognition` is usually enough. If you need to play around with models (and don’t mind the download), Whisper is a great option, also it can works offline!  

---

## Installation  

Before you start, install the required Python packages:  

```bash
pip install pydub requests SpeechRecognition
```

For Whisper support, follow their setup and install:  
```bash
pip install git+https://github.com/openai/whisper.git
```
(Note: Whisper also needs [ffmpeg](https://ffmpeg.org/))  

---
## Configuration
Before running the bot, you need to edit a few things in the code:  
1. **Set your bot token**
   ```python
   BOT_TOKEN = "Your_Token"
   ```
2. **(Optional) Configure proxy for Telegram API**
   ```python
   #proxies = None  
   proxies = {'http': 'http://localhost:2080', 'https': 'http://localhost:2080'}
   ```
3. **Switch to Whisper (optional)**
   * Uncomment these lines at the top:
     ```python
     #import whisper
     #model = whisper.load_model("large")
     ```
   * And call transcription with the model:
     ```python
     text = speech_to_text(wav_file, model=model)
     ```
5. **Change download folder (optional)**  
   By default, files are stored in ```/tmp/downloads```. You can change this:
   ```python
   DOWNLOAD_DIR = "/tmp/downloads"
   os.makedirs(DOWNLOAD_DIR, exist_ok=True)
   ```
---
## Running the Bot  
After setup, simply run:  
```bash
python TVTTB.py
```

Then send your bot a **voice message** in Telegram, and it will reply with the text transcription.  
1. If you’re using ```SpeechRecognition```, it works instantly (but may fail on long audios).
2. If you’re using ```Whisper```, expect slower processing but may be higher accuracy.
3. In my experiments, ```SpeechRecognition``` works better in most cases!

---
## Note  
* This bot currently supports **Persian (fa-IR)** transcription. You can change the language code in the code to support others.
* Clean up of temporary files is included, but you may want to adjust it depending on your usage.
* Contributions and suggestions are welcome!
* You can also run the code on **Google Colab:**[Try it here](https://colab.research.google.com/drive/17_ZhFawtDyT2DNwWdpD_tNq4Lho84yG2?usp=sharing)
