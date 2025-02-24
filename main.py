import streamlit as st
import pandas as pd

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
    df["Score"] = df["Rank"].apply(update_rank)
    
    # Veriyi uygun formata dönüştürme (Keyword'ler satır, Application Id'ler sütun, Rank değerleri hücrede)
    pivot_df = df.pivot_table(index=["Keyword", "Volume"], columns="Application Id", values="Rank", aggfunc=lambda x: ', '.join(x)).reset_index()
    
    # Puanları toplama
    score_pivot = df.groupby("Keyword")["Score"].sum().reset_index()
    pivot_df = pivot_df.merge(score_pivot, on="Keyword", how="left")
    
    # Sütun adlarını güncelle
    pivot_df.columns = ["Keyword", "Volume"] + [f"app{i+1}" for i in range(len(pivot_df.columns) - 3)] + ["Total Score"]
    
    # Boş değerleri null olarak değiştir
    pivot_df = pivot_df.fillna("null")
    
    # Sonuçları gösterme
    st.write("### Dönüştürülmüş Veri Tablosu ve Puanlar")
    st.dataframe(pivot_df)
    
    # CSV olarak indirme butonu
    csv = pivot_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Dönüştürülmüş CSV'yi İndir",
        data=csv,
        file_name="converted_keywords_with_scores.csv",
        mime="text/csv"
    )
