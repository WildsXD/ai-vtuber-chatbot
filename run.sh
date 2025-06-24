#!/bin/bash

echo "========================================"
echo "   Instalasi AI-Waifu-Vtuber (Linux)   "
echo "========================================"

# Cek jika Python terinstal
if command -v python3 &>/dev/null; then
    python_cmd="python3"
elif command -v python &>/dev/null; then
    python_cmd="python"
else
    echo "Python tidak ditemukan. Silakan instal Python 3.8 atau lebih tinggi."
    exit 1
fi

echo "Python terdeteksi: $($python_cmd --version)"

# Cek versi Python
py_version=$($python_cmd -c "import sys; print('{}.{}'.format(sys.version_info.major, sys.version_info.minor))")
py_major=$(echo $py_version | cut -d. -f1)
py_minor=$(echo $py_version | cut -d. -f2)

if [ "$py_major" -lt 3 ] || ([ "$py_major" -eq 3 ] && [ "$py_minor" -lt 8 ]); then
    echo "Program ini membutuhkan Python 3.8 atau lebih tinggi."
    echo "Versi terdeteksi: $py_version"
    exit 1
fi

# Cek jika pip terinstal
if ! $python_cmd -m pip --version &>/dev/null; then
    echo "pip tidak ditemukan. Mencoba menginstal pip..."
    
    # Metode 1: ensurepip
    if $python_cmd -m ensurepip --upgrade &>/dev/null; then
        echo "pip berhasil diinstal dengan ensurepip."
    else
        echo "Instalasi dengan ensurepip gagal. Mencoba metode alternatif..."
        
        # Metode 2: get-pip.py
        echo "Mengunduh get-pip.py..."
        if command -v curl &>/dev/null; then
            curl -s https://bootstrap.pypa.io/get-pip.py -o get-pip.py
        elif command -v wget &>/dev/null; then
            wget -q https://bootstrap.pypa.io/get-pip.py
        else
            echo "curl atau wget tidak ditemukan. Silakan instal pip secara manual:"
            echo "https://pip.pypa.io/en/stable/installation/"
            exit 1
        fi
        
        $python_cmd get-pip.py
        rm -f get-pip.py
        
        if ! $python_cmd -m pip --version &>/dev/null; then
            echo "Gagal menginstal pip. Silakan instal pip secara manual."
            exit 1
        else
            echo "pip berhasil diinstal dengan get-pip.py."
        fi
    fi
fi

# Upgrade pip
echo "Mengupgrade pip..."
$python_cmd -m pip install --upgrade pip

# Instal dependensi
echo "Menginstal dependensi dari requirements.txt..."
$python_cmd -m pip install -r requirements.txt

# Instal MeCab untuk Linux
echo "Menginstal MeCab untuk Linux..."
if command -v apt-get &>/dev/null; then
    # Debian/Ubuntu
    echo "Distro berbasis Debian/Ubuntu terdeteksi."
    sudo apt-get update
    sudo apt-get install -y mecab libmecab-dev mecab-ipadic mecab-ipadic-utf8
elif command -v yum &>/dev/null; then
    # CentOS/RHEL
    echo "Distro berbasis CentOS/RHEL terdeteksi."
    sudo yum install -y mecab mecab-devel mecab-ipadic
elif command -v pacman &>/dev/null; then
    # Arch Linux
    echo "Distro berbasis Arch Linux terdeteksi."
    sudo pacman -S mecab mecab-ipadic
elif command -v brew &>/dev/null; then
    # macOS dengan Homebrew
    echo "macOS dengan Homebrew terdeteksi."
    brew install mecab mecab-ipadic
else
    echo "Paket manager tidak dikenali. Silakan instal MeCab secara manual."
fi

# Instal unidic-lite
$python_cmd -m pip install mecab-python3 unidic-lite

echo ""
echo "Instalasi selesai!"
echo "Untuk menjalankan program, gunakan perintah: python run.py"
echo ""

# Tanya pengguna apakah ingin langsung menjalankan program
read -p "Apakah Anda ingin menjalankan program sekarang? (y/n): " run_now
if [[ $run_now == "y" || $run_now == "Y" ]]; then
    $python_cmd run.py
fi 