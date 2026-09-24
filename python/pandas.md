# 🐼 Resume Lengkap: Pandas (Python)

> **Pandas** adalah library Python open-source yang digunakan untuk **manipulasi dan analisis data**. Pandas menyediakan struktur data yang cepat, fleksibel, dan ekspresif, khususnya untuk data berbentuk tabel (seperti spreadsheet Excel atau tabel database SQL).

---

## 📦 Cara Install Pandas

### Menggunakan pip (cara paling umum)

```bash
pip install pandas
```

### Install beserta library pendukung (direkomendasikan)

```bash
# openpyxl untuk baca/tulis file Excel (.xlsx)
# matplotlib untuk visualisasi data
pip install pandas openpyxl matplotlib
```

### Verifikasi instalasi

```python
import pandas as pd
print(pd.__version__)
```

---

## 🏗️ Konsep Inti Pandas

### 1. Series — Array 1 Dimensi Berlabel

`Series` adalah struktur data 1D seperti kolom dalam sebuah tabel. Setiap elemen memiliki **label (index)**.

```python
import pandas as pd

# Membuat Series dari list
nilai = pd.Series([85, 90, 78, 92], index=['Andi', 'Budi', 'Cici', 'Deni'])
print(nilai)
# Output:
# Andi    85
# Budi    90
# Cici    78
# Deni    92

# Mengakses elemen
print(nilai['Budi'])   # Output: 90
print(nilai[0])        # Output: 85
```

---

### 2. DataFrame — Tabel 2 Dimensi (Inti dari Pandas)

`DataFrame` adalah struktur data 2D seperti **tabel spreadsheet**, terdiri dari baris dan kolom berlabel.

```python
import pandas as pd

data = {
    'Nama'  : ['Andi', 'Budi', 'Cici', 'Deni'],
    'Usia'  : [20, 22, 21, 23],
    'Nilai' : [85, 90, 78, 92],
    'Lulus' : [True, True, True, True]
}

df = pd.DataFrame(data)
print(df)
#    Nama  Usia  Nilai  Lulus
# 0  Andi    20     85   True
# 1  Budi    22     90   True
# 2  Cici    21     78   True
# 3  Deni    23     92   True
```

---

### 3. Membaca & Menulis Data

```python
import pandas as pd

# MEMBACA DATA
df_csv   = pd.read_csv('data.csv')
df_excel = pd.read_excel('data.xlsx')
df_json  = pd.read_json('data.json')

# MENULIS DATA
df.to_csv('output.csv', index=False)
df.to_excel('output.xlsx', index=False)
df.to_json('output.json', orient='records')
```

---

### 4. Eksplorasi Data

```python
df.head(5)        # Menampilkan 5 baris pertama
df.tail(5)        # Menampilkan 5 baris terakhir
df.shape          # Jumlah (baris, kolom) contoh: (4, 3)
df.info()         # Tipe data tiap kolom & info memori
df.describe()     # Statistik ringkas (min, max, mean, dll)
df.columns        # Daftar nama kolom
df.dtypes         # Tipe data setiap kolom
df.isnull().sum() # Menghitung jumlah nilai kosong (NaN)
```

---

### 5. Seleksi & Filter Data

```python
import pandas as pd

data = {'Nama': ['Andi','Budi','Cici','Deni'], 'Nilai': [85, 90, 78, 92], 'Kota': ['Jakarta','Bandung','Jakarta','Surabaya']}
df = pd.DataFrame(data)

# Memilih Kolom
print(df['Nama'])              # 1 kolom -> Series
print(df[['Nama', 'Nilai']])   # Beberapa kolom -> DataFrame

# Memilih Baris berdasarkan Posisi (iloc)
print(df.iloc[0])              # Baris pertama
print(df.iloc[1:3])            # Baris ke-1 sampai ke-2

# Memilih berdasarkan Label (loc)
print(df.loc[0, 'Nama'])       # Baris 0, Kolom 'Nama'

# Filter / Kondisi
df_lulus    = df[df['Nilai'] >= 80]
df_jakarta  = df[df['Kota'] == 'Jakarta']
df_gabungan = df[(df['Nilai'] >= 80) & (df['Kota'] == 'Jakarta')]
```

---

### 6. Manipulasi Data

```python
# Menambah Kolom Baru
df['Grade']    = ['B', 'A', 'B+', 'A']
df['Nilai_x2'] = df['Nilai'] * 2

# Mengubah Nama Kolom
df.rename(columns={'Nama': 'Nama Siswa'}, inplace=True)

# Menghapus Kolom & Baris
df.drop(columns=['Nilai_x2'], inplace=True)
df.drop(index=0, inplace=True)

# Sorting
df.sort_values(by='Nilai', ascending=False)
```

---

### 7. Menangani Data Kosong (Missing Values)

```python
import numpy as np

data = {'Nama': ['Andi', 'Budi', None, 'Deni'], 'Nilai': [85, np.nan, 78, 92]}
df = pd.DataFrame(data)

df.isnull().sum()                       # Hitung total nilai kosong
df.dropna()                             # Hapus baris yang ada nilai kosong
df.fillna(0)                            # Isi nilai kosong dengan 0
df['Nilai'].fillna(df['Nilai'].mean())  # Isi dengan rata-rata
```

---

### 8. Grouping & Agregasi

```python
data = {'Kota': ['Jakarta','Bandung','Jakarta','Bandung'], 'Nilai': [85, 90, 78, 92]}
df = pd.DataFrame(data)

# Rata-rata per Kota
print(df.groupby('Kota')['Nilai'].mean())

# Berbagai agregasi sekaligus
print(df.groupby('Kota')['Nilai'].agg(['mean', 'min', 'max', 'count']))
```

---

### 9. Menggabungkan DataFrame

```python
df1 = pd.DataFrame({'ID': [1, 2, 3], 'Nama': ['Andi', 'Budi', 'Cici']})
df2 = pd.DataFrame({'ID': [2, 3, 4], 'Nilai': [90, 78, 85]})

# merge: seperti JOIN di SQL
df_inner = pd.merge(df1, df2, on='ID', how='inner')  # Hanya ID yang ada di keduanya
df_left  = pd.merge(df1, df2, on='ID', how='left')   # Semua data dari df1

# concat: menumpuk DataFrame
df_bawah  = pd.concat([df1, df2], axis=0)  # Tambah baris
df_samping = pd.concat([df1, df2], axis=1) # Tambah kolom
```

---

## 🚀 Contoh Project: Analisis Nilai Siswa

Simpan kode berikut ke file baru: **`project_pandas.py`**

```python
import pandas as pd

# 1. MEMBUAT DATA
data = {
    'Nama'      : ['Andi', 'Budi', 'Cici', 'Deni', 'Eva', 'Fajar', 'Gita', 'Hana'],
    'Kelas'     : ['X-A', 'X-B', 'X-A', 'X-B', 'X-A', 'X-B', 'X-A', 'X-B'],
    'Matematika': [85, 90, 72, 88, 95, 60, 78, 83],
    'IPA'       : [80, 85, 70, 92, 90, 65, 82, 79],
    'Bahasa'    : [88, 75, 85, 80, 92, 70, 88, 91],
}

df = pd.DataFrame(data)
print("=" * 50)
print("DATA AWAL:")
print(df)

# 2. HITUNG RATA-RATA & TENTUKAN GRADE
df['Rata-rata'] = df[['Matematika', 'IPA', 'Bahasa']].mean(axis=1).round(2)

def tentukan_grade(nilai):
    if nilai >= 90:   return 'A'
    elif nilai >= 80: return 'B'
    elif nilai >= 70: return 'C'
    elif nilai >= 60: return 'D'
    else:             return 'E'

df['Grade']  = df['Rata-rata'].apply(tentukan_grade)
df['Status'] = df['Rata-rata'].apply(lambda x: 'LULUS' if x >= 75 else 'REMEDIAL')

# 3. TAMPILKAN HASIL
print("\n" + "=" * 50)
print("HASIL AKHIR:")
print(df[['Nama', 'Kelas', 'Rata-rata', 'Grade', 'Status']])

# 4. ANALISIS PER KELAS
print("\n" + "=" * 50)
print("ANALISIS PER KELAS:")
analisis = df.groupby('Kelas')['Rata-rata'].agg(
    Rata_rata='mean',
    Tertinggi='max',
    Terendah='min',
    Jumlah='count'
).round(2)
print(analisis)

# 5. PERINGKAT SISWA
print("\n" + "=" * 50)
print("PERINGKAT SISWA:")
peringkat = df[['Nama', 'Rata-rata', 'Grade']].sort_values(
    by='Rata-rata', ascending=False
).reset_index(drop=True)
peringkat.index += 1
print(peringkat)

# 6. SIMPAN KE CSV
df.to_csv('laporan_nilai.csv', index=False)
print("\nLaporan disimpan ke laporan_nilai.csv!")
```

---

## 📚 Ringkasan Konsep

| Konsep                  | Fungsi Utama                           |
| :---------------------- | :------------------------------------- |
| `pd.Series`             | Struktur data 1D (satu kolom berlabel) |
| `pd.DataFrame`          | Struktur data 2D (tabel)               |
| `read_csv / read_excel` | Membaca data dari file                 |
| `to_csv / to_excel`     | Menyimpan data ke file                 |
| `head() / tail()`       | Melihat sebagian data                  |
| `info() / describe()`   | Eksplorasi info & statistik            |
| `iloc / loc`            | Seleksi baris dan kolom                |
| `dropna() / fillna()`   | Menangani data kosong                  |
| `groupby()`             | Mengelompokkan & merangkum data        |
| `merge() / concat()`    | Menggabungkan beberapa DataFrame       |
| `sort_values()`         | Mengurutkan data                       |
| `apply()`               | Menerapkan fungsi ke tiap baris/kolom  |
