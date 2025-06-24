# AI-VTuber-Chatbot

An AI-powered interactive virtual assistant featuring a VTuber avatar. This project uses OpenAI API, DeepSeek, VoiceVox, and other AI technologies to create a responsive AI chatbot with real-time voice and visual interaction.

## Features

* **Voice Recognition**: Capture microphone input and convert to text via speech recognition.
* **AI Conversation**: Natural response generation using DeepSeek and other LLMs.
* **Text-to-Speech**: Convert AI responses to speech in Japanese, English, and more.
* **YouTube Chat Integration**: Read and respond to messages from YouTube live chat.
* **Multi-language Support**: Translate between languages as needed.

## Requirements

* Python 3.8+
* Dependencies listed in `requirements.txt`
* OpenRouter API key for DeepSeek access
* VoiceVox (optional for better Japanese TTS)

## Installation

### Windows

1. Ensure Python is installed
2. Run `install.bat` to install all dependencies
3. If that fails, use `python install_dependencies.py`
4. Download and launch VoiceVox Engine from [official site](https://voicevox.hiroshiba.jp/) (optional)

### Linux / macOS

1. Make sure Python is installed

2. Make `run.sh` executable and run it:

   ```bash
   chmod +x run.sh
   ./run.sh
   ```

3. Or manually install dependencies:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

## Configuration

Edit `config.py` to set:

* `API_KEY`: your OpenRouter API key
* `API_BASE`: default API base URL
* `API_MODEL`: AI model name
* `WHISPER_MODEL`: speech-to-text model

## Usage

Run the program with:

```bash
python run.py
```

Choose a mode:

1. **Mic Mode**: Press and hold RIGHT\_SHIFT to speak
2. **YouTube Mode**: Input YouTube livestream ID to engage with chat
3. **Twitch Mode**: (currently disabled)

## Character Configuration

Create or edit characters in `characterConfig/[CharacterName]/identity.txt`

## Contribution

Contributions are welcome! Submit a pull request or report issues.

## License

[MIT License](LICENSE)

## Support

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/R6R7AH1FA)

## Updates

### v3.5

* Now supports Twitch streamer chat

### v3.0

* VoiceVox Japanese TTS
* Added multilingual support (EN, RU, DE, FR, HI, ES, etc.) using Silero TTS

Switch between TTS engines in `run.py`:

```python
# For Japanese:
voicevox_tts(tts)

# For multilingual:
silero_tts(tts_en, "en", "v3_en", "en_21")
```

## Technologies Used

* [VoiceVox Engine](https://hub.docker.com/r/voicevox/voicevox_engine) or [VoiceVox Colab](https://colab.research.google.com/github/SociallyIneptWeeb/LanguageLeapAI/blob/main/src/run_voicevox_colab.ipynb)
* [DeepL](https://www.deepl.com)
* [DeepLx](https://github.com/OwO-Network/DeepLX)
* [OpenAI Whisper](https://platform.openai.com/account/api-keys)
* [Silero TTS](https://github.com/snakers4/silero-models#text-to-speech)
* [VB-Cable](https://vb-audio.com/Cable/)
* VtubeStudio

## Installation Steps (Extended)

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Create `config.py` and add:

```python
api_key = 'yourapikey'
owner_name = 'YourName'
```

3. (Optional) Add blacklist users in `run.py`:

```python
blacklist = ["Nightbot", "streamelements"]
```

4. Edit assistant character lore in:

```text
characterConfig/Pina/identity.txt
```

5. For Twitch integration, configure `utils/twitch_config.py` with your credentials and token from [Twitch Token Generator](https://twitchapps.com/tmi/)

6. Choose TTS engine (`VoiceVox` or `Silero`) in `run.py`

7. Configure translation method in `utils/translate.py`

* `translate_deeplx()` or `translate_google()`

8. For OBS integration:

* Use `chat.txt` and `output.txt` as inputs for OBS live subtitles

## FAQ

### 1. Audio Transcription Error

Replace try-catch to print detailed error:

```python
def transcribe_audio(file):
    global chat_now
    audio_file = open(file, "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    chat_now = transcript.text
    print("Question: " + chat_now)

    result = owner_name + " said " + chat_now
    conversation.append({'role': 'user', 'content': result})
    openai_answer()
```

### 2. Mecab / Katakana Error

Remove these lines from `utils/TTS.py` if MeCab errors:

```python
from utils.katakana import *
katakana_text = katakana_converter(tts)
```

Pass `tts` directly:

```python
params_encoded = urllib.parse.urlencode({'text': tts, 'speaker': 46})
```

## Credits

Inspired by the work of **shioridotdev**. Thanks to the creators of VoiceVox, DeepL, Whisper, VtubeStudio, and Silero for enabling this project.

## Demo

not yet
