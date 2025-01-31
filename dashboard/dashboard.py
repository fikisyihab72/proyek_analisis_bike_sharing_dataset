import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# memuat data
df_day_path = "df_day.csv"
df_hour_path = "df_hour.csv"
df_2011_path = "df_2011_group_by_musim.csv"
df_2012_path = "df_2012_group_by_musim.csv"

df_day = pd.read_csv(df_day_path)
df_hour = pd.read_csv(df_hour_path)
df_2011_group_by_musim = pd.read_csv(df_2011_path)
df_2012_group_by_musim = pd.read_csv(df_2012_path)

st.title('Analisis Data Bike Sharing Dataset')

with st.sidebar:
    st.image("https://img.icons8.com/?size=100&id=ZEZmzxug8Bzx&format=png&color=000000")
    st.write("Filter tahun data Day.CSV")
    df_day['dteday'] = pd.to_datetime(df_day['dteday'])
    year1 = st.selectbox('Pilih Tahun untuk Day.CSV', df_day['dteday'].dt.year.unique(), key="year1_selectbox")

    st.write("Filter tahun data Hour.CSV")
    df_hour['dteday'] = pd.to_datetime(df_hour['dteday'])
    year2 = st.selectbox('Pilih Tahun untuk Hour.CSV', df_hour['dteday'].dt.year.unique(), key="year2_selectbox")

df_day_filtered = df_day[df_day['dteday'].dt.year == year1]  
df_hour_filtered = df_hour[df_hour['dteday'].dt.year == year2]  

with st.container():
    st.write("Menampilkan Data Day.CSV dalam bentuk tabel")
    
    st.dataframe(df_day_filtered, height=200)

    st.write("Menampilkan Data Hour.CSV dalam bentuk tabel")
    st.dataframe(df_hour_filtered, height=200)

st.title('Hasil Analisis Data')

col1a, col1b, col1c, col1d = st.columns(4)
with col1a:
    st.metric("Total Bike Sharing", df_day['cnt'].sum())

with col1b:
    st.metric("Musim Favorit", "Fall")

with col1c:
    st.metric("Total Pengguna Casual", df_day['casual'].sum())
    
with col1d:
    st.metric("Total Pengguna Registered", df_day['registered'].sum())

# Baris pertama dengan 3 kolom
col1, col2, col3 = st.columns(3)

with col1:
    st.write("**Jumlah peminjam sepeda 2011 setiap musim**")
    fig, ax = plt.subplots(figsize=(6,5))
    sns.barplot(
        x='label_musim',
        y='cnt',
        data=df_2011_group_by_musim,
        hue='label_musim',
        palette="coolwarm",
        ax=ax
    )
    ax.set_title("Jumlah peminjam sepeda tahun 2011 berdasarkan musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Peminjam")

    st.pyplot(fig)

with col2:
    st.write("**Jumlah peminjam sepeda 2012 setiap musim**")
    fig, ax = plt.subplots(figsize=(6, 5))  
    sns.barplot(
        x='label_musim', 
        y='cnt', 
        data=df_2012_group_by_musim, 
        hue='label_musim', 
        palette="BrBG",
        ax=ax  
    )
    ax.set_title("Jumlah peminjam sepeda tahun 2012 berdasarkan musim")
    ax.set_xlabel("Musim")
    ax.set_ylabel("Jumlah Peminjam")
    st.pyplot(fig)

with col3:
    st.write("**Distribusi peminjam sepeda casual vs registered**")
    jumlah_casual = df_day['casual'].sum()
    jumlah_registered = df_day['registered'].sum()

    labels = ['Casual', 'Registered']
    ukuran = [jumlah_casual, jumlah_registered]
    warna = ['#74ad5c', '#963965']
 
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(ukuran, labels=labels, autopct='%1.1f%%', startangle=90, colors=warna)
    ax.set_title('Pie Chart Peminjaman Sepeda: Casual vs Registered tahun 2011-2012')
    st.pyplot(fig)

st.write("**Pengaruh cuaca terahadap jumlah peminjam sepeda**")
weather_map = {
    1: 'Clear / Partly Cloudy',
    2: 'Mist / Cloudy',
    3: 'Light Snow / Rain',
    4: 'Heavy Rain / Snow'
}

# Menyederhanakan label cuaca dengan mengganti berdasarkan dictionary mapping
df_hour['weathersit_label'] = df_hour['weathersit'].map(weather_map)

fig, ax = plt.subplots(figsize=(8, 6))
sns.stripplot(x='cnt', y='weathersit_label', data=df_hour, jitter=True, hue='weathersit_label', palette="coolwarm", ax=ax)

# Menambahkan label sumbu dan judul
ax.set_xlabel('Jumlah Peminjaman Sepeda (cnt)')
ax.set_ylabel('Cuaca (weathersit)')
ax.set_title('Jumlah Peminjaman Sepeda Berdasarkan Cuaca')
st.pyplot(fig)

df_musim_group = df_day[['season', 'casual', 'registered']]

# Mengelompokkan data berdasarkan musim dan menghitung jumlah peminjam casual dan registered
df_casual_registered_group = df_musim_group.groupby('season')[['casual', 'registered']].sum().reset_index()

# Mapping season ke nama musim
season_map = {
    1: 'Springer',
    2: 'Summer',
    3: 'Fall',
    4: 'Winter'
}

df_casual_registered_group['season'] = df_casual_registered_group['season'].map(season_map)

# Menampilkan hasil
#col4, col5, col6 = st.columns(3)
#with col5:
with st.container():
    st.write("**Clustering Jumlah Pengguna Berdasarkan Musim**")
    st.dataframe(df_casual_registered_group, use_container_width=True)


