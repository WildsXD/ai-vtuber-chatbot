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
from g4f.client import Client
from utils.translate import *
from utils.TTS import *
from utils.subtitle import *
from utils.promptMaker import *
sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)



conversation = []
history = {"history": conversation}

mode = 0
total_characters = 0
chat = ""
chat_now = ""
chat_prev = ""
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


    info = p.get_host_api_info_by_index(0)
    numdevices = info.get('deviceCount')
    for i in range(0, numdevices):
        if (p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
            print("Input Device id ", i, " - ", p.get_device_info_by_host_api_device_index(0, i).get('name'))
    
   
    default_input = p.get_default_input_device_info()
    print(f"Using default input device: {default_input['name']}")
    
    try:
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index=default_input['index'],
                        frames_per_buffer=CHUNK)
        
        frames = []
        print("Recording...")
        while keyboard.is_pressed('RIGHT_SHIFT'):
            data = stream.read(CHUNK)
            frames.append(data)
        print("Stopped recording.")
        
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        transcribe_audio("input.wav")
        
    except Exception as e:
        print(f"Error recording audio: {str(e)}")
        p.terminate()

def transcribe_audio(file):
    global chat_now
    try:
        # Load the Whisper model
        model = whisper.load_model("base")
        
        # Transcribe the audio file
        result = model.transcribe(file)
        chat_now = result["text"]
        print("Question: " + chat_now)
        
        result = owner_name + " said " + chat_now
        conversation.append({'role': 'user', 'content': result})
        openai_answer()
        
    except Exception as e:
        print(f"Detailed error: {str(e)}")
        return

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
        print(f"Detailed error: {str(e)}")

def yt_livechat(video_id):
        global chat

        live = pytchat.create(video_id=video_id)
        while live.is_alive():
        # while True:
            try:
                for c in live.get().sync_items():
                    if c.author.name in blacklist:
                        continue
                    # if not c.message.startswith("!") and c.message.startswith('#'):
                    if not c.message.startswith("!"):
                        # Remove emojis from the chat
                        chat_raw = re.sub(r':[^\s]+:', '', c.message)
                        chat_raw = chat_raw.replace('#', '')
                        # chat_author makes the chat look like this: "Nightbot: Hello". So the assistant can respond to the user's name
                        chat = c.author.name + ' berkata ' + chat_raw
                        print(chat)
                        
                    time.sleep(1)
            except Exception as e:
                print("Error receiving chat: {0}".format(e))


# translating is optional
def translate_text(text):
    global is_Speaking
    # subtitle will act as subtitle for the viewer
    # subtitle = translate_google(text, "ID")

    # tts will be the string to be converted to audio
    detect = detect_google(text)
    tts = translate_google(text, f"{detect}", "JA")
    # tts = translate_deeplx(text, f"{detect}", "JA")
    tts_en = translate_google(text, f"{detect}", "EN")
    try:
        # print("ID Answer: " + subtitle)
        print("JP Answer: " + tts)
        print("EN Answer: " + tts_en)
    except Exception as e:
        print("Error printing text: {0}".format(e))
        return
    # Silero TTS, Silero TTS can generate English, Russian, French, Hindi, Spanish, German, etc. Uncomment the line below. Make sure the input is in that language
    silero_tts(tts_en, "en", "v3_en", "en_21")

    generate_subtitle(chat_now, text)

    time.sleep(1)

    # is_Speaking is used to prevent the assistant speaking more than one audio at a time
    is_Speaking = True
    winsound.PlaySound("test.wav", winsound.SND_FILENAME)
    is_Speaking = False

    # Clear the text files after the assistant has finished speaking
    time.sleep(1)
    with open ("output.txt", "w") as f:
        f.truncate(0)
    with open ("chat.txt", "w") as f:
        f.truncate(0)

def preparation():
    global conversation, chat_now, chat, chat_prev
    while True:
        chat_now = chat
        if is_Speaking == False and chat_now != chat_prev:
            conversation.append({'role': 'user', 'content': chat_now})
            chat_prev = chat_now
            openai_answer()
        time.sleep(1)

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
            t.start()
            yt_livechat(live_id)

        elif mode == "3":
            print("Twitch mode is currently disabled")
            
    except KeyboardInterrupt:
        if 't' in locals():
            t.join()
        print("Stopped")


