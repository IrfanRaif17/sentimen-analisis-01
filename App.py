import streamlit as st

# Set the page configuration at the top of the script
st.set_page_config(page_title="Analisis Sentimen App", page_icon="icon/simple.png")

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, recall_score, f1_score, precision_score
from page.fetch import display_pie_chart

import page.home
import page.Pendeteksi   
import page.analisissentimen
import page.ConfusionMatrix

PAGES = {
    "Beranda": page.home,
    "Pendeteksi Kata Tidak Baku": page.Pendeteksi,
    "Analisis Sentimen InSet": page.analisissentimen,
    "Confusion Matrix": page.ConfusionMatrix,
}

def set_page_config():
    page_font = "Times New Roman"
    st.markdown(
        f"""
        <style>
            body {{
                font-family: "{page_font}", sans-serif;
            }}
            .reportview-container .main .block-container {{
                max-width: 1200px;
                padding-top: 5rem;
                padding-right: 5rem;
                padding-left: 5rem;
                padding-bottom: 5rem;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def main():
    set_page_config()

    st.sidebar.markdown('<p style="font-family: Times New Roman; font-size: 24px; font-weight: bold;">Pendeteksi dan Analisis Sentimen</p>', unsafe_allow_html=True)
    
    page = st.sidebar.selectbox("Pilih Menu", list(PAGES.keys()))

    with st.spinner(f"Loading {page} ..."):
        PAGES[page].main()
    
    st.sidebar.markdown('<p style="font-family: Times New Roman; font-size: 24px; font-weight: bold;">APP About</p>', unsafe_allow_html=True)
    
    st.sidebar.info(
        """
        APP ini bertujuan untuk memudahkan pengguna melakukan preprocessing dan melihat perbandingan
        antara analisis sentimen asli dan analisis sentimen yang sudah dilakukan preprocessing.
        """
    )

if __name__ == "__main__":
    main()
