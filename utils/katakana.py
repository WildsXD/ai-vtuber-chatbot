import alkana
import re
import sys

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

alphaReg = re.compile(r'^[a-zA-Z]+$')
def isalpha(s):
    return alphaReg.match(s) is not None

def katakana_converter(text):
    """
    Versi sederhana dari konverter katakana tanpa menggunakan MeCab.
    Hanya menggunakan regex dan alkana library.
    """
    # Pisahkan teks menjadi kata-kata
    words = re.findall(r'\b\w+\b', text)
    
    # Buat kamus untuk menyimpan kata dan konversinya
    dict_rep = {}
    
    # Cari kata-kata bahasa Inggris dan konversi ke katakana
    for word in words:
        if isalpha(word):
            katakana = alkana.get_kana(word)
            if katakana:
                dict_rep[word] = katakana
    
    # Ganti kata-kata dalam teks
    for word, read in dict_rep.items():
        try:
            # Gunakan regex untuk mengganti hanya kata utuh
            pattern = r'\b' + re.escape(word) + r'\b'
            text = re.sub(pattern, read, text)
        except:
            pass
    
    return text