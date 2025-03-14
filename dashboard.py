import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def monthly_count(df):
    monthly_count = df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()
    mapping_month = {
        1: "Januari", 2: "Februari", 3: "Maret", 4: "April",
        5: "Mei", 6: "Juni", 7: "Juli", 8: "Agustus",
        9: "September", 10: "Oktober", 11: "November", 12: "Desember"
    }

    monthly_count['mnth'] = monthly_count['mnth'].map(mapping_month)
    
    # Set kolom 'mnth' sebagai kategori terurut
    bulan_order = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
    monthly_count['mnth'] = pd.Categorical(monthly_count['mnth'], categories=bulan_order, ordered=True)


    return monthly_count

def season(df):
    season_df = df.groupby('season')['cnt'].sum().reset_index()
    return season_df

def temperature(df):
    bins_temp = [0, 0.3, 0.6, 1.0]  
    labels_temp = ['Dingin', 'Sejuk', 'Panas']

    df['temp_group'] = pd.cut(df['temp'], bins=bins_temp, labels=labels_temp)

    temp_df = df.groupby(['temp_group'])['cnt'].sum().reset_index()
    return temp_df

df = pd.read_csv('dashboard.csv')
df['dteday'] = pd.to_datetime(df['dteday'])

monthly_count_df = monthly_count(df)
season_df = season(df)
temperature_df = temperature(df)

st.title('Bike Sharing Analysis :bike:')

st.divider()
st.subheader("Tren Jumlah Penyewaan per-Bulan pada tahun 2011 dan 2012 :chart_with_upwards_trend:")

fig, ax = plt.subplots(figsize=(20,13))
sns.lineplot(
    data=monthly_count_df,
    x = "mnth",
    y="cnt",
    hue="yr",
    marker="o",
    linewidth = 5,
    markersize= 20,
    ax=ax
)
ax.set_title("Tren Penyewaan Sepeda per Bulan di Tahun 2011 dan 2012", fontsize=35, pad=30)
ax.set_xlabel(None)
ax.set_ylabel(None)
plt.xticks(range(0,12))
ax.tick_params(axis='x', labelsize=25, rotation=20, pad=20)
ax.tick_params(axis='y', labelsize=20)

ax.legend(fontsize=25, title="Tahun", title_fontsize=28, labelspacing=1.5)

plt.tight_layout()  
st.pyplot(fig)

with st.expander('Penjelasan'):
    st.write('Dapat dilihat bahwa fluktuasi penyewaan perbulan antara tahun 2011 dengan 2012 hampir sama. Pada tahun 2012 terdapat peningkatan jumlah penyewaan dari tahun 2012. Kedua tahun hampir memiliki tren yang sama yaitu terjadi peningkat pada pertengahan tahun dan penurunan pada awal tahun dan akhir tahun')




st.divider()


col1, col2 = st.columns(2)

with col1:
    st.write(f"**Pengaruh Musim Terhadap Total Penyewaan :mostly_sunny:**")
    fig, ax = plt.subplots(figsize=(20, 19))
 
    sns.barplot(
        x=season_df['season'], 
        y=season_df['cnt'],
        data= season_df,
        palette="coolwarm",
        ax=ax
    )
    ax.set_title("Jumlah Penyewa Berdasarkan Musim", loc="center", fontsize=40, pad=25)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=45)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

    with st.expander('Penjelasan'):
        st.write('Musim yang memiliki jumlah penyewa paling tinggi adalah musim gugur sedangkan yang memiliki jumlah penyewa paling sedikit adalah musim semi')

with col2:
    st.write(f"**Pengaruh Suhu Terhadap Total Penyewaan :thermometer:**")

    fig, ax = plt.subplots(figsize=(20, 18))
 
    sns.barplot(
        x=temperature_df['temp_group'], 
        y=temperature_df['cnt'],
        data= temperature_df,
        palette="coolwarm",
        ax=ax
    )
    ax.set_title("Jumlah Penyewa Berdasarkan Suhu", loc="center", fontsize=40, pad=25)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.tick_params(axis='x', labelsize=45)
    ax.tick_params(axis='y', labelsize=30)
    st.pyplot(fig)

    with st.expander('Penjelasan'):
        st.write('Pada jumlah penyewa yang telah dikelompokan berdasarkan suhu dengan kriteria 0 - 0.3(dingin), 0.3 - 0.6(sejuk) dan 0.6-1.0 panas. Hal ini menunjukan bahwa pada suhu dingin hanya sedikit total saja penyewaan sepeda sedangkan untuk suhu yang cenderung hangat cenderung lebih banyak')


st.header('Tren Penyewaan dari tahun 2011 hingga tahun 2012')

monthly_trend = df.groupby(['yr', 'mnth'])['cnt'].sum().reset_index()

monthly_trend['period'] = monthly_trend['yr'].astype(str) + '-' + monthly_trend['mnth'].astype(str).str.zfill(2)

monthly_trend['period'] = pd.to_datetime(monthly_trend['period'])


min_date = monthly_trend['period'].min().date()  
max_date = monthly_trend['period'].max().date()


start_date, end_date = st.date_input(
    label="Rentang Waktu", 
    min_value=min_date, 
    max_value=max_date,
    value=[min_date, max_date]
)


filtered_data = monthly_trend[
    (monthly_trend['period'].dt.date >= start_date) & 
    (monthly_trend['period'].dt.date <= end_date)
]


if filtered_data.empty:
    st.warning("Data tidak ditemukan pada rentang waktu yang dipilih.")
else :

    fig, ax = plt.subplots(figsize=(20, 18))

    sns.lineplot(
        x=filtered_data['period'], 
        y=filtered_data['cnt'],
        marker='o',
        data= filtered_data,
        palette="coolwarm",
        linewidth = 5,
        markersize= 14,
        ax=ax
    )

    ax.set_title("Jumlah Tren Penyewaan Sepeda dari Tahun 2011 hingga 2012", loc="center", fontsize=30, pad=20)
    ax.set_ylabel('Total Penyewaan', fontsize=30)
    ax.set_xlabel('Periode (Tahun-Bulan)', fontsize=35)
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=18) 
    ax.tick_params(axis='y', labelsize=25)
    ax.tick_params(axis='x', labelsize=25, rotation=45)

    st.pyplot(fig)



st.caption('Copyright (c) Rouf Semangat 2025')