import streamlit as st
import pandas as pd
import re
import unicodedata
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import ast
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import csv
import nltk
from page import analisissentimen

# Then use it in your code
PAGES = {
    "Analisis Sentimen InSet": analisissentimen,
    # Other pages
}

# Set NLTK data directory
nltk.data.path.append("/path/to/nltk_data")

# Download 'punkt' if not already downloaded
if not nltk.data.find('tokenizers/punkt'):
    nltk.download('punkt', download_dir='/path/to/download_directory')

# Fungsi untuk memisahkan hashtag
def pisahkan_hashtag(kalimat):
    pola = r'#[A-Za-z0-9_]+'
    hasil = re.findall(pola, kalimat)
    for hashtag in hasil:
        kata_terpisah = re.sub(r'([a-z])([A-Z])', r'\1 \2', hashtag)
        kalimat = kalimat.replace(hashtag, kata_terpisah)
    return kalimat

# Fungsi untuk menghapus tanda baca menggunakan regex
def hapus_tanda_baca(kata):
    return re.sub(r'[^\w\s-]', '', kata)

# Fungsi untuk menghapus karakter non-ASCII
def remove_non_ascii(text):
    return ''.join(c for c in unicodedata.normalize('NFKD', text) if unicodedata.category(c) != 'Mn')

# Fungsi untuk melakukan preprocessing pada kolom teks
def preprocess_text(text, stop_words=None):
    text = remove_non_ascii(text)
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)
    text = re.sub(r'\@\w+|\#', '', text)
    kata_kata = word_tokenize(text)
    
    if stop_words:
        kata_kata_tanpa_stopwords = [kata for kata in kata_kata if kata.lower() not in stop_words]
    else:
        kata_kata_tanpa_stopwords = kata_kata
    
    kata_kata_tanpa_tanda_baca = [hapus_tanda_baca(kata) for kata in kata_kata_tanpa_stopwords]
    kalimat_tanpa_tanda_baca = ' '.join(kata_kata_tanpa_tanda_baca)
    kalimat_final = re.sub(r'(?<=[^\w\s-])', ' ', kalimat_tanpa_tanda_baca)
    kalimat_tanpa_spasi_ganda = re.sub(r'\s+', ' ', kalimat_final)
    kalimat_tanpa_tanda_baca_dan_digit = re.sub(r'[^\w\s-]', '', kalimat_tanpa_spasi_ganda)
    kalimat_tanpa_digit = re.sub(r'\d+', '', kalimat_tanpa_tanda_baca_dan_digit)
    kalimat_final = kalimat_tanpa_digit.lower()
    kalimat_final = kalimat_final.strip()
    kalimat_final = re.sub(r"\b[a-zA-Z]\b", "", kalimat_final)
    
    return kalimat_final

# Fungsi untuk analisis sentimen
def sentiment_analysis_lexicon_indonesia(text, lexicon_positive, lexicon_negative):
    score = 0
    positive_found = []
    negative_found = []
    for word in text:
        if word in lexicon_positive:
            score += lexicon_positive[word]
            positive_found.append((word, lexicon_positive[word]))
        if word in lexicon_negative:
            score += lexicon_negative[word]
            negative_found.append((word, lexicon_negative[word]))
    polarity = ''
    if score > 0:
        polarity = 'positive'
    elif score < 0:
        polarity = 'negative'
    else:
        polarity = 'neutral'
    return score, polarity, positive_found, negative_found

# Function to group all positive/negative words
def words_with_sentiment(text, lexicon_positive, lexicon_negative):
    positive_words=[]
    negative_words=[]
    for word in text:
        score_pos = 0
        score_neg = 0
        if (word in lexicon_positive):
            score_pos = lexicon_positive[word]
        if (word in lexicon_negative):
            score_neg = lexicon_negative[word]
        
        if (score_pos + score_neg > 0):
            positive_words.append(word)
        elif (score_pos + score_neg < 0):
            negative_words.append(word)
            
    return positive_words, negative_words

def main():
    st.markdown('<p style="font-family: Times New Roman; font-size: 32px; font-weight: bold;">Analisis Sentimen InSet</p>', unsafe_allow_html=True)

    # Unggah file
    uploaded_file_data = st.file_uploader("Upload file data yang akan diproses", type=["csv"])
    if uploaded_file_data is not None:
        # Read CSV file
        data = pd.read_csv(uploaded_file_data, encoding='utf-8')

        # Display available columns for selection
        st.write("Kolom yang tersedia dalam data:")
        st.write(data.columns.tolist())

                # Select column containing text
        kolom_teks = st.selectbox("Pilih kolom yang berisi teks:", data.columns)
        
        # Periksa apakah kolom yang dipilih oleh pengguna ada dalam DataFrame
        if kolom_teks in data.columns:
            data['pisah_hashtag&kata'] = data[kolom_teks].apply(pisahkan_hashtag)
            data['text_cleaning'] = data['pisah_hashtag&kata'].apply(lambda x: preprocess_text(x))
            st.write("Hasil setelah cleaning:")
            st.dataframe(data)
            
            # Upload bahan normalisasi
            uploaded_normalisasi = st.file_uploader("Upload bahan normalisasi TXT", type="txt")
            
            if uploaded_normalisasi:
                contents = uploaded_normalisasi.getvalue().decode("utf-8")
                slangs_dict = ast.literal_eval(contents)
                slangs = {r"\b{}\b".format(k): v for k, v in slangs_dict.items()}

                data['text_normalisasi'] = data['text_cleaning'].replace(slangs, regex=True)
                st.write("Hasil setelah normalisasi:")
                st.write(data[['text_cleaning', 'text_normalisasi']])
                
                # Checkbox to use additional stopwords
                use_stopwords = st.checkbox("Gunakan stopwords tambahan")

                if use_stopwords:
                    # Upload stopwords
                    uploaded_stopwords = st.file_uploader("Upload file stopwords TXT", type="txt")
                    
                    stop_words = set(stopwords.words('indonesian'))
                    stop_words.update(["yg", "dg", "rt", "dgn", "ny", "d", 'klo', 
                                       'kalo', 'amp', 'biar', 'bikin', 'bilang', 
                                       'gak', 'ga', 'krn', 'nya', 'nih', 'sih', 
                                       'si', 'tau', 'tdk', 'tuh', 'utk', 'ya', 
                                       'jd', 'jgn', 'sdh', 'aja', 'n', 't', 
                                       'nyg', 'hehe', 'pen', 'u', 'nan', 'loh', 'rt',
                                       '&amp', 'yah', '-',])
                    
                    if uploaded_stopwords:
                        uploaded_stopwords_content = uploaded_stopwords.getvalue().decode("utf-8").splitlines()
                        stop_words.update(uploaded_stopwords_content)
                    
                    # Data sebelum dihapus stopwords
                    st.write("Data sebelum dihapus stopwords:")
                    st.write(data[['text_normalisasi']])
                    
                    data['text_cleaning'] = data['text_normalisasi'].apply(lambda x: preprocess_text(x, stop_words))
                    
                    # Data setelah dihapus stopwords
                    st.write("Data setelah dihapus stopwords:")
                    st.write(data[['text_cleaning']])
                    
                else:
                    data['text_cleaning'] = data['text_normalisasi'].apply(preprocess_text)
                    st.write("Hasil setelah normalisasi tanpa menggunakan stopwords:")
                    st.write(data[['text_cleaning']])

                # Upload leksikon positif dan negatif
                uploaded_lexicon_positive = st.file_uploader("Upload lexicon positif.CSV", type="csv")
                uploaded_lexicon_negative = st.file_uploader("Upload lexicon negatif.CSV", type="csv")
                
                if uploaded_lexicon_positive and uploaded_lexicon_negative:
                    lexicon_positive = {}
                    lexicon_negative = {}

                    positive_data = pd.read_csv(uploaded_lexicon_positive)
                    negative_data = pd.read_csv(uploaded_lexicon_negative)
                    
                    for i, row in positive_data.iterrows():
                        lexicon_positive[row[0]] = int(row[1])
                    for i, row in negative_data.iterrows():
                        lexicon_negative[row[0]] = int(row[1])

                    data['tweet_tokens'] = data['text_cleaning'].apply(word_tokenize)
                    
                    results = data['tweet_tokens'].apply(lambda x: sentiment_analysis_lexicon_indonesia(x, lexicon_positive=lexicon_positive, lexicon_negative=lexicon_negative))
                    results = list(zip(*results))
                    data['polarity_score'] = results[0]
                    data['polarity'] = results[1]

                    # Unpack positive and negative words from results
                    data['positive_words'] = [", ".join([word[0] for word in positive]) for positive in results[2]]
                    data['negative_words'] = [", ".join([word[0] for word in negative]) for negative in results[3]]
                    
                    st.write("Hasil analisis sentimen:")
                    st.write(data[['tweet_tokens', 'polarity', 'polarity_score', 'positive_words', 'negative_words']])
                    
                    csv = data.to_csv(index=False)
                    st.download_button(label="Download hasil CSV", data=csv, file_name='hasil_tweets_data.csv', mime='text/csv')

                    st.write(data['polarity'].value_counts())

                    fig, ax = plt.subplots(figsize=(6, 6))
                    sizes = [count for count in data['polarity'].value_counts()]
                    labels = list(data['polarity'].value_counts().index)
                    explode = [0.1 if i == 0 else 0 for i in range(len(sizes))]
                    ax.pie(x=sizes, labels=labels, autopct='%1.1f%%', explode=explode, textprops={'fontsize': 14})
                    ax.set_title('Sentiment Polarity on Tweets Data \n Persentase Polarity dari Semua data', fontsize=16, pad=20)
                    st.pyplot(fig)
                    
                    list_words = ''
                    for tweet in data['tweet_tokens']:
                        for word in tweet:
                            list_words += ' ' + (word)
                    
                    wordcloud = WordCloud(width=600, height=400, min_font_size=10).generate(list_words)
                    fig, ax = plt.subplots(figsize=(8, 6))
                    st.write("Sebaran Semua data yang Paling Bnayak Muncul:")
                    ax.set_title('Word Cloud of Tweets Data \n Semakin Besar Kata Semakin Banyak jumlah frekuensi', fontsize=18)
                    ax.grid(False)
                    ax.imshow(wordcloud)
                    ax.axis('off')
                    st.pyplot(fig)

                    # Visualize positive and negative word clouds
                    sentiment_words = data['tweet_tokens'].apply(lambda x: words_with_sentiment(x, lexicon_positive, lexicon_negative))
                    sentiment_words = list(zip(*sentiment_words))
                    positive_words = sentiment_words[0]
                    negative_words = sentiment_words[1]

                    fig, ax = plt.subplots(1, 2, figsize=(12, 10))
                    list_words_positive = ''
                    for row_word in positive_words:
                        for word in row_word:
                            list_words_positive += ' ' + (word)
                    wordcloud_positive = WordCloud(width=800, height=600, background_color='black', colormap='Greens', min_font_size=10).generate(list_words_positive)
                    st.write("Sebaran Data Positive dan Negative:")
                    ax[0].set_title('Word Cloud of Positive Words on Tweets Data \n (based on Indonesia Sentiment Lexicon)', fontsize=14)
                    ax[0].grid(False)
                    ax[0].imshow(wordcloud_positive)
                    fig.tight_layout(pad=0)
                    ax[0].axis('off')

                    list_words_negative = ''
                    for row_word in negative_words:
                        for word in row_word:
                            list_words_negative += ' ' + (word)
                    wordcloud_negative = WordCloud(width=800, height=600, background_color='black', colormap='Reds', min_font_size=10).generate(list_words_negative)
                    ax[1].set_title('Word Cloud of Negative Words on Tweets Data \n (based on Indonesia Sentiment Lexicon)', fontsize=14)
                    ax[1].grid(False)
                    ax[1].imshow(wordcloud_negative)
                    fig.tight_layout(pad=0)
                    ax[1].axis('off')
                    st.pyplot(fig)
    else:
        st.write("Unggah file CSV untuk memulai.")

if __name__ == "__main__":
    main()
