# AI VTuber Chatbot

**AI VTuber Chatbot** is a real-time, voice-interactive virtual assistant designed to simulate lifelike conversations using speech recognition, translation, and text-to-speech. This project connects cutting-edge technologies including Whisper, OpenAI (via OpenRouter), and multilingual TTS to create an immersive VTuber experience.

---

## 🔍 Overview

This project enables a talking VTuber assistant that can:

* Understand voice input via microphone
* Chat with users via YouTube livestream chat
* Respond using natural AI-generated responses
* Speak using high-quality TTS in multiple languages
* Display real-time subtitles for use with OBS

---

## 🚀 Features

* 🎧 **Mic Mode** — Hold `Right Shift` to speak with your assistant
* 🗨️ **YouTube Live Chat Mode** — Responds automatically to viewers in chat
* 🌐 **Multilingual** — Translate content and responses into Japanese, English, and more
* 🧠 **Contextual AI** — Smart conversation history trimming (within token limits)
* 🔊 **TTS Output** — Convert text responses to natural-sounding speech using Silero or VoiceVox
* 📺 **OBS Integration** — Output chat and answers to `.txt` files for live subtitles

---

## 🧰 Dependencies

* Python 3.8+
* [Whisper](https://github.com/openai/whisper) for speech recognition
* [pytchat](https://github.com/taizan-hokuto/pytchat) for YouTube live chat
* [Silero TTS](https://github.com/snakers4/silero-models) / VoiceVox
* [OpenRouter](https://openrouter.ai) key for DeepSeek / GPT-4o-mini access

Install requirements:

```bash
pip install -r requirements.txt
```

---

## 🛠 Usage

1. **Run the app:**

```bash
python run.py
```

2. **Choose a mode:**

   * `1` = Mic mode (hold Right Shift to record)
   * `2` = YouTube Live mode (enter stream ID)
   * `3` = Twitch mode (disabled)

3. **Configure settings:**
   Edit your API keys, model, and character identity in `config.py` or the appropriate `characterConfig` folder.

---

## 🤝 Contributing

All contributions are welcome! Feel free to:

* Open issues
* Submit pull requests
* Fork and build your own AI VTuber

---

## 📜 License

MIT License — free for personal and commercial use.

