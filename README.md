## 📓 Penjelasan Notebook Utama

### 1. Processing & Analysis
Memuat dataset sensor pertanian (`cropdata_updated.csv`) dan melakukan eksplorasi awal
untuk memahami struktur data, tipe kolom, dan statistik deskriptif.

### 2. Data Cleaning
- Menghapus missing value dengan `dropna()`
- Menyeragamkan nama kolom (huruf kecil + underscore)
- Visualisasi outlier menggunakan boxplot pada kolom `moi`, `temp`, dan `humidity`
- Dataset tidak memiliki kolom datetime sehingga konversi tidak diperlukan

### 3. Data Analysis
- **Correlation Heatmap** — menganalisis hubungan antar variabel sensor
- **Time Series Trend** — memvisualisasikan tren kelembaban tanah (MOI) dari waktu ke waktu
- Hasil cleaning disimpan sebagai `cleaned_data.csv`

### 4. Data Quality Score
Mengukur kualitas dataset menggunakan dua metrik:
| **Accuracy** | Persentase data yang tidak bermasalah |
| **Completeness** | Persentase data yang tersedia (tidak kosong) |

> Dataset tidak memiliki kolom timestamp sehingga metrik **Timeliness** tidak dihitung.

## 📊 Penjelasan Dashboard

Dashboard dibangun menggunakan **Streamlit** dan dapat diakses di:
🔗 https://data-smart-agriculture-23082010225.streamlit.app/

### Fitur yang tersedia:

**1. ⚙️ Sidebar Control**
Pengguna dapat memilih sensor (moi, temp, humidity) dan mengatur
nilai threshold minimum secara interaktif menggunakan slider.

**2. 📊 KPI Cards**
Menampilkan ringkasan statistik sensor yang dipilih: rata-rata,
nilai minimum, maksimum, dan nilai sensor terkini beserta selisihnya.

**3. 📈 Time Series**
Grafik tren nilai sensor dari waktu ke waktu, dilengkapi keterangan
otomatis apakah tren meningkat, menurun, atau stabil.

**4. 🎯 Gauge Monitor & Alert System**
Gauge chart menampilkan nilai sensor saat ini. Alert otomatis muncul:
- 🔴 Merah jika nilai di bawah threshold
- 🟡 Kuning jika mendekati batas minimum
- 🟢 Hijau jika kondisi optimal

**5. 🌾 Soil Type Distribution**
Bar chart distribusi jenis tanah, dapat difilter per jenis tanah.

**6. 🔥 Correlation Heatmap**
Visualisasi korelasi antar variabel sensor menggunakan heatmap,
membantu mengidentifikasi hubungan antar sensor pertanian.
