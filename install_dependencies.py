import sys
import subprocess
import os
import platform

def check_python():
    print("Memeriksa versi Python...")
    major = sys.version_info.major
    minor = sys.version_info.minor
    
    if major < 3 or (major == 3 and minor < 8):
        print(f"Python versi {major}.{minor} terdeteksi.")
        print("Program ini membutuhkan Python 3.8 atau lebih tinggi.")
        return False
    
    print(f"Python versi {major}.{minor} terdeteksi. ✓")
    return True

def install_pip():
    print("Memeriksa pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "--version"])
        print("pip sudah terinstal. ✓")
        return True
    except:
        print("pip tidak ditemukan. Mencoba menginstal pip...")
        
        # Metode 1: ensurepip
        try:
            subprocess.check_call([sys.executable, "-m", "ensurepip", "--upgrade"])
            print("pip berhasil diinstal dengan ensurepip. ✓")
            return True
        except:
            print("Instalasi dengan ensurepip gagal. Mencoba metode alternatif...")
        
        # Metode 2: get-pip.py
        try:
            import urllib.request
            print("Mengunduh get-pip.py...")
            urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", "get-pip.py")
            
            subprocess.check_call([sys.executable, "get-pip.py"])
            
            # Bersihkan
            if os.path.exists("get-pip.py"):
                os.remove("get-pip.py")
                
            print("pip berhasil diinstal dengan get-pip.py. ✓")
            return True
        except Exception as e:
            print(f"Gagal menginstal pip: {e}")
            print("Silakan instal pip secara manual: https://pip.pypa.io/en/stable/installation/")
            return False

def upgrade_pip():
    print("Mengupgrade pip...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        print("pip berhasil diupgrade. ✓")
        return True
    except Exception as e:
        print(f"Gagal mengupgrade pip: {e}")
        return False

def install_requirements():
    print("Menginstal dependensi dari requirements.txt...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Semua dependensi berhasil diinstal. ✓")
        return True
    except Exception as e:
        print(f"Gagal menginstal dependensi: {e}")
        return False

def install_mecab():
    print("Menginstal MeCab dan unidic-lite...")
    try:
        if platform.system() == "Windows":
            # Windows memerlukan penanganan khusus untuk MeCab
            subprocess.check_call([sys.executable, "-m", "pip", "install", "unidic-lite"])
        else:
            # Untuk Linux/Mac
            subprocess.check_call([sys.executable, "-m", "pip", "install", "mecab-python3", "unidic-lite"])
        print("MeCab berhasil diinstal. ✓")
        return True
    except Exception as e:
        print(f"Peringatan: Gagal menginstal MeCab: {e}")
        print("Program masih bisa berjalan tetapi fitur katakana_converter mungkin tidak berfungsi.")
        return False

def main():
    print("=" * 50)
    print("Instalasi Dependensi untuk AI-Waifu-Vtuber")
    print("=" * 50)
    
    if not check_python():
        input("Tekan Enter untuk keluar...")
        return
    
    if not install_pip():
        input("Tekan Enter untuk keluar...")
        return
    
    upgrade_pip()
    install_requirements()
    install_mecab()
    
    print("\nInstalasi selesai!")
    print("Untuk menjalankan program, gunakan perintah: python run.py")
    input("Tekan Enter untuk keluar...")

if __name__ == "__main__":
    main() 