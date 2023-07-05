from page.fetch import*

def main():
	front_up()


import streamlit as st
import pandas as pd
import csv

# Fungsi untuk memuat kamus positif dan negatif dari file CSV
def load_lexicon(file_path):
    lexicon = dict()
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0] != 'word':  # skip header row
                lexicon[row[0]] = int(row[1])
    return lexicon

# Fungsi untuk melakukan analisis sentimen menggunakan kamus
def sentiment_analysis_lexicon_indonesia(text, lexicon_positive, lexicon_negative):
    words = text.split()
    score = 0
    for word in words:
        if word in lexicon_positive:
            score += lexicon_positive[word]
        if word in lexicon_negative:
            score += lexicon_negative[word]
    polarity = ''
    if score > 0:
        polarity = 'positif'
    elif score == 0:
        polarity = 'netral'
    elif score < 0:
        polarity = 'negatif'
    return score, polarity

def main():
    st.markdown('<p style="font-family: Times New Roman; font-size: 32px; font-weight: bold;">Analisis Sentimen Menggunakan InSet</p>', unsafe_allow_html=True)
    # Meminta file positive.csv dari pengguna
    positive_file = st.file_uploader("Upload file positive.csv", type="csv")
    if positive_file is not None:
        lexicon_positive = load_lexicon(positive_file.name)

        # Meminta file negative.csv dari pengguna
        negative_file = st.file_uploader("Upload file negative.csv", type="csv")
        if negative_file is not None:
            lexicon_negative = load_lexicon(negative_file.name)

            # Meminta file CSV yang akan dianalisis dari pengguna
            uploaded_file = st.file_uploader("Upload file CSV untuk analisis sentimen", type="csv")
            if uploaded_file is not None:
                # Membaca file CSV menjadi DataFrame
                df_tweet = pd.read_csv(uploaded_file)

                # Mengecek apakah kolom 'tweet_clean' ada di dalam DataFrame
                if 'tweet_clean' in df_tweet.columns:
                    # Mengaplikasikan analisis sentimen pada kolom 'tweet_clean'
                    results = df_tweet['tweet_clean'].apply(lambda x: sentiment_analysis_lexicon_indonesia(x, lexicon_positive, lexicon_negative))
                    results = list(zip(*results))
                    df_tweet['polarity_score'] = results[0]
                    df_tweet['polarity'] = results[1]

                    # Menampilkan hasil analisis sentimen
                    st.write(df_tweet['polarity'].value_counts())

                    # Menampilkan 5 sampel dari setiap label beserta nilai polaritasnya
                    st.subheader("Sampel Label Negatif:")
                    negative_samples = df_tweet[df_tweet['polarity'] == 'negatif'].sample(5)
                    negative_samples['polarity_score'] = negative_samples['polarity_score'].apply(lambda x: f"{x:.2f}")
                    st.write(negative_samples[['tweet_clean', 'polarity_score']])

                    st.subheader("Sampel Label Positif:")
                    positive_samples = df_tweet[df_tweet['polarity'] == 'positif'].sample(5)
                    positive_samples['polarity_score'] = positive_samples['polarity_score'].apply(lambda x: f"{x:.2f}")
                    st.write(positive_samples[['tweet_clean', 'polarity_score']])

                    st.subheader("Sampel Label Netral:")
                    neutral_samples = df_tweet[df_tweet['polarity'] == 'netral'].sample(5)
                    neutral_samples['polarity_score'] = neutral_samples['polarity_score'].apply(lambda x: f"{x:.2f}")
                    st.write(neutral_samples[['tweet_clean', 'polarity_score']])

                    # Export ke CSV
                    if st.button("Export ke CSV"):
                        df_tweet.to_csv("hasil_analisis_sentimen.csv", index=False)
                        st.success("File CSV berhasil dieksport.")

                    # Export ke XLSX
                    if st.button("Export ke XLSX"):
                        df_tweet.to_excel("hasil_analisis_sentimen.xlsx", index=False)
                        st.success("File XLSX berhasil dieksport.")
                else:
                    # Mengaplikasikan analisis sentimen pada kolom 'text_clean'
                    results = df_tweet['text_clean'].apply(lambda x: sentiment_analysis_lexicon_indonesia(x, lexicon_positive, lexicon_negative))
                    results = list(zip(*results))
                    df_tweet['polarity_score'] = results[0]
                    df_tweet['polarity'] = results[1]

                    # Menampilkan hasil analisis sentimen
                    st.write(df_tweet['polarity'].value_counts())

                    # Menampilkan 5 sampel dari setiap label beserta nilai polaritasnya
                    st.subheader("Sampel Label Negatif:")
                    negative_samples = df_tweet[df_tweet['polarity'] == 'negatif'].sample(5)
                    negative_samples['polarity_score'] = negative_samples['polarity_score'].apply(lambda x: f"{x:.2f}")
                    st.write(negative_samples[['text_clean', 'polarity_score']])

                    st.subheader("Sampel Label Positif:")
                    positive_samples = df_tweet[df_tweet['polarity'] == 'positif'].sample(5)
                    positive_samples['polarity_score'] = positive_samples['polarity_score'].apply(lambda x: f"{x:.2f}")
                    st.write(positive_samples[['text_clean', 'polarity_score']])

                    st.subheader("Sampel Label Netral:")
                    neutral_samples = df_tweet[df_tweet['polarity'] == 'netral'].sample(5)
                    neutral_samples['polarity_score'] = neutral_samples['polarity_score'].apply(lambda x: f"{x:.2f}")
                    st.write(neutral_samples[['text_clean', 'polarity_score']])

                    # Export ke CSV
                    if st.button("Export ke CSV"):
                        df_tweet.to_csv("hasil_analisis_sentimen.csv", index=False)
                        st.success("File CSV berhasil dieksport.")

                    # Export ke XLSX
                    if st.button("Export ke XLSX"):
                        df_tweet.to_excel("hasil_analisis_sentimen.xlsx", index=False)
                        st.success("File XLSX berhasil dieksport.")

if __name__ == "__main__":
    main()





