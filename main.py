import streamlit as st
import pandas as pd

# Başlık
st.title("Uygulama ID'lerine Göre Rank Edilmiş Anahtar Kelimeler")

# CSV dosyalarını yükleme
uploaded_files = st.file_uploader("CSV dosyalarınızı yükleyin", type=["csv"], accept_multiple_files=True)

if uploaded_files:
    # Dosyaları oku ve birleştir
    df_list = [pd.read_csv(file) for file in uploaded_files]
    df = pd.concat(df_list, ignore_index=True)  # Tüm dosyaları birleştir
    df = df.drop_duplicates()  # Tekrar eden satırları kaldır
    
    # Rank ve Volume değerlerini string yaparak birleştirmeye uygun hale getirme
    df["Rank"] = df["Rank"].astype(str)
    df["Volume"] = df["Volume"].astype(str)
    
    # Rank ve Volume'ü birleştirme
    df["Rank_Volume"] = df["Rank"] + " (" + df["Volume"] + ")"
    
    # Veriyi uygun formata dönüştürme (Keyword'ler satır, Application Id'ler sütun, Rank_Volume değerleri hücrede)
    pivot_df = df.pivot_table(index="Keyword", columns="Application Id", values="Rank_Volume", aggfunc=lambda x: ', '.join(x))
    
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
