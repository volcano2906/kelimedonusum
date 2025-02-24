import streamlit as st
import pandas as pd

# Sayfa ayarlarını tam ekran yap
st.set_page_config(layout="wide")

# Başlık
st.title("Uygulama ID'lerine Göre Rank Edilmiş Anahtar Kelimeler ve Puanlama")

# CSV dosyasını yükleme
uploaded_file = st.file_uploader("CSV dosyanızı yükleyin", type=["csv"])

def update_rank(rank):
    try:
        rank = float(rank)
    except:
        rank = 250.0
    if 1 <= rank <= 10:
        return 5
    elif 11 <= rank <= 30:
        return 4
    elif 31 <= rank <= 50:
        return 3
    elif 51 <= rank <= 249:
        return 2
    else:
        return 1

if uploaded_file is not None:
    # Dosyayı oku
    df = pd.read_csv(uploaded_file)
    
    # Rank değerlerini sayıya çevir ve puan hesapla
    df["Rank"] = df["Rank"].astype(str)  # Rank sütunu string olmalı
    df["Score"] = df["Rank"].apply(update_rank)
    
    # Veriyi uygun formata dönüştürme (Keyword'ler satır, Application Id'ler sütun, Rank değerleri hücrede)
    pivot_df = df.pivot_table(index=["Keyword", "Volume"], columns="Application Id", values="Rank", aggfunc=lambda x: ', '.join(map(str, x))).reset_index()
    
    # Puanları toplama
    score_pivot = df.groupby("Keyword")["Score"].sum().reset_index()
    
    # Null olmayan Rank değerlerini sayma
    rank_count = df.groupby("Keyword")["Rank"].count().reset_index()
    rank_count.rename(columns={"Rank": "Rank Count"}, inplace=True)
    
    # Puanları ve Rank sayısını tabloya ekleme
    pivot_df = pivot_df.merge(score_pivot, on="Keyword", how="left")
    pivot_df = pivot_df.merge(rank_count, on="Keyword", how="left")
    
    # Sütun adlarını güncelle
    pivot_df.columns = ["Keyword", "Volume"] + [f"app{i+1}" for i in range(len(pivot_df.columns) - 4)] + ["Total Score", "Rank Count"]
    
    # Boş değerleri null olarak değiştir
    pivot_df = pivot_df.fillna("null")
    
    # Sonuçları gösterme
    st.write("### Dönüştürülmüş Veri Tablosu ve Puanlar")
    st.dataframe(pivot_df, use_container_width=True)
    
    # CSV olarak indirme butonu
    csv = pivot_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Dönüştürülmüş CSV'yi İndir",
        data=csv,
        file_name="converted_keywords_with_scores.csv",
        mime="text/csv"
    )
