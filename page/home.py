import streamlit as st
    
def main():
    st.markdown('<p style="font-family: Times New Roman; font-size: 32px; font-weight: bold;">Pendeteksi Kata Tidak Baku</p>', unsafe_allow_html=True)

    # Menambahkan penjelasan mengenai aplikasi
    st.markdown("""
    
Aplikasi ini adalah program Python yang menggunakan library Streamlit, Pandas, NLTK, dan beberapa library lainnya. Aplikasi ini digunakan untuk melakukan preprocessing pada teks dan mendeteksi kata-kata tidak baku. Beberapa fitur yang tersedia di aplikasi ini antara lain:

    a. Pada antarmuka aplikasi, upload file kamus KBBI Anda dalam format CSV, TXT, XLS, atau XLSX dengan menggunakan widget unggah file yang tersedia.
    b. Sistem akan memuat dan membaca file kamus KBBI yang Anda unggah.
    c. Setelah mengunggah file kamus KBBI, unggah file data yang ingin Anda proses dalam format CSV.
    d. Sistem akan menampilkan kolom yang tersedia dalam file data Anda.
    e. Pilih kolom yang berisi teks yang akan diproses dari dropdown yang tersedia.
    f. Sistem akan melakukan preprocessing pada teks, termasuk penghapusan URL, mention, dan hashtag, serta tanda baca dan karakter non-ASCII.
    g. Sistem akan menampilkan hasil preprocessing dalam bentuk tabel.
    h. Sistem akan mencari kata-kata tidak baku dalam teks berdasarkan kamus KBBI yang telah diunggah.
    i. Kata-kata tidak baku akan ditampilkan dalam tabel hasil preprocessing.
    j. Sistem akan menghapus kata-kata yang memiliki imbuhan dalam teks, memastikan hanya kata-kata tidak baku yang bersih yang ditampilkan.
    k. Setelah proses selesai, Anda dapat mengunduh kata-kata slang yang telah ditemukan dalam bentuk file teks (TXT) atau file CSV.

    """)
    
    st.markdown('<p style="font-family: Times New Roman; font-size: 32px; font-weight: bold;">Analisis Sentimen InSet</p>', unsafe_allow_html=True)

    # Menambahkan penjelasan mengenai aplikasi
    st.markdown("""
Aplikasi ini adalah program Python yang menggunakan library Streamlit, Pandas, NLTK, dan beberapa library lainnya. Aplikasi ini digunakan untuk melakukan analisis sentimen menggunakan InSet. Beberapa fitur yang tersedia di aplikasi ini antara lain:
                
    a. Gunakan pemilih file yang diberi label "Upload file data yang akan diproses" untuk mengunggah file CSV yang berisi data teks yang ingin dianalisis.
    b. File harus dalam format CSV dan mengandung setidaknya satu kolom dengan data teks.
    c. Setelah mengunggah file CSV, Anda akan melihat daftar kolom yang tersedia di data.
    d. Pilih Kolom: Pilih kolom dari menu dropdown yang berisi data teks yang ingin dianalisis.
    e. Aplikasi akan secara otomatis memproses teks di kolom yang dipilih, termasuk melakukan preprocessing pada text.
    f. Unggah File TXT: Gunakan pemilih file yang diberi label "Upload bahan normalisasi TXT" untuk mengunggah file TXT yang berisi kamus untuk normalisasi istilah gaul.
    g. File TXT harus diformat sebagai kamus di mana kunci adalah istilah gaul dan nilai adalah pengganti standarnya.
    h. Kotak Centang: Centang kotak yang diberi label "Gunakan stopwords tambahan" jika Anda ingin menggunakan stopwords tambahan selain yang sudah ada.
    i. Unggah Stopwords: Jika Anda mencentang kotak, unggah file TXT dengan stopwords tambahan.
    j. Unggah Leksikon Positif: Gunakan pemilih file yang diberi label "Upload lexicon positif.CSV" untuk mengunggah file CSV yang berisi kata-kata sentimen positif dan skor mereka.
    k. Unggah Leksikon Negatif: Gunakan pemilih file yang diberi label "Upload lexicon negatif.CSV" untuk mengunggah file CSV yang berisi kata-kata sentimen negatif dan skor mereka.
    l. Kedua file CSV harus memiliki dua kolom: kolom pertama dengan kata-kata dan kolom kedua dengan skor sentimen mereka.
    m. Aplikasi akan memproses data teks menggunakan leksikon yang diunggah dan menampilkan:
    n. Hasil Analisis Sentimen: Menampilkan polaritas sentimen (positif, negatif, netral) dan skor untuk setiap teks.
    o. Data dengan Kata Positif dan Negatif: Menampilkan daftar kata positif dan negatif yang ditemukan dalam teks.
    p. Klik tombol "Download hasil CSV" untuk mengunduh data yang telah dianalisis dalam format CSV.
    """)

    st.markdown('<p style="font-family: Times New Roman; font-size: 32px; font-weight: bold;">Confusion Matrix InSet</p>', unsafe_allow_html=True)

    # Menambahkan penjelasan mengenai aplikasi
    st.markdown("""
Aplikasi ini adalah program Python yang menggunakan library Streamlit dan Pandas untuk melakukan evaluasi matrix InSet pada data hasil analisis sentimen:

    a. Di aplikasi, cari pemilih file yang diberi label "Upload file asli".
    b. Pilih file CSV atau Excel yang berisi data asli dengan kolom label yang menunjukkan kategori sentimen (positif, negatif, netral).
    c. Gunakan pemilih file yang diberi label "Upload file hasil analisis".
    d. Pilih file CSV atau Excel yang berisi hasil analisis sentimen dengan kolom polarity yang menunjukkan polaritas sentimen hasil analisis.
    e. Aplikasi akan memeriksa dan memetakan nilai pada kolom label dari data asli dan kolom polarity dari hasil analisis ke dalam format yang konsisten.
    f. Data yang tidak sesuai format akan diubah menjadi 'unknown'.
    g. Aplikasi akan menampilkan DataFrame asli dan DataFrame hasil analisis setelah praproses.
    h. Aplikasi akan menampilkan diagram lingkaran yang menunjukkan distribusi sentimen dalam data asli.
    i. Jumlah data per kategori sentimen juga akan ditampilkan.
    j. Diagram lingkaran yang menunjukkan distribusi polaritas dalam data hasil analisis juga akan ditampilkan.
    k. Jumlah data per kategori polaritas akan ditampilkan.
    l. Aplikasi akan menghitung dan menampilkan metrik evaluasi sentimen dengan pendekatan macro, termasuk Accuracy, Recall, Precision, dan F1 Score.
    m. Metrik ini juga ditampilkan dalam persentase.
    n. Aplikasi juga akan menghitung dan menampilkan metrik evaluasi sentimen dengan pendekatan weighted, termasuk Accuracy, Recall, Precision, dan F1 Score.
    o. Metrik ini juga ditampilkan dalam persentase.
    p. Aplikasi menampilkan metrik evaluasi dalam format tabel dan persentase untuk kedua pendekatan (macro dan weighted).
    """)
if __name__ == "__main__":
    main()