import streamlit as st
import pandas as pd
import nltk
import re
import csv
import string
import unicodedata
from nltk.tokenize import word_tokenize
import base64
from page import ConfusionMatrix

with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# Set NLTK data directory
nltk.data.path.append("/path/to/nltk_data")

# Download 'punkt' if not already downloaded
if not nltk.data.find('tokenizers/punkt'):
    nltk.download('punkt', download_dir='/path/to/download_directory')
    
# Set up stopwords and stemmer
nltk.download('stopwords')
nltk.download('punkt')
stopwords = set(nltk.corpus.stopwords.words('indonesian'))

# Fungsi untuk memisahkan hashtag dalam kalimat
def pisahkan_hashtag(kalimat):
    pola = r'#[A-Za-z0-9_]+'
    hasil = re.findall(pola, kalimat)
    for hashtag in hasil:
        kata_terpisah = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', hashtag)
        kata_terpisah = re.sub(r'([a-zA-Z])([0-9])', r'\1 \2', kata_terpisah)
        kalimat = kalimat.replace(hashtag, kata_terpisah)
    return kalimat

# Fungsi untuk menghapus tanda baca menggunakan regex
def hapus_tanda_baca(kata):
    return re.sub(r'[^\w\s-]', '', kata)

# Fungsi untuk melakukan preprocessing pada kolom teks
def preprocess(text):
    # Menghapus karakter non-ASCII
    text = remove_non_ascii(text)

    # Remove URLs, mentions, and hashtags
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'\@\w+|\#', '', text)

    # Tokenisasi kalimat menjadi kata-kata
    kata_kata = word_tokenize(text)

    # Menghapus tanda baca dari setiap kata
    kata_kata_tanpa_tanda_baca = [hapus_tanda_baca(kata) for kata in kata_kata]

    # Menggabungkan kata-kata kembali menjadi kalimat
    kalimat_tanpa_tanda_baca = ' '.join(kata_kata_tanpa_tanda_baca)

    # Menggantikan tanda baca dengan spasi tunggal menggunakan regex
    kalimat_final = re.sub(r'(?<=[^\w\s-])', ' ', kalimat_tanpa_tanda_baca)

    # Menggantikan multiple spasi dengan satu spasi menggunakan regex
    kalimat_tanpa_spasi_ganda = re.sub(r'\s+', ' ', kalimat_final)

    # Remove special characters and digits
    kalimat_tanpa_tanda_baca_dan_digit = re.sub(r'[^\w\s-]', '', kalimat_tanpa_spasi_ganda)
    kalimat_tanpa_digit = re.sub(r'\d+', '', kalimat_tanpa_tanda_baca_dan_digit)

    # Convert to lowercase
    kalimat_final = kalimat_tanpa_digit.lower()

    # Remove whitespace leading & trailing
    kalimat_final = kalimat_final.strip()

    # Remove single char
    kalimat_final = re.sub(r"\b[a-zA-Z]\b", "", kalimat_final)

    return kalimat_final

def remove_non_ascii(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if unicodedata.category(c) != 'Mn')

# Fungsi untuk memuat kamus KBBI dari file
def muat_kamus_kbbi(file):
    extension = file.name.split(".")[-1]
    if extension == "csv":
        return pd.read_csv(file, header=None, names=["kata"], encoding='utf-8')
    elif extension == "xls" or extension == "xlsx":
        return pd.read_excel(file, header=None, names=["kata"])
    elif extension == "txt":
        with open(file.name, "r", encoding="utf-8") as f:
            data = f.read().splitlines()
        return pd.DataFrame(data, columns=["kata"])
    else:
        raise ValueError("Format file tidak didukung. Harap gunakan file dengan format CSV, TXT, XLS, atau XLSX.")

# Fungsi untuk mencari kata tidak baku
def cari_kata_tidak_baku(kalimat, kamus):
    kata_kalimat = set(kalimat.split())
    kata_baku = set(kamus["kata"])
    kata_tidak_baku = kata_kalimat.difference(kata_baku)
    return list(kata_tidak_baku)

def hapus_kata_berimbuhan(tweets):
    hapus_kata = []
    for tweet in tweets:
        kata_kata = re.findall(r'\w+', tweet)
        for kata in kata_kata:
            pref = cek_prefiks(kata)
            suf = cek_sufiks(kata)
            inf = cek_infiks(kata)
            kon = cek_konfiks(kata)
            if not pref and not suf and not inf and not kon:
                hapus_kata.append(kata)  # Menambah kata ke dalam list hapus_kata jika memiliki imbuhan

    return hapus_kata

# Function to export results to a text file
def export_to_txt(kata_tidak_baku_unik, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for kata in kata_tidak_baku_unik:
            f.write(f"'{kata}':'....',\n")

def export_to_csv(kata_tidak_baku_unik, output_file):
    data = []
    for kata in kata_tidak_baku_unik:
        data.append([kata, "...."])

    df_output = pd.DataFrame(data, columns=["tidak_baku", "normalisasi"])
    df_output.to_csv(output_file, index=False, encoding='utf-8')

def cek_prefiks(kata):
    prefiks = ['ber', 'me', 'di', 'ter', 'ke', 'se', 'pe']

    for pref in prefiks:
        if kata.startswith(pref):
            return pref

    return None

def cek_sufiks(kata):
    sufiks = ['kan', 'an', 'lah', 'nya']

    for suf in sufiks:
        if kata.endswith(suf):
            return suf

    return None

def cek_infiks(kata):
    infiks = ['el', 'em']

    for inf in infiks:
        if inf in kata:
            return inf

    return None

def cek_konfiks(kata):
    konfiks = ['me', 'mem', 'men', 'meng', 'meny', 'pe', 'pem', 'pen', 'peng', 'peny']

    for kon in konfiks:
        if kata.startswith(kon) and kata.endswith('i'):
            return kon + 'i'

    return None

def main():
    st.markdown('<p style="font-family: Times New Roman; font-size: 32px; font-weight: bold;">Pendeteksi Kata Slang</p>', unsafe_allow_html=True)
    st.write("Upload file CSV, TXT, XLS, or XLSX untuk memuat kamus KBBI.")

    # Upload file kamus KBBI
    uploaded_file_kamus = st.file_uploader("Upload file kamus KBBI", type=["csv", "txt", "xls", "xlsx"])

    if uploaded_file_kamus is not None:
        try:
            kamus_kbbi = muat_kamus_kbbi(uploaded_file_kamus)

            # Unggah file
            uploaded_file_data = st.file_uploader("Upload file data yang akan diproses", type=["csv"])
            
            if uploaded_file_data is not None:
                # Baca file CSV
                df_data = pd.read_csv(uploaded_file_data, encoding='utf-8')

            # Tampilkan kolom yang tersedia untuk dipilih
                st.write("Kolom yang tersedia dalam data:")
                st.write(df_data.columns.tolist())

            # Pilih kolom yang berisi teks
                kolom_teks = st.selectbox("Pilih kolom yang berisi teks:", df_data.columns)

                # Memisahkan hashtag dari kolom yang dipilih
                df_data['split_hashtag'] = df_data[kolom_teks].apply(pisahkan_hashtag)

                # Preprocessing
                df_data['preprocessing'] = df_data['split_hashtag'].apply(preprocess)

                # Menampilkan hasil preprocessing
                st.write("Hasil Preprocessing:")
                st.dataframe(df_data)

                # Mencari kata tidak baku
                df_data['kata_tidak_baku'] = df_data['preprocessing'].apply(lambda x: cari_kata_tidak_baku(x, kamus_kbbi))

                # Menghapus kata berimbuhan
                df_data['kata_tidak_baku_clean'] = df_data['kata_tidak_baku'].apply(hapus_kata_berimbuhan)

                # Mengumpulkan semua kata tidak baku menjadi satu dan menghapus kata yang sama
                kata_tidak_baku_unik = set([kata for sublist in df_data['kata_tidak_baku_clean'] for kata in sublist])

                st.write("Kata Tidak Baku:")

                # Fungsi untuk mengekspor ke file teks dan menghasilkan tautan unduh
                def export_to_txt(kata_tidak_baku_unik, output_file):
                    with open(output_file, 'w', encoding='utf-8') as f:
                        for kata in kata_tidak_baku_unik:
                            f.write(f"'{kata}':'....',\n")

                    # Create href tag to download the file
                    href = get_download_link(output_file, 'TXT')

                    # Display the download link
                    st.markdown(href, unsafe_allow_html=True)

                # Fungsi untuk mengekspor ke file CSV dan menghasilkan tautan unduh
                def export_to_csv(kata_tidak_baku_unik, output_file):
                    data = []
                    for kata in kata_tidak_baku_unik:
                        data.append([kata, "...."])

                    df_output = pd.DataFrame(data, columns=["tidak_baku", "normalisasi"])
                    df_output.to_csv(output_file, index=False, encoding='utf-8')

                    # Create href tag to download the file
                    href = get_download_link(output_file, 'CSV')

                    # Display the download link
                    st.markdown(href, unsafe_allow_html=True)

                # Fungsi untuk menghasilkan tautan unduh file
                def get_download_link(file_path, file_type):
                    with open(file_path, 'rb') as file:
                        contents = file.read()
                        base64_encoded = base64.b64encode(contents).decode()
                        href = f'<a href="data:text/{file_type};base64,{base64_encoded}" download="{file_path}">Download {file_type}</a>'
                    return href

                # Export to text file
                if st.button("Export ke TXT"):
                    file_name = "kamus_slang_new.txt"
                    export_to_txt(kata_tidak_baku_unik, file_name)
                    st.success(f"Data kata tidak baku telah diekspor ke file: {file_name}")

                # Export to CSV file
                if st.button("Export ke CSV"):
                    file_name = "kamus_slang_new.csv"
                    export_to_csv(kata_tidak_baku_unik, file_name)
                    st.success(f"Data kata tidak baku telah diekspor ke file: {file_name}")

        except Exception as e:
            st.error("Terjadi kesalahan dalam membaca file.")
            st.error(str(e))

if __name__ == '__main__':
    main()