import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from streamlit_folium import st_folium

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="Beijing Air Quality Dashboard",
    layout="wide"
)

sns.set_style("whitegrid")

# ==============================
# TITLE
# ==============================

st.title("📊 Beijing Air Quality Dashboard")

st.markdown("""
Dashboard ini menampilkan analisis kualitas udara Beijing berdasarkan dataset **Air Quality 2013–2017**.  
Visualisasi mencakup tren PM2.5, distribusi polusi udara, pola polusi berdasarkan waktu, serta distribusi geografis stasiun pemantauan.
""")

# ==============================
# LOAD DATA
# ==============================

df = pd.read_csv("dashboard/main_data.csv")

# ==============================
# SIDEBAR FILTER
# ==============================

st.sidebar.header("Filter Data")

station = st.sidebar.multiselect(
    "Pilih Stasiun",
    options=df["station"].unique(),
    default=df["station"].unique()
)

df_filtered = df[df["station"].isin(station)]

# ==============================
# METRICS SUMMARY
# ==============================

st.subheader("Ringkasan Kualitas Udara")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Average PM2.5", f"{df_filtered['PM2.5'].mean():.2f}")
col2.metric("Max PM2.5", f"{df_filtered['PM2.5'].max():.2f}")
col3.metric("Min PM2.5", f"{df_filtered['PM2.5'].min():.2f}")
col4.metric("Total Records", f"{len(df_filtered)}")

st.divider()

# ==============================
# CHARTS ROW
# ==============================

col1, col2 = st.columns(2)

# Trend PM2.5
with col1:

    st.subheader("Trend PM2.5 per Bulan")

    pm25_month = df_filtered.groupby("month")["PM2.5"].mean()

    fig, ax = plt.subplots(figsize=(6,4))

    sns.lineplot(
        x=pm25_month.index,
        y=pm25_month.values,
        marker="o",
        ax=ax
    )

    ax.set_xlabel("Bulan")
    ax.set_ylabel("PM2.5")

    st.pyplot(fig)

# Distribusi PM2.5
with col2:

    st.subheader("Distribusi PM2.5")

    fig2, ax2 = plt.subplots(figsize=(6,4))

    sns.histplot(df_filtered["PM2.5"], bins=40, ax=ax2)

    ax2.set_xlabel("PM2.5")

    st.pyplot(fig2)

st.divider()

# ==============================
# POLUSI PER JAM
# ==============================

st.subheader("Pola PM2.5 Berdasarkan Jam")

pm25_hour = df_filtered.groupby("hour")["PM2.5"].mean()

fig3, ax3 = plt.subplots(figsize=(10,4))

sns.lineplot(
    x=pm25_hour.index,
    y=pm25_hour.values,
    marker="o",
    ax=ax3
)

ax3.set_xlabel("Jam")
ax3.set_ylabel("PM2.5")

st.pyplot(fig3)

st.divider()

# ==============================
# RANKING STASIUN
# ==============================

st.subheader("Ranking Stasiun dengan Polusi Tertinggi")

pm25_rank = df_filtered.groupby("station")["PM2.5"].mean().sort_values(ascending=False)

fig4, ax4 = plt.subplots(figsize=(8,4))

pm25_rank.plot(
    kind="bar",
    color="firebrick",
    ax=ax4
)

ax4.set_ylabel("PM2.5")
ax4.set_xlabel("Station")

st.pyplot(fig4)

st.divider()

# ==============================
# MAP
# ==============================

st.subheader("Peta Distribusi PM2.5")

station_location = {
"Aotizhongxin": (39.982,116.397),
"Changping": (40.217,116.231),
"Dingling": (40.292,116.220),
"Dongsi": (39.929,116.417),
"Guanyuan": (39.933,116.339),
"Gucheng": (39.914,116.184),
"Huairou": (40.357,116.631),
"Nongzhanguan": (39.937,116.461),
"Shunyi": (40.127,116.655),
"Tiantan": (39.886,116.407),
"Wanliu": (39.987,116.298),
"Wanshouxigong": (39.878,116.352)
}

pm25_station = df_filtered.groupby("station")["PM2.5"].mean().reset_index()

map_beijing = folium.Map(location=[39.9042,116.4074], zoom_start=10)

min_pm = pm25_station["PM2.5"].min()
max_pm = pm25_station["PM2.5"].max()

def get_color(pm):

    if pd.isna(pm):
        return "#ffff00"

    if max_pm == min_pm:
        ratio = 1
    else:
        ratio = (pm - min_pm) / (max_pm - min_pm)

    r = 255
    g = int(255 * (1 - ratio))
    b = 0

    return f'#{r:02x}{g:02x}{b:02x}'

for _, row in pm25_station.iterrows():

    station = row["station"]
    pm25 = row["PM2.5"]

    lat, lon = station_location[station]

    color = get_color(pm25)

    folium.CircleMarker(
        location=[lat,lon],
        radius=8,
        popup=f"{station} PM2.5:{pm25:.2f}",
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8
    ).add_to(map_beijing)

st_folium(map_beijing, width=1200, height=500)