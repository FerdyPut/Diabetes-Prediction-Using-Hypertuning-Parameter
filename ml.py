import streamlit as st
import pandas as pd
import numpy as np
from joblib import load

# --- Fungsi load joblib ---
def load_joblib_local(path):
    try:
        obj = load(path)
        return obj
    except FileNotFoundError:
        st.error(f"File tidak ditemukan: {path}")
        return None
    except Exception as e:
        st.error(f"Gagal load file {path}: {e}")
        return None

# --- Fungsi utama ml debug ---
def ml(display=True):
    # Load model, scaler, encoder
    model = load_joblib_local("rf_gridsearch_non_smote.joblib")
    scaler = load_joblib_local("scaler.joblib")
    encoding = load_joblib_local("model_diabetes_encoding.joblib")
    if not model or not scaler or not encoding:
        st.error("Gagal load salah satu dari model/scaler/encoder.")
        return

    # Ambil input user
    input_df = pd.DataFrame([{
        'gender': st.session_state.gender,
        'hypertension': st.session_state.hypertension,
        'heart_disease': st.session_state.heart_disease,
        'age': st.session_state.age,
        'bmi': st.session_state.bmi,
        'HbA1c_level': st.session_state.hba1c,
        'blood_glucose_level': st.session_state.glucose,
        'smoking_history': st.session_state.smoking_history
    }])

    # Encode gender
    input_df['gender'] = encoding['le_gender'].transform(input_df['gender'])

    # Encode smoking history
    smoke_input = input_df[['smoking_history']].values
    smoke_encoded = encoding['ohe_smoke'].transform(smoke_input)
    smoke_df = pd.DataFrame(smoke_encoded, columns=list(encoding['ohe_cols']))
    input_df = pd.concat([input_df.drop(columns=['smoking_history']), smoke_df], axis=1)

    # Encode hypertension & heart_disease
    yesno = {'No': 0, 'Yes': 1}
    input_df['hypertension'] = input_df['hypertension'].map(yesno)
    input_df['heart_disease'] = input_df['heart_disease'].map(yesno)

    # # Scaling numeric khusus yg jarak 
    # numerik_cols = ['age','bmi','HbA1c_level','blood_glucose_level']
    # input_df[numerik_cols] = scaler.transform(input_df[numerik_cols])

    # Pastikan urutan kolom sesuai training
    model_cols = ['gender','age','hypertension','heart_disease','bmi','HbA1c_level','blood_glucose_level'] + list(encoding['ohe_cols'])
    input_df = input_df[model_cols]

    # --- DEBUG: tampilkan input akhir ke model ---

    # Prediksi
    try:
        hasil_prediksi = model.predict(input_df)
        y_prob = model.predict_proba(input_df)[0]
        if display:
            if hasil_prediksi[0] == 1:  # Terdeteksi diabetes
                st.warning(f"Hasil prediksi: Terdeteksi Diabetes")
            else:  # Tidak terdeteksi
                st.success(f"Hasil prediksi: Tidak Terdeteksi Diabetes")
            
            st.info(f"Probabilitas Negatif: {y_prob[0]*100:.2f}% | Probabilitas Positif: {y_prob[1]*100:.2f}%")



        return hasil_prediksi, y_prob[1]  # <-- return hasil + prob
    
    except Exception as e:
        st.error(f"Gagal prediksi: {e}")
