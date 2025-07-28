import winsound
import sys
import pytchat
import time
import re
import pyaudio
import keyboard
import wave
import threading
import json
import whisper
import os
from g4f.client import Client
from utils.translate import *
from utils.TTS import *
from utils.subtitle import *
from utils.promptMaker import *

# Setup encoding
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

whisper_model = whisper.load_model("base", device="cpu")


conversation = []
history = {"history": conversation}
chat_now, chat_prev, chat = "", "", ""
total_characters = 0
is_Speaking = False
owner_name = "Wilds"
blacklist = ["Nightbot", "streamelements"]

def record_audio():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    WAVE_OUTPUT_FILENAME = "input.wav"
    
    p = pyaudio.PyAudio()
    default_input = p.get_default_input_device_info()
    print(f"Using input: {default_input['name']}")

    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=default_input['index'],
                        frames_per_buffer=CHUNK)
        
        frames = []
        print("Recording... Hold RIGHT_SHIFT")
        while keyboard.is_pressed('RIGHT_SHIFT'):
            data = stream.read(CHUNK)
            frames.append(data)
        print("Recording stopped.")

        stream.stop_stream()
        stream.close()
        p.terminate()
        
        with wave.open(WAVE_OUTPUT_FILENAME, 'wb') as wf:
            wf.setnchannels(CHANNELS)
            wf.setsampwidth(p.get_sample_size(FORMAT))
            wf.setframerate(RATE)
            wf.writeframes(b''.join(frames))

        transcribe_audio(WAVE_OUTPUT_FILENAME)
        os.remove(WAVE_OUTPUT_FILENAME)

    except Exception as e:
        print(f"Recording error: {e}")
        p.terminate()

def transcribe_audio(file):
    global chat_now
    try:
        result = whisper_model.transcribe(file)
        chat_now = result["text"]
        print("Question:", chat_now)

        message = f"{owner_name} said {chat_now}"
        conversation.append({'role': 'user', 'content': message})
        openai_answer()

    except Exception as e:
        print(f"Transcribe error: {e}")

def openai_answer():
    global total_characters, conversation
    try:
        client = Client()

        total_characters = sum(len(d['content']) for d in conversation)
        while total_characters > 4000:
            conversation.pop(2)
            total_characters = sum(len(d['content']) for d in conversation)

        with open("conversation.json", "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)

        prompt = getPrompt()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=prompt,
            web_search=False
        )

        message = response.choices[0].message.content
        conversation.append({'role': 'assistant', 'content': message})
        print(message)
        translate_text(message)

    except Exception as e:
        print(f"OpenAI error: {e}")

def yt_livechat(video_id):
    global chat
    live = pytchat.create(video_id=video_id)
    while live.is_alive():
        try:
            for c in live.get().sync_items():
                if c.author.name in blacklist:
                    continue
                if not c.message.startswith("!"):
                    chat_raw = re.sub(r':[^\s]+:', '', c.message).replace('#', '')
                    chat = c.author.name + ' berkata ' + chat_raw
                    print(chat)
            time.sleep(1)
        except Exception as e:
            print(f"Chat error: {e}")

def translate_text(text):
    global is_Speaking
    detect = detect_google(text)
    tts = translate_google(text, detect, "JA")
    tts_en = translate_google(text, detect, "EN")

    print("JP Answer:", tts)
    print("EN Answer:", tts_en)

    silero_tts(tts_en, "en", "v3_en", "en_21")
    generate_subtitle(chat_now, text)

    is_Speaking = True
    winsound.PlaySound("test.wav", winsound.SND_FILENAME)
    is_Speaking = False
    if os.path.exists("test.wav"):
        os.remove("test.wav")

    # Clear subtitle
    open("output.txt", "w").close()
    open("chat.txt", "w").close()

def preparation():
    global chat_now, chat_prev, conversation
    while True:
        chat_now = chat
        if not is_Speaking and chat_now != chat_prev:
            chat_prev = chat_now
            conversation.append({'role': 'user', 'content': chat_now})
            openai_answer()
        time.sleep(2)  # lebih hemat CPU

if __name__ == "__main__":
    try:
        mode = input("Mode (1-Mic,2-Youtube,3-Twitch): ")
        if mode == "1":
            print("Press and Hold Right Shift to record audio")
            while True:
                if keyboard.is_pressed('RIGHT_SHIFT'):
                    record_audio()

        elif mode == "2":
            live_id = input("Livestream ID: ")
            t = threading.Thread(target=preparation)
            t.daemon = True
            t.start()
            yt_livechat(live_id)

        elif mode == "3":
            print("Twitch mode is currently disabled")

    except KeyboardInterrupt:
        print("Stopped")
