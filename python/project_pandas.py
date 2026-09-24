import pandas as pd

# 1. MEMBUAT DATA
# Variabel `data` ini adalah sebuah tipe data Dictionary di Python.
# Setiap Key (contoh: 'Nama', 'Kelas') akan menjadi nama kolom.
# Setiap Value (berupa List) akan menjadi isi baris dari atas ke bawah untuk kolom tersebut.
data = {
    'Nama'      : ['Andi', 'Budi', 'Cici', 'Deni', 'Eva', 'Fajar', 'Gita', 'Hana'],
    'Kelas'     : ['X-A', 'X-B', 'X-A', 'X-B', 'X-A', 'X-B', 'X-A', 'X-B'],
    'Matematika': [85, 90, 72, 88, 95, 60, 78, 83],
    'IPA'       : [80, 85, 70, 92, 90, 65, 82, 79],
    'Bahasa'    : [88, 75, 85, 80, 92, 70, 88, 91],
}

# `pd.DataFrame(data)` digunakan untuk mengubah tipe data Dictionary di atas menjadi 
# sebuah tabel 2 Dimensi (baris dan kolom) yang sangat mudah diolah oleh Pandas.
df = pd.DataFrame(data)

print("=" * 50)
print("DATA AWAL:")
print("=" * 50)
# Menampilkan keseluruhan isi tabel yang sudah dibuat
print(df)


# 2. HITUNG RATA-RATA & TENTUKAN GRADE
# `df[['Matematika', 'IPA', 'Bahasa']]` : Mengambil hanya 3 kolom nilai tersebut.
# `.mean(axis=1)` : Menghitung nilai rata-rata secara horizontal (tiap baris / per siswa). 
#                   Jika `axis=0`, maka menghitung rata-rata vertikal (per mata pelajaran).
# `.round(2)` : Membulatkan hasil rata-rata menjadi 2 angka di belakang koma.
# Nilai yang didapat lalu dimasukkan ke dalam sebuah kolom baru bernama 'Rata-rata'.
df['Rata-rata'] = df[['Matematika', 'IPA', 'Bahasa']].mean(axis=1).round(2)

# Fungsi sederhana Python biasa (def) untuk mengubah angka menjadi huruf A/B/C/D/E
def tentukan_grade(nilai):
    if nilai >= 90:   return 'A'
    elif nilai >= 80: return 'B'
    elif nilai >= 70: return 'C'
    elif nilai >= 60: return 'D'
    else:             return 'E'

# `.apply(tentukan_grade)` : Menjalankan fungsi `tentukan_grade` ke SETIAP baris 
# yang ada di dalam kolom 'Rata-rata'.
# Hasil hurufnya (A/B/C...) akan disimpan ke dalam kolom baru bernama 'Grade'.
df['Grade']  = df['Rata-rata'].apply(tentukan_grade)

# Serupa dengan di atas, menggunakan `.apply()` dengan lambda (fungsi sebaris/anonim).
# Untuk setiap angka `x` di kolom 'Rata-rata', jika `x >= 75` maka isi dengan 'LULUS', 
# selain itu isi dengan 'REMEDIAL'. Kolom barunya diberi nama 'Status'.
df['Status'] = df['Rata-rata'].apply(lambda x: 'LULUS' if x >= 75 else 'REMEDIAL')


# 3. TAMPILKAN HASIL
print("\n" + "=" * 50)
print("HASIL AKHIR:")
print("=" * 50)
# df[['...']] digunakan untuk menampilkan tabel, tapi HANYA kolom-kolom yang dipilih saja.
print(df[['Nama', 'Kelas', 'Rata-rata', 'Grade', 'Status']])


# 4. ANALISIS PER KELAS
print("\n" + "=" * 50)
print("ANALISIS PER KELAS:")
print("=" * 50)
# `df.groupby('Kelas')` : Mengelompokkan tabel berdasarkan kesamaan isi di kolom 'Kelas' (X-A dan X-B).
# `['Rata-rata']` : Setelah dikelompokkan, kita hanya peduli pada nilai di kolom 'Rata-rata'.
# `.agg(...)` : Melakukan berbagai perhitungan sekaligus pada kolom yang dikelompokkan tadi.
analisis = df.groupby('Kelas')['Rata-rata'].agg(
    Rata_rata='mean',     # 'mean' = rata-rata keseluruhan kelas
    Tertinggi='max',      # 'max' = nilai terbesar di kelas itu
    Terendah='min',       # 'min' = nilai terkecil di kelas itu
    Jumlah='count'        # 'count' = menghitung ada berapa siswa di kelas itu
).round(2)                # Bulatkan semua hasil agregat ke 2 angka desimal
print(analisis)


# 5. PERINGKAT SISWA
print("\n" + "=" * 50)
print("PERINGKAT SISWA:")
print("=" * 50)
# `.sort_values(by='Rata-rata', ascending=False)` : Mengurutkan isi tabel berdasarkan kolom 'Rata-rata'.
# `ascending=False` artinya diurutkan dari nilai yang paling BESAR ke KECIL (Z-A / Ranking 1 di atas).
# `.reset_index(drop=True)` : Mereset nomor baris di kiri tabel (index) agar kembali mulai dari 0,1,2 secara berurutan
#                             meskipun datanya sudah diacak urutannya.
peringkat = df[['Nama', 'Rata-rata', 'Grade']].sort_values(
    by='Rata-rata', ascending=False
).reset_index(drop=True)

# Menambahkan angka 1 pada index, agar nomor urut peringkatnya dimulai dari angka 1, bukan angka 0.
peringkat.index += 1
print(peringkat)


# 6. SIMPAN KE CSV
# `.to_csv()` : Mengubah tabel (DataFrame) ini menjadi sebuah file excel/csv sungguhan.
# 'laporan_nilai.csv' : adalah nama file yang akan dibuat.
# `index=False` : Mencegah nomor urut indeks (0, 1, 2...) ikut tersimpan ke dalam file CSV.
df.to_csv('laporan_nilai.csv', index=False)
print("\nLaporan disimpan ke laporan_nilai.csv!")
