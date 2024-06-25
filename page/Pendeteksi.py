import streamlit as st
import pandas as pd
import nltk
import re
import string
import unicodedata
from nltk.tokenize import word_tokenize
import os
import tempfile

# Add your custom stylesheet
with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Set NLTK data directory to a temporary directory
nltk_data_dir = tempfile.mkdtemp()

# Ensure the NLTK data directory exists
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)

# Download 'punkt' and 'stopwords' if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', download_dir=nltk_data_dir)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', download_dir=nltk_data_dir)

# Set up stopwords and stemmer
stopwords = set(nltk.corpus.stopwords.words('indonesian'))

# Function to split hashtags in a sentence
def pisahkan_hashtag(kalimat):
    pola = r'#[A-Za-z0-9_]+'
    hasil = re.findall(pola, kalimat)
    for hashtag in hasil:
        kata_terpisah = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', hashtag)
        kata_terpisah = re.sub(r'([a-zA-Z])([0-9])', r'\1 \2', kata_terpisah)
        kalimat = kalimat.replace(hashtag, kata_terpisah)
    return kalimat

# Function to remove punctuation using regex
def hapus_tanda_baca(kata):
    return re.sub(r'[^\w\s-]', '', kata)

# Function to preprocess text column
def preprocess(text):
    # Remove non-ASCII characters
    text = remove_non_ascii(text)

    # Remove URLs, mentions, and hashtags
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'\@\w+|\#', '', text)

    # Tokenize sentence into words
    kata_kata = word_tokenize(text)

    # Remove punctuation from each word
    kata_kata_tanpa_tanda_baca = [hapus_tanda_baca(kata) for kata in kata_kata]

    # Join words back into a sentence
    kalimat_tanpa_tanda_baca = ' '.join(kata_kata_tanpa_tanda_baca)

    # Replace punctuation with a single space using regex
    kalimat_final = re.sub(r'(?<=[^\w\s-])', ' ', kalimat_tanpa_tanda_baca)

    # Replace multiple spaces with a single space using regex
    kalimat_tanpa_spasi_ganda = re.sub(r'\s+', ' ', kalimat_final)

    # Remove special characters and digits
    kalimat_tanpa_tanda_baca_dan_digit = re.sub(r'[^\w\s-]', '', kalimat_tanpa_spasi_ganda)
    kalimat_tanpa_digit = re.sub(r'\d+', '', kalimat_tanpa_tanda_baca_dan_digit)

    # Convert to lowercase
    kalimat_final = kalimat_tanpa_digit.lower()

    # Remove whitespace leading & trailing
    kalimat_final = kalimat_final.strip()

    # Remove single characters
    kalimat_final = re.sub(r"\b[a-zA-Z]\b", "", kalimat_final)

    return kalimat_final

# Function to remove non-ASCII characters
def remove_non_ascii(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if unicodedata.category(c) != 'Mn')

# Function to load KBBI dictionary from file
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

# Function to find non-standard words
def cari_kata_tidak_baku(kalimat, kamus):
    kata_kalimat = set(kalimat.split())
    kata_baku = set(kamus["kata"])
    kata_tidak_baku = kata_kalimat.difference(kata_baku)
    return list(kata_tidak_baku)

# Function to remove words with affixes
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

# Function to check prefixes
def cek_prefiks(kata):
    prefiks = ['ber', 'me', 'di', 'ter', 'ke', 'se', 'pe']
    for pref in prefiks:
        if kata.startswith(pref):
            return pref
    return None

# Function to check suffixes
def cek_sufiks(kata):
    sufiks = ['kan', 'an', 'lah', 'nya']
    for suf in sufiks:
        if kata.endswith(suf):
            return suf
    return None

# Function to check infixes
def cek_infiks(kata):
    infiks = ['el', 'em']
    for inf in infiks:
        if inf in kata:
            return inf
    return None

# Function to check confixes
def cek_konfiks(kata):
    konfiks = ['me', 'mem', 'men', 'meng', 'meny', 'pe', 'pem', 'pen', 'peng', 'peny']
    for kon in konfiks:
        if kata.startswith(kon) and kata.endswith('i'):
            return kon + 'i'
    return None

def main():
    st.markdown('<p style="font-family: Times New Roman; font-size: 32px; font-weight: bold;">Pendeteksi Kata Slang</p>', unsafe_allow_html=True)
    st.write("Upload file CSV, TXT, XLS, or XLSX untuk memuat kamus KBBI.")

    # Upload KBBI dictionary file
    uploaded_file_kamus = st.file_uploader("Upload file kamus KBBI", type=["csv", "txt", "xls", "xlsx"])

    if uploaded_file_kamus is not None:
        try:
            kamus_kbbi = muat_kamus_kbbi(uploaded_file_kamus)

            # Upload data file to be processed
            uploaded_file_data = st.file_uploader("Upload file data yang akan diproses", type=["csv"])
            
            if uploaded_file_data is not None:
                # Read CSV file
                df_data = pd.read_csv(uploaded_file_data, encoding='utf-8')

                # Display available columns for selection
                st.write("Kolom yang tersedia dalam data:")
                st.write(df_data.columns.tolist())

                # Select column containing text
                kolom_teks = st.selectbox("Pilih kolom yang berisi teks:", df_data.columns)

                # Split hashtags from selected column
                df_data['split_hashtag'] = df_data[kolom_teks].apply(pisahkan_hashtag)

                # Preprocess the text
                df_data['preprocessing'] = df_data['split_hashtag'].apply(preprocess)

                # Display preprocessing results
                st.write("Hasil Preprocessing:")
                st.dataframe(df_data)

                # Find non-standard words
                df_data['kata_tidak_baku'] = df_data['preprocessing'].apply(lambda x: cari_kata_tidak_baku(x, kamus_kbbi))

                # Remove words with affixes
                df_data['kata_tidak_baku_clean'] = df_data['kata_tidak_baku'].apply(hapus_kata_berimbuhan)

                # Collect all unique non-standard words
                kata_tidak_baku_unik = set([kata for sublist in df_data['kata_tidak_baku_clean'] for kata in sublist])

                st.write("Kata Tidak Baku:")

                # Export to text file and generate download button
                def export_to_txt(kata_tidak_baku_unik):
                    return "\n".join(kata_tidak_baku_unik)

                # Export to CSV file and generate download button
                def export_to_csv(kata_tidak_baku_unik):
                    data = [[kata, "...."] for kata in kata_tidak_baku_unik]
                    df_output = pd.DataFrame(data, columns=["tidak_baku", "normalisasi"])
                    return df_output.to_csv(index=False, encoding='utf-8')

                # Create TXT download button
                txt_data = export_to_txt(kata_tidak_baku_unik)
                st.download_button(
                    label="Download TXT",
                    data=txt_data,
                    file_name="kamus_slang_new.txt",
                    mime="text/plain"
                )

                # Create CSV download button
                csv_data = export_to_csv(kata_tidak_baku_unik)
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name="kamus_slang_new.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error("Terjadi kesalahan dalam membaca file.")
            st.error(str(e))

if __name__ == '__main__':
    main()
