import streamlit as st
    
def main():
    st.markdown('<p style="font-family: Times New Roman; font-size: 32px; font-weight: bold;">Pendeteksi Kata Slang</p>', unsafe_allow_html=True)

    # Menambahkan penjelasan mengenai aplikasi
    st.markdown("""
    
Aplikasi ini adalah program Python yang menggunakan library Streamlit, Pandas, NLTK, dan beberapa library lainnya. Aplikasi ini digunakan untuk melakukan preprocessing pada teks dan mendeteksi kata-kata tidak baku. Beberapa fitur yang tersedia di aplikasi ini antara lain:

    a. User mengunggah file kamus KBBI dalam format CSV, TXT, XLS, atau XLSX.
    b. User mengunggah file data yang akan diproses dalam format CSV.
    c. Sistem melakukan preprocessing pada teks, termasuk penghapusan URL, mention, dan hashtag, serta tanda baca dan karakter non-ASCII.
    d. Sistem mencari kata slang dalam teks berdasarkan kamus KBBI.
    e. Sistem menghapus kata-kata berimbuhan dalam teks.
    f. Sistem menampilkan hasil preprocessing dan kata-kata tidak baku.
    g. User bisa mengeskpor kata slang ke file teks (TXT) atau file CSV.


Aplikasi ini menyediakan antarmuka web sederhana menggunakan library Streamlit. Dengan menggunakan aplikasi ini, pengguna dapat melakukan pemrosesan teks dan analisis sederhana terhadap data yang diunggah.
    """)
    st.markdown('<p style="font-family: Times New Roman; font-size: 32px; font-weight: bold;">Optimalisasi Pra-proses</p>', unsafe_allow_html=True)

    # Menambahkan penjelasan mengenai aplikasi
    st.markdown("""

    """)
    st.markdown('<p style="font-family: Times New Roman; font-size: 32px; font-weight: bold;">Analisis Sentimen Menggunakan InSet</p>', unsafe_allow_html=True)

    # Menambahkan penjelasan mengenai aplikasi
    st.markdown("""

    """)
    st.markdown('<p style="font-family: Times New Roman; font-size: 32px; font-weight: bold;">Analisis Sentimen Menggunakan Vader</p>', unsafe_allow_html=True)

    # Menambahkan penjelasan mengenai aplikasi
    st.markdown("""

    """)
    st.markdown('<p style="font-family: Times New Roman; font-size: 32px; font-weight: bold;">Evaluasi Matrix</p>', unsafe_allow_html=True)

    # Menambahkan penjelasan mengenai aplikasi
    st.markdown("""
Aplikasi ini adalah program Python yang menggunakan library Streamlit dan Pandas untuk melakukan evaluasi matrix pada data hasil analisis sentimen:

    a. Mengunggah file sebelum analisis sentimen dan sesudah analisis sentimen: User dapat memilih file yang akan diunggah untuk dievaluasi matrixnya.
    b. Menampilkan data asli: Sistem menampilkan data sebelum analisis sentimen dan sesudah analisis sentimen yang sudah dimasukan.
    c. Menampilkan distribusi label pada data asli: Sistem menampilkan grafik pie yang menunjukkan distribusi label pada data sebelum analisis sentimen.
    d. Menampilkan distribusi sentimen pada data hasil analisis: Sistem menampilkan grafik pie yang menunjukkan distribusi sentimen pada data sesudah analisis sentimen.
    e. Menghitung evaluasi matrix weighted-average: Sistem menghitung dan menampilkan evaluasi matrix seperti akurasi, recall, presisi, dan F1 score untuk analisis sentimen menggunakan matrix weighted.
    f. Menampilkan evaluasi matrix weighted-average dalam persentase: Sistem menampilkan evaluasi matrix seperti akurasi, recall, presisi, dan F1 score dalam bentuk persentase.
    g. Menghitung evaluasi matrix macro-average: Sistem menghitung dan menampilkan evaluasi matrix seperti akurasi, recall, presisi, dan F1 score untuk analisis sentimen menggunakan matrix macro-averaged.
    h. Menampilkan evaluasi matrix macro-average dalam persentase: Sistem menampilkan evaluasi matrix seperti akurasi, recall, presisi, dan F1 score dalam bentuk persentase.

Pengguna dapat melakukan evaluasi matriks pada data hasil analisis sentimen dengan mudah dan memahami hasilnya melalui antarmuka web aplikasi Streamlit yang interaktif.
    """)

if __name__ == "__main__":
    main()