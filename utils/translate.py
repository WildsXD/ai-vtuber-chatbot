import requests
import json
import sys
from deep_translator import GoogleTranslator
from deep_translator.exceptions import LanguageNotSupportedException
from langdetect import detect

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

# You can use DeepL or Google Translate to translate the text
# DeepL can translate more casual text in Japanese
# DeepLx is a free and open-source DeepL API
def translate_deeplx(text, source, target):
    url = "http://localhost:1188/translate"
    headers = {"Content-Type": "application/json"}

    # define the parameters for the translation request
    params = {
        "text": text,
        "source_lang": source,
        "target_lang": target
    }

    # convert the parameters to a JSON string
    payload = json.dumps(params)

    # send the POST request with the JSON payload
    response = requests.post(url, headers=headers, data=payload)

    # get the response data as a JSON object
    data = response.json()

    # extract the translated text from the response
    translated_text = data['data']

    return translated_text

def translate_google(text, source, target):
    try:
        translator = GoogleTranslator(source=source.lower(), target=target.lower())
        result = translator.translate(text)
        return result
    except LanguageNotSupportedException:
        print(f"Language not supported: source={source}, target={target}")
        return text
    except Exception as e:
        print(f"Error translate: {str(e)}")
        return text

def detect_google(text):
    try:
        result = detect(text)
        return result.upper()
    except Exception as e:
        print(f"Error detect: {str(e)}")
        return 'EN'

if __name__ == "__main__":
    text = "aku tidak menyukaimu"
    source = translate_deeplx(text, "ID", "JA")
    print(source)
