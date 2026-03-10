# Beijing Air Quality Data Analysis

## Deskripsi Proyek

Proyek ini bertujuan untuk menganalisis kualitas udara di Beijing berdasarkan dataset **Beijing Air Quality Dataset (2013–2017)**.  
Analisis dilakukan menggunakan Python dengan pendekatan eksplorasi data, visualisasi, dan analisis lanjutan seperti clustering manual serta analisis geospasial.

Selain analisis dalam notebook, proyek ini juga menyertakan **dashboard interaktif menggunakan Streamlit** untuk memvisualisasikan data secara lebih informatif.

---

## Dataset

Dataset yang digunakan adalah **Beijing Multi-Site Air Quality Dataset** yang berisi data kualitas udara dari beberapa stasiun pemantauan di Beijing.

Dataset mencakup beberapa parameter polusi udara seperti:

- PM2.5
- PM10
- SO2
- NO2
- CO
- O3

Serta faktor meteorologi seperti:

- Temperatur (TEMP)
- Tekanan udara (PRES)
- Curah hujan (RAIN)
- Kecepatan angin (WSPM)

---

## Pertanyaan Analisis

Proyek ini berusaha menjawab beberapa pertanyaan berikut:

1. Bagaimana pola perubahan konsentrasi PM2.5 berdasarkan waktu (jam dan bulan)?
2. Stasiun pemantauan mana yang memiliki tingkat polusi PM2.5 tertinggi?
3. Bagaimana distribusi polusi udara berdasarkan lokasi geografis stasiun pemantauan?

---

## Setup Environment - Anaconda
```
conda create --name air-quality python=3.9
conda activate air-quality
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

## Run steamlit app
```
streamlit run dashboard/dashboard.py
```
