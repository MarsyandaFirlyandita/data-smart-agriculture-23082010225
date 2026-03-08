import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import os

st.set_page_config(
    page_title="Smart Agriculture Dashboard",
    layout="wide"
)

# Load Data
@st.cache_data
def load_data():
    base_dir = os.path.dirname(__file__)
    file_path = os.path.join(base_dir, "..", "outputs", "cleaned_data.csv")
    return pd.read_csv(file_path)

df = load_data()
numeric_df = df.select_dtypes(include="number")

# Title
st.title("🌱 Smart Agriculture Monitoring Dashboard")
st.caption("Interactive dashboard untuk analisis sensor pertanian")


# Sidebar Control
st.sidebar.header("⚙️ Dashboard Control")
sensor = st.sidebar.selectbox(
    "Pilih Sensor",
    ["moi", "temp", "humadity"]
)

sensor_info = {
    "moi": "MOI menunjukkan tingkat kelembaban tanah.",
    "temp": "Temperature menunjukkan suhu lingkungan tanaman.",
    "humidity": "Humidity menunjukkan kelembaban udara di sekitar tanaman."
}

st.info(sensor_info.get(sensor, "Sensor monitoring"))

default_threshold = {
    "moi": 40,
    "temp": 20,
    "humidity": 50
}

threshold = st.sidebar.slider(
    "Threshold Minimum",
    float(numeric_df[sensor].min()),
    float(numeric_df[sensor].max()),
    float(default_threshold.get(sensor, numeric_df[sensor].mean()))
)


# KPI Cards
st.divider()
st.subheader("📊 Ringkasan Sensor")
avg_value = df[sensor].mean()
min_value = df[sensor].min()
max_value = df[sensor].max()
latest_value = df[sensor].iloc[-1]

c1, c2, c3 = st.columns(3)

c1.metric(
    label=f"📈 Rata-rata {sensor}",
    value=f"{avg_value:.2f}",
    delta=f"{latest_value - avg_value:.2f}"
)

c2.metric(
    label=f"📉 Minimum {sensor}",
    value=f"{min_value:.2f}"
)

c3.metric(
    label=f"📊 Maksimum {sensor}",
    value=f"{max_value:.2f}"
)

c4 = st.columns(1)[0]

c4.metric(
    label=f"🎯 Nilai Sensor Saat Ini ({sensor})",
    value=f"{latest_value:.2f}"
)


# Time Series
st.divider()
st.subheader("📈 Time Series Data Sensor")
df_ts = df[[sensor]].copy()
df_ts["time"] = range(len(df_ts))
st.line_chart(df_ts.set_index("time"))


trend = df[sensor].iloc[-1] - df[sensor].iloc[0]
if trend > 0:
    st.info(f"📈 Nilai {sensor} menunjukkan tren meningkat selama periode observasi")
elif trend < 0:
    st.info(f"📉 Nilai {sensor} menunjukkan tren menurun selama periode observasi")
else:
    st.info(f"➖ Nilai {sensor} relatif stabil")


# Gauge & Alert
st.divider()
st.subheader("🎯 Monitoring Kondisi Terkini")
latest_value = df[sensor].iloc[-1]

col1, col2 = st.columns(2)

with col1:
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=latest_value,
        title={"text": sensor},
        gauge={
            "axis": {
                "range": [
                    float(numeric_df.min().min()),
                    float(numeric_df.max().max())
                ]
            }
        }
    ))
    st.plotly_chart(fig_gauge, use_container_width=True)

with col2:
    if latest_value < threshold:
        st.error("🔴 Kelembaban tanah terlalu rendah, tanaman membutuhkan penyiraman")
    elif latest_value < threshold * 1.1:
        st.warning("🟡 Kelembaban tanah mendekati batas minimum, perlu pemantauan")
    else:
        st.success("🟢 Kelembaban tanah dalam kondisi optimal")


# Soil Type
st.divider()
st.subheader("🌾 Informasi Soil Type")
soil_selected = st.selectbox(
    "Pilih Jenis Tanah",
    ["All"] + list(df["soil_type"].unique())
)

if soil_selected =="All":
    soil_data = df
else:
    soil_data = df[df["soil_type"] == soil_selected]

soil_counts = soil_data["soil_type"].value_counts()
st.bar_chart(soil_counts)

st.caption(
"Grafik ini menunjukkan distribusi jenis tanah pada dataset "
"yang dapat mempengaruhi kondisi pertumbuhan tanaman."
)


# Heatmap Correlation
st.divider()
st.subheader("🔥 Korelasi Antar Sensor")
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(numeric_df.corr(), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig)

st.caption(
"Heatmap menunjukkan hubungan antar sensor. "
"Nilai mendekati 1 berarti hubungan positif kuat, "
"nilai mendekati -1 menunjukkan hubungan negatif."
)





