import pickle
import requests
import pandas as pd
import streamlit as st
from io import BytesIO
import ml
import os
from datetime import datetime

# Fungsi untuk mengunduh dan memuat pickle dari Dropbox
def load_pickle_from_dropbox(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pickle.load(BytesIO(response.content))
    else:
        st.error(f"Error: {response.status_code}")
        return None


def prediksi():
    st.title('AI-Powered Diabetes Prediction')
    st.info("Prediction Tools ini digunakan untuk menguji variabel kesehatan pasien untuk mengetahui estimasi potensi diabetes.")
    st.warning("Copyrights by @Ferdy 2025")

    tab1, tab2, tab3 = st.tabs(['Input Data', 'Raw Data Pasien', 'Mini Analytics'])

    # ================================
    # SESSION STATE + CSV PERSISTENCE
    # ================================
    if os.path.exists("data_pasien.csv"):
        st.session_state.data_pasien = pd.read_csv("data_pasien.csv").to_dict(orient="records")
    else:
        st.session_state.data_pasien = []

    if "data_pasien_list" not in st.session_state:
        st.session_state.data_pasien_list = []

    # ================================
    # TAB 1 - INPUT PASIEN
    # ================================
    with tab1:

        st.warning("Masukkan data pasien untuk memprediksi potensi diabetes!")

        # -------------------------------
        # CSS BOX 1
        # -------------------------------

        st.markdown(f"""
            <style>
            .hover-box3 {{
                border: 1px solid #255736;
                border-radius: 10px;
                padding: 5px;
                text-align: center;
                background-color: #255736;
                color: white;
                font-size: 18px;
                margin-top: 1px;
            }}
            .download-btn {{
                display: none;
                margin-top: 10px;
            }}
            .hover-box3:hover .download-btn {{
                display: block;
            }}
            .hover-box3:hover {{
                background-color: #255736;
                transform: scale(1.01);
            }}
            </style>
            <div class="hover-box3"><strong>DATA GEOGRAFIS PASIEN</strong></div>
        """, unsafe_allow_html=True)

        # -------------------------------
        # INPUT BOX 1
        # -------------------------------
        with st.container(border=True):
            # Load CSV wilayah Indonesia
            df = pd.read_csv("regions.csv")  # ganti sesuai path

            col1, col2 = st.columns([1, 2])
            with col1:
                Nama = st.text_input("Nama Pasien:", key="nama")
                Alamat = st.text_input("Alamat Pasien:", key="alamat")
                
                # Pilih Provinsi
                provinsi_list = sorted(df['province'].unique())
                Provinsi = st.selectbox("Pilih Provinsi", provinsi_list,key="provinsi")
                
                # Selectbox Kecamatan nantinya berdasarkan Kota & Provinsi 
                # Tapi harus pilih Provinsi & Kota dulu, jadi kita letakkan Provinsi & Kota di col2
                # Untuk sekarang kita buat placeholder
                Kecamatan = st.empty()
                
            with col2:

                
                # Filter Kota sesuai Provinsi
                df_prov = df[df['province'] == Provinsi]
                kota_list = sorted(df_prov['district'].unique())
                Kota = st.selectbox("Pilih Kota/Kabupaten", kota_list, key="kota")
                
                # Filter Kecamatan sesuai Kota
                df_kota = df_prov[df_prov['district'] == Kota]
                kec_list = sorted(df_kota['subdistrict'].unique())
                kecamatan_selected = st.selectbox("Pilih Kecamatan", kec_list, key="kecamatan")

                
                # Filter Kelurahan sesuai Kecamatan
                df_kec = df_kota[df_kota['subdistrict'] == kecamatan_selected]
                kel_list = sorted(df_kec['area'].unique())
                Kelurahan = st.selectbox("Pilih Kelurahan", kel_list, key="kelurahan")

        st.markdown(f"""
            <style>
            .hover-box {{
                border: 1px solid #0F4D0F;
                border-radius: 10px;
                padding: 5px;
                text-align: center;
                background-color: #0F4D0F;
                color: white;
                font-size: 18px;
                margin-top: 1px;
            }}
            .download-btn {{
                display: none;
                margin-top: 10px;
            }}
            .hover-box:hover .download-btn {{
                display: block;
            }}
            .hover-box:hover {{
                background-color: #0F4D0F;
                transform: scale(1.01);
            }}
            </style>
            <div class="hover-box"><strong>DATA FISIK PASIEN</strong></div>
        """, unsafe_allow_html=True)

        # -------------------------------
        # INPUT BOX 1
        # -------------------------------
        with st.container(border=True):
            col1, col2 = st.columns([1, 2])
            with col1:
                berat = st.number_input("Berat Badan (kg)", 0.0, 300.0, 60.0)
                tinggi = st.number_input("Tinggi Badan (cm)", 0.0, 300.0, 165.0)
            with col2:
                gender = st.selectbox("Jenis Kelamin", ["Male", "Female"])
                age = st.number_input("Usia", 1, 120, 40)

        # Hitung BMI
        tinggi_m = tinggi / 100 if tinggi > 0 else 1
        bmi = berat / (tinggi_m ** 2)

        # -------------------------------
        # CSS BOX 2
        # -------------------------------
        st.markdown(f"""
            <style>
            .hover-box1 {{
                border: 1px solid #008000;
                border-radius: 10px;
                padding: 5px;
                text-align: center;
                background-color: #008000;
                color: white;
                font-size: 18px;
                margin-top: 1px;
            }}
            .download-btn {{
                display: none;
                margin-top: 10px;
            }}
            .hover-box1:hover .download-btn {{
                display: block;
            }}
            .hover-box1:hover {{
                background-color: #008000;
                transform: scale(1.01);
            }}
            </style>
            <div class="hover-box1"><strong>DATA KONDISI KESEHATAN PASIEN</strong></div>
        """, unsafe_allow_html=True)

        # -------------------------------
        # INPUT BOX 2
        # -------------------------------
        with st.container(border=True):
            col1, col2 = st.columns([1, 2])
            with col1:
                hba1c = st.number_input("HbA1c Level (dalam %)", 3.0, 100.0, 6.0)
                glucose = st.number_input("Blood Glucose Level", 40, 500, 120)
                heart_text = st.selectbox("Riwayat Penyakit Jantung ?", ["No", "Yes"])

            with col2:
                hypertension_text = st.selectbox("Riwayat Hipertensi", ["No", "Yes"])
                smoke_text = st.selectbox("Riwayat Merokok", ["never", "current", "former", "ever", "No Info", "not current"])
        
        # ---- SIMPAN KE SESSION STATE ----
        st.session_state.gender = gender
        st.session_state.age = age
        st.session_state.hypertension = hypertension_text
        st.session_state.heart_disease = heart_text
        st.session_state.smoking_history = smoke_text
        st.session_state.bmi = bmi
        st.session_state.hba1c = hba1c
        st.session_state.glucose = glucose
        
        # -------------------------------
        # TOMBOL SIMPAN (langsung simpan)
        # -------------------------------
        col1, col2, col3 = st.columns([1,2,1])

        # Tombol Deteksi
        with col1:
            if st.button("Deteksi Data Pasien!", key='deteksi'):
                hasil, prob_yes = ml.ml(display=False)  # Hanya dipanggil sekali saat Deteksi
                st.session_state.hasil_prediksi = hasil
                st.session_state.prob_yes = prob_yes

        # Tampilkan hasil full-width
        if st.session_state.get("hasil_prediksi") is not None:
            hasil_text = "Terdeteksi Diabetes" if st.session_state.hasil_prediksi==1 else "Tidak Terdeteksi Diabetes"
            prob_percent = round(st.session_state.prob_yes*100,2)
            if st.session_state.hasil_prediksi==1 :
                st.error(f"Hasil Deteksi: {hasil_text}")
                st.info(f"Probabilitas Positif: {prob_percent} %")
            else:
                st.success(f"Hasil Deteksi: {hasil_text}")
                st.info(f"Probabilitas Positif: {prob_percent} %")          

        # Tentukan rekomendasi berdasarkan hasil dan probabilitas
            st.markdown(f"""
                        <style>
                        .hover-box {{
                            border: 1px solid #0F4D0F;
                            border-radius: 10px;
                            padding: 5px;
                            text-align: center;
                            background-color: #0F4D0F;
                            color: white;
                            font-size: 18px;
                            margin-top: 1px;
                        }}
                        .download-btn {{
                            display: none;
                            margin-top: 10px;
                        }}
                        .hover-box:hover .download-btn {{
                            display: block;
                        }}
                        .hover-box:hover {{
                            background-color: #0F4D0F;
                            transform: scale(1.01);
                        }}
                        </style>
                        <div class="hover-box"><strong>REKOMENDASI </strong></div>
                        </p>
                    """, unsafe_allow_html=True)
            
            if st.session_state.hasil_prediksi == 1:  # Positif diabetes
                if prob_percent > 70:
                    rekomendasi = f"""
                    <div style="background-color:#ffcccc; padding:10px; border-radius:10px;">

                    <b>🔴 Tindakan Darurat & Medis:</b><br>
                    - Segera konsultasi dokter atau endokrinologis.<br>
                    - Pantau gula darah 4-6x/hari sesuai anjuran dokter.<br>
                    - Jika perlu, penggunaan insulin atau obat oral sesuai resep.<br><br>

                    <b>🥗 Pola Makan:</b><br>
                    - Hindari gula dan karbohidrat olahan.<br>
                    - Tingkatkan konsumsi sayur, protein rendah lemak, biji-bijian.<br>
                    - Batasi makanan tinggi lemak jenuh dan garam.<br><br>

                    <b>🏃‍♂️ Aktivitas Fisik:</b><br>
                    - Jalan kaki 30–60 menit/hari atau olahraga ringan–sedang.<br><br>

                    <b>🩺 Pemeriksaan & Pemantauan:</b><br>
                    - Cek HbA1c tiap 3 bulan.<br>
                    - Cek tekanan darah, kolesterol, fungsi ginjal rutin.<br><br>

                    <b>💡 Gaya Hidup Sehat:</b><br>
                    - Jangan merokok, hindari alkohol.<br>
                    - Tidur cukup 7–8 jam.<br>
                    - Kelola stres, meditasi atau yoga ringan.
                    </div>
                                    </p>
                    """
                elif prob_percent > 40:
                    rekomendasi = f"""
                    <div style="background-color:#ffe5b4; padding:10px; border-radius:10px;">

                    <b>🟠 Tindakan Medis:</b><br>
                    - Konsultasi dokter secara rutin.<br>
                    - Pemantauan gula darah 2–3x/hari.<br><br>

                    <b>🥗 Pola Makan:</b><br>
                    - Kurangi gula, makanan cepat saji.<br>
                    - Tingkatkan sayur, protein, dan biji-bijian.<br><br>

                    <b>🏃‍♂️ Aktivitas Fisik:</b><br>
                    - Jalan cepat, senam ringan, yoga 30–60 menit/hari.<br><br>

                    <b>🩺 Pemeriksaan:</b><br>
                    - Cek HbA1c tiap 3–6 bulan.<br>
                    - Monitor tekanan darah dan berat badan.<br><br>

                    <b>💡 Gaya Hidup:</b><br>
                    - Jangan merokok, kurangi stres, tidur cukup.
                    </div>
                                    </p>
                    """
                else:
                    rekomendasi = f"""
                    <div style="background-color:#ccffcc; padding:10px; border-radius:10px;">

                    <b>🟢 Pemantauan:</b><br>
                    - Monitor gula darah secara rutin.<br>
                    - Periksa ulang secara berkala ke dokter.<br><br>

                    <b>🥗 Pola Makan & Hidup:</b><br>
                    - Tetap jaga pola makan sehat.<br>
                    - Olahraga ringan minimal 30 menit/hari.<br>
                    - Tidur cukup, hindari stres berlebihan.
                    </div>
                                    </p>
                    """
            else:  # Negatif diabetes
                if prob_percent > 70:
                    rekomendasi = f"""
                    <div style="background-color:#ffe5b4; padding:10px; border-radius:10px;">

                    <b>🟠 Meski Negatif, Probabilitas Tinggi:</b><br>
                    - Tetap waspada, periksa gula darah tiap beberapa bulan.<br>
                    - Jaga pola makan rendah gula dan karbohidrat olahan.<br>
                    - Olahraga rutin minimal 150 menit/minggu.<br>
                    - Periksa tekanan darah dan kolesterol secara berkala.
                    </div>
                                    </p>
                    """
                elif prob_percent > 40:
                    rekomendasi = f"""
                    <div style="background-color:#ffffb3; padding:10px; border-radius:10px;">

                    <b>🟡 Probabilitas Sedang:</b><br>
                    - Monitor gula darah dan HbA1c tiap 6–12 bulan.<br>
                    - Tetap jaga diet sehat dan olahraga rutin.
                    </div>
                                    </p>
                    """
                else:
                    rekomendasi = f"""
                    <div style="background-color:#ccffcc; padding:10px; border-radius:10px;">

                    <b>🟢 Probabilitas Rendah:</b><br>
                    - Pertahankan gaya hidup sehat: diet seimbang, olahraga rutin, tidur cukup.<br>
                    - Cek kesehatan rutin minimal setahun sekali.
                    </div>
                    </p>
                    """

            # Tampilkan di Streamlit
            if st.button("🔍 Tampilkan Rekomendasi AI"):
                st.markdown(rekomendasi, unsafe_allow_html=True)

        # Tombol Simpan
        with col3:
            if st.button("Simpan Data Pasien"):
                hasil_text = "Terdeteksi Diabetes" if st.session_state.get("hasil_prediksi",0)==1 else "Tidak Terdeteksi Diabetes"
                prob_yes = st.session_state.get("prob_yes", None)
                prob_percent = round(prob_yes*100,2) if prob_yes is not None else None
                data = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Nama" : Nama,
                    "Alamat" : Alamat,
                    "Provinsi" : Provinsi,
                    "Kota/Kabupaten" : Kota,
                    "Kecamatan" : kecamatan_selected,
                    "Kelurahan" : Kelurahan,
                    "Berat (kg)": berat,
                    "Tinggi (cm)": tinggi,
                    "Gender": gender,
                    "Usia": age,
                    "BMI": round(bmi,2),
                    "HbA1c": hba1c,
                    "Glukosa": glucose,
                    "Heart Disease": heart_text,
                    "Hipertensi": hypertension_text,
                    "Smoking": smoke_text,
                    "Hasil Deteksi": hasil_text,
                    "Probabilitas Positif (%)": f"{prob_percent} %"
                }
                if "data_pasien" not in st.session_state:
                    st.session_state.data_pasien = []          # full history
                if "data_pasien_list" not in st.session_state:
                    st.session_state.data_pasien_list = []     # pasien terbaru

                # Simpan full history
                st.session_state.data_pasien.append(data)
                pd.DataFrame(st.session_state.data_pasien).to_csv("data_pasien.csv", index=False)

                # Simpan hanya data terbaru (1 baris)
                st.session_state.data_pasien_list = [data]


                        
        if st.session_state.data_pasien_list:
            st.success("Data pasien berhasil disimpan!")
            st.markdown(f"""
                        <style>
                        .hover-box1 {{
                            border: 1px solid #008000;
                            border-radius: 10px;
                            padding: 5px;
                            text-align: center;
                            background-color: #008000;
                            color: white;
                            font-size: 18px;
                            margin-top: 1px;
                        }}
                        .download-btn {{
                            display: none;
                            margin-top: 10px;
                        }}
                        .hover-box1:hover .download-btn {{
                            display: block;
                        }}
                        .hover-box1:hover {{
                            background-color: #008000;
                            transform: scale(1.01);
                        }}
                        </style>
                        <div class="hover-box1"><strong>DATA HASIL INPUTAN</strong></div>
                        </p>
                    """, unsafe_allow_html=True)
            # Tampilkan pasien terbaru
            st.dataframe(pd.DataFrame(st.session_state.data_pasien_list))




        



    # ================================
    # TAB 2 — DataFrame Data Tersimpan
    # ================================
    with tab2:
        st.markdown(f"""
            <style>
            .hover-box {{
                border: 1px solid #0F4D0F;
                border-radius: 10px;
                padding: 5px;
                text-align: center;
                background-color: #0F4D0F;
                color: white;
                font-size: 18px;
                margin-top: 1px;
            }}
            .download-btn {{
                display: none;
                margin-top: 10px;
            }}
            .hover-box:hover .download-btn {{
                display: block;
            }}
            .hover-box:hover {{
                background-color: #0F4D0F;
                transform: scale(1.01);
            }}
            </style>
            <div class="hover-box"><strong>DATA TABEL SEMUA PASIEN</strong></div>
                    </p>
        """, unsafe_allow_html=True)

        if len(st.session_state.data_pasien) > 0:
            df_pasien = pd.DataFrame(st.session_state.data_pasien)
            df_pasien["Hapus"] = False

            st.info("Edit data langsung di tabel, lalu klik **Simpan Perubahan**.")

            edited_df = st.data_editor(
                df_pasien,
                use_container_width=True,
                num_rows="dynamic",
                hide_index=True
            )

            colA, colB, colC = st.columns(3)

            # Simpan perubahan edit
            with colA:
                if st.button("💾 Simpan Perubahan"):
                    cleaned = edited_df.drop(columns=["Hapus"])
                    st.session_state.data_pasien = cleaned.to_dict(orient="records")
                    cleaned.to_csv("data_pasien.csv", index=False)
                    st.success("Perubahan berhasil disimpan!")
                    st.rerun()

            # Hapus baris
            with colB:
                if st.button("🗑️ Hapus Baris Terpilih"):
                    filtered = edited_df[edited_df["Hapus"]==False].drop(columns=["Hapus"])
                    st.session_state.data_pasien = filtered.to_dict(orient="records")
                    filtered.to_csv("data_pasien.csv", index=False)
                    st.success("Baris yang dipilih berhasil dihapus!")
                    st.rerun()

            # Download CSV
            with colC:
                csv = edited_df.drop(columns=["Hapus"]).to_csv(index=False).encode("utf-8")
                st.download_button("⬇️ Download Data (CSV)", data=csv, file_name="data_pasien.csv", mime="text/csv")
        else:
            st.info("Belum ada data pasien yang disimpan.")

    with tab3:
        import minianalis
        minianalis.minianalis()

if __name__ == "__main__":
    prediksi()
