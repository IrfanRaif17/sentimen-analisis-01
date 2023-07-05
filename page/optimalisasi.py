from page.fetch import*
import streamlit as st
import pandas as pd
import ast
import unicodedata
import re
import nltk
import base64

with open('styles.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
list_stopword = []

# Fungsi untuk memisahkan hashtag dalam kalimat
def pisahkan_hashtag(kalimat):
    pola = r'#[A-Za-z0-9_]+'
    hasil = re.findall(pola, kalimat)
    for hashtag in hasil:
        kata_terpisah = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', hashtag)
        kata_terpisah = re.sub(r'([a-zA-Z])([0-9])', r'\1 \2', kata_terpisah)
        kalimat = kalimat.replace(hashtag, kata_terpisah)
    return kalimat

# Fungsi untuk menghapus karakter non-ASCII
def remove_non_ascii(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if unicodedata.category(c) != 'Mn')

# Fungsi menghapus nomer
def remove_number(text):
    return re.sub(r"\d+", " ", text)

# Fungsi menghapus tanda baca
def hapus_tanda_baca(text):
    return re.sub(r'[^\w\s]', '', text)

# Fungsi menghilangkan karakter khusus underscore
def remove_tweet_special(text):
    text = text.replace('_', ' ')
    return text

# Melakukan tokenisasi dengan NLTK
def word_tokenize(text):
    if not text:
        return []
    else:
        return nltk.word_tokenize(text)
    
# Menghilangkan stopword pada data
def stopword_removal(text):
    return [word for word in text if word.lower() not in list_stopword]
    
# Menggabungkan kata 
def make_sentence (text):
    return re.sub(r'\s+', ' ', ' '.join([i+' ' for i in text])).strip()

# Menghapus spasi ganda
def remove_multiple_space(text):
    return re.sub('\s+', ' ', text)

# Menghapus karakter tunggal
def remove_single_character_words(text):
    # Menggunakan ekspresi reguler untuk mencari kata-kata yang hanya terdiri dari satu karakter
    pattern = r'\b\w\b'
    result = re.sub(pattern, '', text)
    return result

def main():
    st.markdown('<p style="font-family: Times New Roman; font-size: 32px; font-weight: bold;">Optimalisasi Pra-proses</p>', unsafe_allow_html=True)
    st.write("Upload file CSV dengan nama 'df_tweet' yang berisi kolom 'text'.")

    # Upload file CSV
    uploaded_file = st.file_uploader("Upload file CSV", type=["csv"])

    # Upload file kamus slang
    uploaded_slang_file = st.file_uploader("Upload file kamus slang (kamus_slang_new.txt)", type=["txt"])

    # Up;oad file stopword_clean
    uploaded_stopword_file = st.file_uploader("Upload file stopword_clean (stopword_clean.txt)", type=["txt"])
    if uploaded_file is not None:
        try:
            df_tweet = pd.read_csv(uploaded_file)

            # Memisahkan hashtag

            df_tweet['split_hashtag'] = df_tweet['text'].apply(pisahkan_hashtag)

            # Case folding
            df_tweet['case_folding'] = df_tweet['split_hashtag'].str.lower()

            # Standarisasi dan tokenisasi data
            df_tweet['remove_nonascii'] = df_tweet['case_folding'].apply(remove_non_ascii)

            # Menghapus nomer
            df_tweet['remove_number'] = df_tweet['remove_nonascii'].apply(remove_number)

            # Menghapus tanda baca
            df_tweet['has_remove_punctuation'] = df_tweet['remove_number'].apply(hapus_tanda_baca)

            # Menghilangkan karakter khusus underscore
            df_tweet['remove_tweet_special'] = df_tweet['has_remove_punctuation'].apply(remove_tweet_special)

            # Menampilkan proses ke tampilan depat streamlit
            st.subheader('Hasil Tahap 1')
            st.write(df_tweet)

            if uploaded_slang_file is not None:
                try:
                    slang_file_contents = uploaded_slang_file.read().decode('utf-8')
                    slang_dict = ast.literal_eval(slang_file_contents)
                    slangs = {r"\b{}\b".format(k): v for k, v in slang_dict.items()}
                    df_tweet['tweet_prep_slang'] = df_tweet['remove_tweet_special'].replace(slangs, regex=True)
                    df_tweet['tweet_tokens'] = df_tweet['tweet_prep_slang'].apply(word_tokenize)
                    st.subheader('Hasil Tahap 2')
                    st.write(df_tweet[['remove_tweet_special','tweet_prep_slang', 'tweet_tokens']])
                except Exception as e:
                    st.error("Terjadi kesalahan dalam membaca file kamus slang. Pastikan file berformat teks (txt) dan sesuai format kamus slang.")
                    st.error(str(e))
            else:
                st.warning("Upload file kamus slang (kamus_slang_new.txt) untuk melanjutkan pemrosesan.")
            
            if uploaded_stopword_file is not None:
                try:
                    stopword_file_contents = uploaded_stopword_file.read().decode('utf-8')
                    list_stopword = stopword_file_contents.splitlines()
                    df_tweet['tweet_tokens_WSW'] = df_tweet['tweet_tokens'].apply(stopword_removal)
                    df_tweet['tweet_sentences'] = df_tweet['tweet_tokens_WSW'].apply(lambda text: make_sentence(text))
                    df_tweet['remove_multiple_space'] = df_tweet['tweet_sentences'].apply(remove_multiple_space)
                    df_tweet['tweet_clean'] = df_tweet['remove_multiple_space'].apply(remove_single_character_words)
                    st.subheader('Hasil Tahap 3')
                    st.write(df_tweet[['tweet_tokens','tweet_tokens_WSW','tweet_sentences','tweet_clean']])
                    
                    # Export ke CSV
                    if st.button("Export ke CSV"):
                        file_name = st.text_input("Masukkan nama file CSV:")
                        if file_name:
                            if file_name.endswith(".csv"):
                                csv_data = df_tweet.to_csv(index=False)
                                b64 = base64.b64encode(csv_data.encode()).decode()
                                href = f'<a href="data:file/csv;base64,{b64}" download="{file_name}">Download CSV</a>'
                                st.markdown(href, unsafe_allow_html=True)
                                st.success(f"File CSV dengan nama '{file_name}' berhasil diekspor.")
                            else:
                                st.error("Nama file harus berakhir dengan ekstensi .csv")
                        else:
                            st.warning("Masukkan nama file CSV terlebih dahulu.")

                    # Export ke XLSX
                    if st.button("Export ke XLSX"):
                        file_name = st.text_input("Masukkan nama file XLSX:")
                        if file_name:
                            if file_name.endswith(".xlsx"):
                                xlsx_data = df_tweet.to_excel(index=False)
                                b64 = base64.b64encode(xlsx_data).decode()
                                href = f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="{file_name}">Download XLSX</a>'
                                st.markdown(href, unsafe_allow_html=True)
                                st.success(f"File XLSX dengan nama '{file_name}' berhasil diekspor.")
                            else:
                                st.error("Nama file harus berakhir dengan ekstensi .xlsx")
                        else:
                            st.warning("Masukkan nama file XLSX terlebih dahulu.")




                except Exception as e:
                    st.error("Terjadi kesalahan dalam membaca file stopword. Pastikan file berformat teks (txt) dan sesuai format stopword.")
                    st.error(str(e))
            else:
                st.warning("Upload file stopword_clean (stopword_clean.txt) untuk melanjutkan pemrosesan.")


            
            




        except Exception as e:
            st.error("Terjadi kesalahan dalam membaca file. Pastikan file CSV memiliki kolom 'text'.")
            st.error(str(e))


if __name__ == "__main__":
    main()