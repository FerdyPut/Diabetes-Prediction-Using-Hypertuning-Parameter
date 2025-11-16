import pickle
import requests
import pandas as pd
import streamlit as st
from io import BytesIO

# Fungsi untuk mengunduh dan memuat pickle dari Dropbox
def load_pickle_from_dropbox(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pickle.load(BytesIO(response.content))  # Memuat pickle dari response content
    else:
        st.error(f"Error: {response.status_code}")
        return None




def prediksi():
    st.title('Diabetes Prediction')
    st.info("Prediction Tools ini digunakan untuk menguji dari variabel-variabel yang ada berkaitan dengan faktor pengantaran makanan nantinya didapatkan berapa perkiraan estimasi waktu pengantarannya. Hal ini, berguna untuk meminimalisisr resiko pengantaran.")

    # Input variabel dari pengguna
    st.warning("Masukkan data pasien untuk memprediksi potensi diabetes!")


    # ---- CSS Box ----
    st.markdown("""
        <style>
        .box {
            padding: 20px;
            border-radius: 15px;
            background-color: #f5f5f5;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    # ---- UI Box ----
    with st.container():
        st.markdown("<div class='box'>", unsafe_allow_html=True)
        
        berat = st.number_input("Berat Badan (kg)", 1.0, 300.0, 60.0)
        tinggi = st.number_input("Tinggi Badan (cm)", 50.0, 250.0, 165.0)
        gender_text = st.selectbox("Jenis Kelamin", ["Female", "Male"])

        st.markdown("</div>", unsafe_allow_html=True)

    # Konversi tinggi ke meter
    tinggi_m = tinggi / 100

    # Hitung BMI
    bmi = berat / (tinggi_m ** 2)

    hba1c = st.number_input("HbA1c Level", 3.0, 20.0, 6.0)
    glucose = st.number_input("Blood Glucose Level", 40, 500, 120)
    age = st.number_input("Usia", 1, 120, 40)
    heart_text = st.selectbox("Riwayat Penyakit Jantung ?", ["No", "Yes"])
    hypertension_text = st.selectbox("Riwayat Hipertensi", ["No", "Yes"])
    smoke_text = st.selectbox("Riwayat Merokok", ["never", "current", "former", "ever", "No Info", "not current"])


