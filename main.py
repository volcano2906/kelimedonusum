import streamlit as st
import pandas as pd

# Başlık
st.title("Uygulama ID'lerine Göre Rank Edilmiş Anahtar Kelimeler")

# CSV dosyasını yükleme
uploaded_file = st.file_uploader("CSV dosyanızı yükleyin", type=["csv"])

if uploaded_file is not None:
    # Dosyayı oku
    df = pd.read_csv(uploaded_file)
    
    # Veriyi uygun formata dönüştürme (Keyword'ler satır, Application Id'ler sütun, Rank değerleri hücrede)
    df["Rank"] = df["Rank"].astype(str)  # Rank değerlerini string yaparak birleştirmeye uygun hale getirme
    pivot_df = df.pivot_table(index="Keyword", columns="Application Id", values="Rank", aggfunc=lambda x: ', '.join(x))
    
    # Sonuçları gösterme
    st.write("### Dönüştürülmüş Veri Tablosu")
    st.dataframe(pivot_df)
    
    # CSV olarak indirme butonu
    csv = pivot_df.to_csv().encode('utf-8')
    st.download_button(
        label="Dönüştürülmüş CSV'yi İndir",
        data=csv,
        file_name="converted_keywords.csv",
        mime="text/csv"
    )
