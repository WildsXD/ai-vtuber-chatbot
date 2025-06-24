# 🤖 AI VTuber Chatbot

**AI VTuber Chatbot** is an interactive, voice-enabled virtual assistant that combines OpenAI (via DeepSeek), Whisper for speech recognition, translation engines, and TTS (Text-to-Speech) to bring your anime-style VTuber assistant to life.

> 🎤 Supports real-time mic input or YouTube livestream chat with multilingual responses and voice playback.

---

## ✨ Features

* 🎤 **Voice Recognition (Mic)**
  Press and hold `RIGHT_SHIFT` to speak to your AI VTuber.

* 💬 **Conversational AI**
  Uses OpenAI GPT (via DeepSeek/OpenRouter) to generate human-like responses.

* 🌍 **Multilingual Support**
  Translates responses to Japanese and English for accurate TTS output.

* 🗣️ **Text-to-Speech (TTS)**
  Uses Silero TTS to generate natural voice audio from AI responses.

* 🎮 **YouTube Chat Integration**
  Reads and replies to YouTube livestream chats in real-time.

* 🧠 **Context Awareness**
  Maintains conversation history and trims intelligently beyond 4000 tokens.

* 📃 **Live Subtitles for OBS**
  Writes `chat.txt` and `output.txt` for real-time captioning on OBS overlays.

---

## 📦 Requirements

* Python 3.8 or higher
* FFmpeg (for Whisper and audio handling)
* [VoiceVox Engine](https://voicevox.hiroshiba.jp/) (optional, for Japanese TTS)
* API Key for OpenRouter (DeepSeek)

Install dependencies with:

```bash
pip install -r requirements.txt
```

---

## ⚙️ How to Run

1. **Configure Your API Key**

Create `config.py` or export your key in the script:

```python
api_key = 'your-api-key'
owner_name = 'Wilds'
```

2. **Run the bot**

```bash
python run.py
```

3. **Choose Mode**

* `1` = Mic input mode (hold `RIGHT_SHIFT` to talk)
* `2` = YouTube live chat mode (enter livestream ID)
* `3` = Twitch (currently disabled)

---

## 🧠 Tech Stack

| Component      | Technology                                                     |
| -------------- | -------------------------------------------------------------- |
| Speech-to-Text | [Whisper](https://github.com/openai/whisper)                   |
| Chat AI        | [g4f (DeepSeek via OpenRouter)](https://openrouter.ai)         |
| Translation    | Google Translate / DeepLX                                      |
| TTS            | [Silero](https://github.com/snakers4/silero-models) / VoiceVox |
| Live Chat      | [pytchat](https://github.com/taizan-hokuto/pytchat)            |
| Subtitles      | Custom OBS-ready files                                         |
| Input Control  | `keyboard` Python module                                       |

---

## 📁 Project Structure

```
.
├── characterConfig/
│   └── Pina/               # Character identity and lore
├── utils/                  # TTS, translation, prompt maker, subtitle handler
├── run.py                  # Main entry point
├── run.bat / run.sh        # Platform-specific runners
├── requirements.txt        # Python dependencies
├── conversation.json       # Chat history for context
├── speaker.json            # Voice speaker configs
├── chat_response.json      # AI reply caching (if needed)
├── output.txt / chat.txt   # OBS overlay files
```

---

## 🥪 Demo

* 🎮 [Live Test](https://youtu.be/h6UEgJxH1-E?t=1616)
* 🔗 [Short Clip](https://www.youtube.com/shorts/_mKVr3ZaM9Q)
* 📘 [Code Explanation](https://youtu.be/qpNG9qrcmrQ)

---

## 💬 Contribution

Pull requests and feedback are welcome!
To contribute, clone the repo, create a feature branch, and submit a PR.

---

## 📝 License

This project is licensed under the MIT License.
Feel free to modify and use it for both personal and commercial purposes.

---

## ☕ Support

If you like this project, consider supporting via [Ko-fi](https://ko-fi.com/ardhach)

