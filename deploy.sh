#!/bin/bash

# Menampilkan pesan untuk memulai proses
echo "Memulai proses deployment..."

# Langkah 1: Membuat virtual environment
echo "Membuat virtual environment..."
python -m venv venv

# Langkah 2: Mengaktifkan virtual environment
echo "Mengaktifkan virtual environment..."
# Untuk Windows, gunakan:
# venv\Scripts\activate
# Untuk macOS/Linux, gunakan:
source venv/bin/activate

# Langkah 3: Memperbarui pip
echo "Memperbarui pip..."
pip install --upgrade pip

# Langkah 4: Menginstal dependensi
echo "Menginstal dependensi dari requirements.txt..."
pip install -r requirements.txt

# Langkah 5: Menjalankan aplikasi Streamlit
echo "Menjalankan aplikasi Streamlit..."
streamlit run app.py

# Menampilkan pesan selesai
echo "Deployment selesai."
