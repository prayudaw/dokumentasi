"""
=============================================================
📊 Contoh Penerapan NumPy pada Project Data Science / Data Analysis
=============================================================
File ini berisi contoh-contoh nyata bagaimana NumPy digunakan
dalam project Data Science dan Data Analysis sehari-hari.
"""

import numpy as np

# ============================================================
# 📌 PROJECT 1: Analisis Data Penjualan Toko Online
# ============================================================
# Skenario: Kamu adalah Data Analyst di sebuah toko online.
# Kamu punya data penjualan 6 bulan dari 4 kategori produk.

print("=" * 60)
print("PROJECT 1: Analisis Data Penjualan Toko Online")
print("=" * 60)

# Data penjualan (dalam juta rupiah)
# Dimensi 0 = Cabang (0: Jakarta, 1: Bandung)
# Dimensi 1 = Bulan (Jan-Jun)
# Dimensi 2 = Kategori (Elektronik, Fashion, Makanan, Buku)
penjualan = np.array([
    # Cabang Jakarta
    [
        [150, 80, 200, 30],   # Januari
        [170, 95, 180, 35],   # Februari
        [160, 110, 220, 28],  # Maret
        [200, 120, 250, 40],  # April
        [180, 100, 230, 38],  # Mei
        [210, 130, 270, 45],  # Juni
    ],
    # Cabang Bandung
    [
        [120, 60, 150, 25],   # Januari
        [130, 75, 140, 20],   # Februari
        [140, 90, 160, 30],   # Maret
        [150, 85, 180, 35],   # April
        [160, 110, 170, 40],  # Mei
        [180, 120, 200, 50],  # Juni
    ]
])

cabang = ["Jakarta", "Bandung"]
bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni"]
kategori = ["Elektronik", "Fashion", "Makanan", "Buku"]

# --- Analisis 1: Total penjualan per cabang ---
# Sum pada axis 1 (bulan) dan axis 2 (kategori)
total_per_cabang = np.sum(penjualan, axis=(1, 2))
print("\n🏢 Total Penjualan per Cabang (Juta Rp):")
for cab, total in zip(cabang, total_per_cabang):
    print(f"   {cab:10s}: Rp {total} juta")

# --- Analisis 2: Total penjualan per kategori (Semua Cabang) ---
# Sum pada axis 0 (cabang) dan axis 1 (bulan)
total_per_kategori = np.sum(penjualan, axis=(0, 1))
print("\n📦 Total Penjualan per Kategori (Semua Cabang):")
for kat, total in zip(kategori, total_per_kategori):
    print(f"   {kat:12s}: Rp {total} juta")

# --- Analisis 3: Total penjualan per bulan (Semua Cabang) ---
# Sum pada axis 0 (cabang) dan axis 2 (kategori)
total_per_bulan = np.sum(penjualan, axis=(0, 2))
print("\n📅 Total Penjualan per Bulan (Semua Cabang):")
for bln, total in zip(bulan, total_per_bulan):
    print(f"   {bln:10s}: Rp {total} juta")

# --- Analisis 4: Bulan dengan penjualan tertinggi (Nasional) ---
bulan_terbaik_idx = np.argmax(total_per_bulan)
print(f"\n🏆 Bulan terbaik (Nasional): {bulan[bulan_terbaik_idx]} (Rp {total_per_bulan[bulan_terbaik_idx]} juta)")

# --- Analisis 5: Kategori paling laris (Nasional) ---
kategori_terbaik_idx = np.argmax(total_per_kategori)
print(f"🥇 Kategori terlaris (Nasional): {kategori[kategori_terbaik_idx]} (Rp {total_per_kategori[kategori_terbaik_idx]} juta)")

# --- Analisis 6: Perbandingan Performa Cabang (Pertumbuhan Bulanan) ---
# Hitung total per bulan untuk masing-masing cabang
total_bulan_per_cabang = np.sum(penjualan, axis=2) # Shape: (2 cabang, 6 bulan)
pertumbuhan_cabang = np.diff(total_bulan_per_cabang, axis=1) / total_bulan_per_cabang[:, :-1] * 100

print("\n📈 Pertumbuhan Bulanan per Cabang:")
for i, cab in enumerate(cabang):
    print(f"   Cabang {cab}:")
    for j, growth in enumerate(pertumbuhan_cabang[i]):
        arrow = "↑" if growth > 0 else "↓"
        print(f"      {bulan[j]} → {bulan[j+1]}: {arrow} {growth:+.1f}%")

# --- Analisis 7: Kontribusi setiap kategori di Cabang Jakarta (%) ---
total_kategori_jkt = np.sum(penjualan[0], axis=0) # Index 0 = Jakarta, sum over months
kontribusi_jkt = total_kategori_jkt / np.sum(total_kategori_jkt) * 100
print("\n🥧 Kontribusi per Kategori di Cabang Jakarta:")
for kat, pct in zip(kategori, kontribusi_jkt):
    bar = "█" * int(pct / 2)
    print(f"   {kat:12s}: {pct:5.1f}% {bar}")

# --- Analisis 8: Statistik Penjualan (Seluruh Data) ---
print("\n📊 Statistik Keseluruhan (Juta Rp):")
print(f"   Rata-rata penjualan per item/bulan : {np.mean(penjualan):.1f}")
print(f"   Standar deviasi penjualan          : {np.std(penjualan):.1f}")
print(f"   Nilai penjualan terendah           : {np.min(penjualan)}")
print(f"   Nilai penjualan tertinggi          : {np.max(penjualan)}")


# ============================================================
# 📌 PROJECT 2: Analisis Performa Karyawan
# ============================================================
# Skenario: HRD meminta kamu menganalisis KPI 20 karyawan

print("\n\n" + "=" * 60)
print("PROJECT 2: Analisis Performa Karyawan")
print("=" * 60)

np.random.seed(123)

# Simulasi data 20 karyawan
jumlah_karyawan = 20
nama_karyawan = [f"Karyawan_{i+1:02d}" for i in range(jumlah_karyawan)]

# KPI: Produktivitas (0-100), Kehadiran (%), Kualitas (0-100)
produktivitas = np.random.normal(loc=72, scale=12, size=jumlah_karyawan).clip(0, 100).round(1)
kehadiran = np.random.normal(loc=90, scale=8, size=jumlah_karyawan).clip(50, 100).round(1)
kualitas = np.random.normal(loc=78, scale=10, size=jumlah_karyawan).clip(0, 100).round(1)

# Gabungkan jadi matrix KPI
kpi_matrix = np.column_stack([produktivitas, kehadiran, kualitas])

# --- Hitung skor akhir dengan bobot ---
# Bobot: Produktivitas 40%, Kehadiran 30%, Kualitas 30%
bobot = np.array([0.4, 0.3, 0.3])
skor_akhir = np.dot(kpi_matrix, bobot)  # Dot product untuk weighted score

print("\n👥 Top 5 Karyawan:")
print(f"   {'Nama':15s} {'Produktivitas':>14s} {'Kehadiran':>10s} {'Kualitas':>10s} {'Skor Akhir':>12s}")
print(f"   {'-'*64}")

# Urutkan berdasarkan skor akhir (tertinggi dulu)
ranking = np.argsort(skor_akhir)[::-1]
for rank, idx in enumerate(ranking[:5], 1):
    print(f"   {nama_karyawan[idx]:15s} {produktivitas[idx]:>14.1f} {kehadiran[idx]:>10.1f} {kualitas[idx]:>10.1f} {skor_akhir[idx]:>12.1f}")

# --- Klasifikasi performa ---
print("\n📋 Klasifikasi Performa:")
excellent = np.sum(skor_akhir >= 85)
good = np.sum((skor_akhir >= 70) & (skor_akhir < 85))
average = np.sum((skor_akhir >= 55) & (skor_akhir < 70))
poor = np.sum(skor_akhir < 55)
print(f"   ⭐ Excellent (≥85) : {excellent} orang ({excellent/jumlah_karyawan*100:.0f}%)")
print(f"   ✅ Good (70-84)    : {good} orang ({good/jumlah_karyawan*100:.0f}%)")
print(f"   ⚠️  Average (55-69) : {average} orang ({average/jumlah_karyawan*100:.0f}%)")
print(f"   ❌ Poor (<55)      : {poor} orang ({poor/jumlah_karyawan*100:.0f}%)")

# --- Korelasi antar KPI ---
# Apakah produktivitas tinggi berkaitan dengan kehadiran tinggi?
korelasi = np.corrcoef(kpi_matrix.T)
kpi_names = ["Produktivitas", "Kehadiran", "Kualitas"]
print("\n🔗 Matriks Korelasi antar KPI:")
print(f"   {'':15s}", end="")
for name in kpi_names:
    print(f" {name:>14s}", end="")
print()
for i, name in enumerate(kpi_names):
    print(f"   {name:15s}", end="")
    for j in range(3):
        print(f" {korelasi[i, j]:>14.3f}", end="")
    print()


# ============================================================
# 📌 PROJECT 3: Deteksi Anomali pada Data Sensor
# ============================================================
# Skenario: Kamu menganalisis data sensor suhu mesin pabrik
# untuk mendeteksi anomali (suhu tidak normal)

print("\n\n" + "=" * 60)
print("PROJECT 3: Deteksi Anomali Data Sensor Suhu")
print("=" * 60)

np.random.seed(42)

# Simulasi 200 pembacaan sensor suhu (°C)
# Normal: sekitar 65°C, dengan sedikit variasi
suhu_normal = np.random.normal(loc=65, scale=3, size=200)

# Tambahkan beberapa anomali
anomali_indices = [15, 42, 78, 123, 167]
suhu_data = suhu_normal.copy()
suhu_data[15] = 95    # Overheat!
suhu_data[42] = 30    # Terlalu dingin
suhu_data[78] = 88    # Overheat!
suhu_data[123] = 25   # Terlalu dingin
suhu_data[167] = 92   # Overheat!

# --- Metode Z-Score untuk deteksi anomali ---
mean_suhu = np.mean(suhu_data)
std_suhu = np.std(suhu_data)
z_scores = np.abs((suhu_data - mean_suhu) / std_suhu)

# Anomali jika z-score > 2 (lebih dari 2 standar deviasi)
threshold = 2
anomali_mask = z_scores > threshold
anomali_detected = np.where(anomali_mask)[0]

print(f"\n🌡️ Statistik Suhu:")
print(f"   Rata-rata : {mean_suhu:.1f}°C")
print(f"   Std Dev   : {std_suhu:.1f}°C")
print(f"   Minimum   : {np.min(suhu_data):.1f}°C")
print(f"   Maximum   : {np.max(suhu_data):.1f}°C")

print(f"\n🚨 Anomali Terdeteksi (Z-Score > {threshold}):")
print(f"   Jumlah anomali: {np.sum(anomali_mask)} dari {len(suhu_data)} pembacaan")
for idx in anomali_detected:
    status = "🔥 OVERHEAT" if suhu_data[idx] > mean_suhu else "🧊 TERLALU DINGIN"
    print(f"   Sensor #{idx:3d}: {suhu_data[idx]:6.1f}°C (Z-Score: {z_scores[idx]:.2f}) → {status}")

# --- Batas normal ---
batas_bawah = mean_suhu - threshold * std_suhu
batas_atas = mean_suhu + threshold * std_suhu
print(f"\n📏 Batas Normal: {batas_bawah:.1f}°C - {batas_atas:.1f}°C")

# --- Persentase data normal ---
persen_normal = np.sum(~anomali_mask) / len(suhu_data) * 100
print(f"✅ Data Normal: {persen_normal:.1f}%")


# ============================================================
# 📌 PROJECT 4: Sistem Rekomendasi Sederhana (Cosine Similarity)
# ============================================================
# Skenario: Membuat rekomendasi produk berdasarkan kesamaan
# preferensi antar user

print("\n\n" + "=" * 60)
print("PROJECT 4: Sistem Rekomendasi Sederhana")
print("=" * 60)

# Rating user terhadap produk (1-5, 0 = belum rating)
# Baris = User, Kolom = Produk (Laptop, HP, Tablet, Headset, Smartwatch)
ratings = np.array([
    [5, 3, 4, 0, 2],   # User A
    [4, 0, 4, 3, 3],   # User B
    [0, 2, 1, 5, 4],   # User C
    [5, 4, 5, 1, 1],   # User D
    [1, 1, 0, 4, 5],   # User E
])

users = ["User A", "User B", "User C", "User D", "User E"]
produk = ["Laptop", "HP", "Tablet", "Headset", "Smartwatch"]

# --- Hitung Cosine Similarity antar user ---
def cosine_similarity(a, b):
    """Menghitung cosine similarity antara 2 vektor."""
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 0
    return dot / (norm_a * norm_b)

# Hitung similarity matrix
n_users = len(users)
similarity_matrix = np.zeros((n_users, n_users))
for i in range(n_users):
    for j in range(n_users):
        similarity_matrix[i, j] = cosine_similarity(ratings[i], ratings[j])

print("\n🔗 Cosine Similarity antar User:")
print(f"   {'':8s}", end="")
for u in users:
    print(f" {u:>8s}", end="")
print()
for i, u in enumerate(users):
    print(f"   {u:8s}", end="")
    for j in range(n_users):
        print(f" {similarity_matrix[i, j]:>8.3f}", end="")
    print()

# --- Rekomendasi untuk User A ---
target_user = 0  # User A
print(f"\n🎯 Rekomendasi untuk {users[target_user]}:")

# Cari user paling mirip (selain diri sendiri)
similarities = similarity_matrix[target_user].copy()
similarities[target_user] = -1  # Exclude diri sendiri
most_similar_idx = np.argmax(similarities)
print(f"   User paling mirip: {users[most_similar_idx]} (similarity: {similarities[most_similar_idx]:.3f})")

# Rekomendasikan produk yang belum di-rating oleh target user
# tapi di-rating tinggi oleh user yang mirip
belum_rating = np.where(ratings[target_user] == 0)[0]
print(f"\n   Produk yang belum di-rating oleh {users[target_user]}:")
for idx in belum_rating:
    rating_similar = ratings[most_similar_idx, idx]
    rec = "⭐ DIREKOMENDASIKAN" if rating_similar >= 4 else "Biasa saja"
    print(f"   → {produk[idx]:12s} (Rating {users[most_similar_idx]}: {rating_similar}) {rec}")


# ============================================================
# 📌 PROJECT 5: Normalisasi Data (Preprocessing)
# ============================================================
# Skenario: Mempersiapkan data sebelum masuk ke model ML.
# Data harus dinormalisasi agar fitur dengan skala berbeda
# tidak mendominasi model.

print("\n\n" + "=" * 60)
print("PROJECT 5: Normalisasi Data (Preprocessing untuk ML)")
print("=" * 60)

# Data mentah: Usia, Gaji (juta), Pengalaman (tahun)
data_mentah = np.array([
    [25, 5,  1],
    [30, 8,  3],
    [35, 15, 7],
    [28, 6,  2],
    [45, 25, 15],
    [22, 4,  0],
    [40, 20, 10],
    [33, 12, 5],
])
fitur = ["Usia", "Gaji (Jt)", "Pengalaman"]

print("\n📊 Data Mentah:")
print(f"   {'':4s} {fitur[0]:>8s} {fitur[1]:>12s} {fitur[2]:>12s}")
for i, row in enumerate(data_mentah):
    print(f"   #{i+1:2d}  {row[0]:>8.0f} {row[1]:>12.0f} {row[2]:>12.0f}")

# --- Metode 1: Min-Max Normalization (0-1) ---
min_vals = np.min(data_mentah, axis=0)
max_vals = np.max(data_mentah, axis=0)
data_minmax = (data_mentah - min_vals) / (max_vals - min_vals)

print("\n📐 Setelah Min-Max Normalization (0-1):")
print(f"   {'':4s} {fitur[0]:>8s} {fitur[1]:>12s} {fitur[2]:>12s}")
for i, row in enumerate(data_minmax):
    print(f"   #{i+1:2d}  {row[0]:>8.3f} {row[1]:>12.3f} {row[2]:>12.3f}")

# --- Metode 2: Z-Score Standardization ---
mean_vals = np.mean(data_mentah, axis=0)
std_vals = np.std(data_mentah, axis=0)
data_zscore = (data_mentah - mean_vals) / std_vals

print("\n📐 Setelah Z-Score Standardization (mean=0, std=1):")
print(f"   {'':4s} {fitur[0]:>8s} {fitur[1]:>12s} {fitur[2]:>12s}")
for i, row in enumerate(data_zscore):
    print(f"   #{i+1:2d}  {row[0]:>8.3f} {row[1]:>12.3f} {row[2]:>12.3f}")

# Verifikasi: mean ≈ 0, std ≈ 1
print("\n✅ Verifikasi Z-Score:")
print(f"   Mean setelah normalisasi: {np.mean(data_zscore, axis=0).round(10)}")
print(f"   Std setelah normalisasi : {np.std(data_zscore, axis=0).round(4)}")


# ============================================================
# 📌 RINGKASAN: Kapan NumPy Digunakan di Dunia Nyata?
# ============================================================

print("\n\n" + "=" * 60)
print("RINGKASAN: Penggunaan NumPy di Dunia Nyata")
print("=" * 60)

ringkasan = """
┌─────────────────────────────────────────────────────────────┐
│  Bidang              │  Penggunaan NumPy                    │
├─────────────────────────────────────────────────────────────┤
│  Data Analysis       │  Statistik, agregasi, filtering      │
│  Machine Learning    │  Normalisasi, matrix operasi, vektor │
│  Computer Vision     │  Manipulasi pixel gambar (array 3D)  │
│  NLP                 │  Word embeddings, TF-IDF matrix      │
│  Finance             │  Analisis saham, risiko, portfolio    │
│  Scientific Research │  Simulasi, komputasi numerik         │
│  IoT / Sensor        │  Analisis time-series, deteksi       │
│                      │  anomali                             │
│  Rekomendasi         │  Cosine similarity, collaborative    │
│                      │  filtering                           │
└─────────────────────────────────────────────────────────────┘

💡 Ingat: NumPy adalah FONDASI dari hampir semua library
   Data Science di Python (Pandas, Scikit-learn, TensorFlow,
   PyTorch, dll.)
"""
print(ringkasan)
