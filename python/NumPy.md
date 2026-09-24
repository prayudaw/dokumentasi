# 📘 Roadmap Belajar NumPy di Python

> **NumPy** (Numerical Python) adalah library fundamental untuk komputasi numerik di Python.
> Digunakan secara luas dalam Data Science, Machine Learning, dan Scientific Computing.

---

## 🗺️ Roadmap Overview

```
Level 1: Dasar          ➜ Instalasi, Array, Indexing, Slicing
Level 2: Menengah       ➜ Operasi Matematika, Broadcasting, Reshaping
Level 3: Lanjutan       ➜ Linear Algebra, Random, Statistik
Level 4: Praktik        ➜ Studi Kasus & Integrasi dengan Pandas/Matplotlib
```

---

## 📦 Level 1 — Dasar-Dasar NumPy

### 1.1 Instalasi NumPy

```bash
pip install numpy
```

### 1.2 Import NumPy

```python
import numpy as np
```

### 1.3 Membuat Array

```python
# Dari list Python
arr1 = np.array([1, 2, 3, 4, 5])
print(arr1)           # [1 2 3 4 5]
print(type(arr1))     # <class 'numpy.ndarray'>

# Array 2 Dimensi (Matrix)
arr2d = np.array([[1, 2, 3],
                  [4, 5, 6]])
print(arr2d)
# [[1 2 3]
#  [4 5 6]]

# Array 3 Dimensi
arr3d = np.array([[[1, 2], [3, 4]],
                  [[5, 6], [7, 8]]])
print(arr3d.ndim)     # 3
```

### 1.4 Fungsi Pembuat Array

```python
# Array berisi angka nol
zeros = np.zeros((3, 4))        # Matrix 3x4 berisi 0

# Array berisi angka satu
ones = np.ones((2, 3))          # Matrix 2x3 berisi 1

# Array berisi nilai tertentu
full = np.full((2, 2), 7)       # Matrix 2x2 berisi 7

# Array identitas (diagonal = 1)
identity = np.eye(3)            # Matrix identitas 3x3

# Array dengan range
range_arr = np.arange(0, 10, 2) # [0 2 4 6 8] (start, stop, step)

# Array dengan jarak merata
linspace = np.linspace(0, 1, 5) # [0.   0.25 0.5  0.75 1.  ] (5 elemen dari 0-1)

# Array kosong (tanpa inisialisasi)
empty = np.empty((2, 3))        # Nilai random dari memori
```

### 1.5 Atribut Array

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

print(arr.shape)    # (2, 3) → 2 baris, 3 kolom
print(arr.ndim)     # 2      → jumlah dimensi
print(arr.size)     # 6      → total elemen
print(arr.dtype)    # int64  → tipe data elemen
print(arr.itemsize) # 8      → ukuran tiap elemen (bytes)
print(arr.nbytes)   # 48     → total memori (bytes)
```

### 1.6 Indexing & Slicing

```python
arr = np.array([10, 20, 30, 40, 50])

# Indexing (akses elemen)
print(arr[0])    # 10   → elemen pertama
print(arr[-1])   # 50   → elemen terakhir

# Slicing (potong array)
print(arr[1:4])  # [20 30 40] → elemen index 1 sampai 3
print(arr[:3])   # [10 20 30] → 3 elemen pertama
print(arr[2:])   # [30 40 50] → dari index 2 ke akhir
print(arr[::2])  # [10 30 50] → setiap 2 langkah

# Indexing 2D
arr2d = np.array([[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]])

print(arr2d[0, 0])    # 1  → baris 0, kolom 0
print(arr2d[1, 2])    # 6  → baris 1, kolom 2
print(arr2d[0:2, 1:]) # [[2 3]  → baris 0-1, kolom 1 ke akhir
                       #  [5 6]]

# Boolean Indexing (Fancy Indexing)
arr = np.array([1, 2, 3, 4, 5, 6])
mask = arr > 3
print(arr[mask])       # [4 5 6]
print(arr[arr % 2 == 0])  # [2 4 6] → elemen genap
```

---

## ⚙️ Level 2 — Operasi & Manipulasi

### 2.1 Operasi Aritmatika (Element-wise)

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(a + b)   # [5 7 9]   → penjumlahan
print(a - b)   # [-3 -3 -3] → pengurangan
print(a * b)   # [4 10 18]  → perkalian
print(a / b)   # [0.25 0.4 0.5] → pembagian
print(a ** 2)  # [1 4 9]    → pangkat
print(a % 2)   # [1 0 1]    → modulo

# Fungsi matematika
print(np.sqrt(a))    # [1.   1.41 1.73] → akar kuadrat
print(np.exp(a))     # [2.72 7.39 20.09] → eksponensial
print(np.log(a))     # [0.   0.69 1.10]  → logaritma natural
print(np.abs([-1, -2, 3]))  # [1 2 3]   → nilai absolut
print(np.sin(a))     # sin dari setiap elemen
print(np.cos(a))     # cos dari setiap elemen
```

### 2.2 Operasi Agregat (Statistik Dasar)

```python
arr = np.array([10, 20, 30, 40, 50])

print(np.sum(arr))     # 150   → total
print(np.mean(arr))    # 30.0  → rata-rata
print(np.median(arr))  # 30.0  → median
print(np.std(arr))     # 14.14 → standar deviasi
print(np.var(arr))     # 200.0 → varians
print(np.min(arr))     # 10    → minimum
print(np.max(arr))     # 50    → maksimum
print(np.argmin(arr))  # 0     → index elemen terkecil
print(np.argmax(arr))  # 4     → index elemen terbesar

# Operasi per axis (baris/kolom)
arr2d = np.array([[1, 2, 3],
                  [4, 5, 6]])

print(np.sum(arr2d, axis=0))  # [5 7 9]   → jumlah per kolom
print(np.sum(arr2d, axis=1))  # [6 15]    → jumlah per baris
print(np.mean(arr2d, axis=0)) # [2.5 3.5 4.5] → rata-rata per kolom
```

### 2.3 Broadcasting

```python
# Broadcasting: operasi antara array dengan bentuk berbeda
arr = np.array([[1, 2, 3],
                [4, 5, 6]])  # Shape: (2, 3)

scalar = 10
print(arr + scalar)  # Scalar di-broadcast ke semua elemen
# [[11 12 13]
#  [14 15 16]]

# Broadcasting 1D ke 2D
row = np.array([100, 200, 300])  # Shape: (3,)
print(arr + row)
# [[101 202 303]
#  [104 205 306]]

col = np.array([[10],
                [20]])           # Shape: (2, 1)
print(arr + col)
# [[11 12 13]
#  [24 25 26]]
```

### 2.4 Reshaping & Manipulasi Bentuk

```python
arr = np.array([1, 2, 3, 4, 5, 6])

# Reshape: ubah bentuk array
reshaped = arr.reshape(2, 3)
print(reshaped)
# [[1 2 3]
#  [4 5 6]]

reshaped = arr.reshape(3, 2)
print(reshaped)
# [[1 2]
#  [3 4]
#  [5 6]]

# Reshape otomatis dengan -1
print(arr.reshape(2, -1))  # (2, 3) → NumPy hitung otomatis
print(arr.reshape(-1, 2))  # (3, 2)

# Flatten: ubah ke 1D
arr2d = np.array([[1, 2], [3, 4]])
print(arr2d.flatten())     # [1 2 3 4]
print(arr2d.ravel())       # [1 2 3 4] (referensi, lebih hemat memori)

# Transpose
print(arr2d.T)
# [[1 3]
#  [2 4]]

# Menambah dimensi
arr1d = np.array([1, 2, 3])
print(arr1d[np.newaxis, :])  # [[1 2 3]] → shape (1, 3) → row vector
print(arr1d[:, np.newaxis])  # [[1]      → shape (3, 1) → column vector
                              #  [2]
                              #  [3]]
```

### 2.5 Menggabung & Memisah Array

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

# Concatenate (gabung)
print(np.concatenate([a, b]))      # [1 2 3 4 5 6]

# Stack (gabung dengan dimensi baru)
print(np.vstack([a, b]))  # Vertikal → [[1 2 3]
                           #              [4 5 6]]
print(np.hstack([a, b]))  # Horizontal → [1 2 3 4 5 6]

# 2D concatenate
x = np.array([[1, 2], [3, 4]])
y = np.array([[5, 6], [7, 8]])

print(np.concatenate([x, y], axis=0))  # Gabung baris
# [[1 2]
#  [3 4]
#  [5 6]
#  [7 8]]

print(np.concatenate([x, y], axis=1))  # Gabung kolom
# [[1 2 5 6]
#  [3 4 7 8]]

# Split (pisah)
arr = np.array([1, 2, 3, 4, 5, 6])
print(np.split(arr, 3))     # [array([1,2]), array([3,4]), array([5,6])]
print(np.split(arr, [2, 4])) # Split di index 2 dan 4
```

### 2.6 Sorting (Pengurutan)

```python
arr = np.array([3, 1, 4, 1, 5, 9, 2, 6])

print(np.sort(arr))          # [1 1 2 3 4 5 6 9] → sorted copy
print(np.argsort(arr))       # [1 3 6 0 2 4 7 5] → index urutan

# Sorting 2D
arr2d = np.array([[3, 1, 2],
                  [6, 4, 5]])
print(np.sort(arr2d, axis=1))  # Sort per baris
# [[1 2 3]
#  [4 5 6]]
```

---

## 🧮 Level 3 — Topik Lanjutan

### 3.1 Linear Algebra

```python
# Dot Product (perkalian matriks)
A = np.array([[1, 2],
              [3, 4]])
B = np.array([[5, 6],
              [7, 8]])

print(np.dot(A, B))      # atau A @ B
# [[19 22]
#  [43 50]]

# Determinan
print(np.linalg.det(A))  # -2.0

# Invers matriks
print(np.linalg.inv(A))
# [[-2.   1. ]
#  [ 1.5 -0.5]]

# Eigenvalue & Eigenvector
eigenvalues, eigenvectors = np.linalg.eig(A)
print("Eigenvalues:", eigenvalues)
print("Eigenvectors:\n", eigenvectors)

# Solve sistem persamaan linear: Ax = b
# 2x + 3y = 8
# x  + 2y = 5
A = np.array([[2, 3],
              [1, 2]])
b = np.array([8, 5])
x = np.linalg.solve(A, b)
print(x)  # [1. 2.] → x=1, y=2

# Norm (panjang vektor)
v = np.array([3, 4])
print(np.linalg.norm(v))  # 5.0
```

### 3.2 Random Number Generation

```python
# Set seed untuk reproducibility
np.random.seed(42)
rng = np.random.default_rng(42)  # Cara modern (recommended)

# Random integer
print(np.random.randint(1, 10, size=5))     # 5 angka random 1-9

# Random float (0-1)
print(np.random.random((2, 3)))             # Matrix 2x3 random

# Distribusi Normal (Gaussian)
normal = np.random.normal(loc=0, scale=1, size=1000)  # mean=0, std=1
print(f"Mean: {normal.mean():.4f}, Std: {normal.std():.4f}")

# Distribusi Uniform
uniform = np.random.uniform(low=0, high=10, size=5)

# Random choice (pilih acak dari array)
arr = np.array([10, 20, 30, 40, 50])
print(np.random.choice(arr, size=3, replace=False))  # Pilih 3 tanpa duplikat

# Shuffle (acak urutan)
np.random.shuffle(arr)
print(arr)

# Permutasi
print(np.random.permutation(10))  # [0-9] dalam urutan acak
```

### 3.3 Operasi Set (Himpunan)

```python
a = np.array([1, 2, 3, 4, 5])
b = np.array([3, 4, 5, 6, 7])

print(np.union1d(a, b))       # [1 2 3 4 5 6 7] → gabungan
print(np.intersect1d(a, b))   # [3 4 5]         → irisan
print(np.setdiff1d(a, b))     # [1 2]           → di a, tidak di b
print(np.setxor1d(a, b))      # [1 2 6 7]       → XOR (bukan irisan)
print(np.in1d(a, b))          # [F F T T T]     → cek keanggotaan
print(np.unique([1,1,2,3,3])) # [1 2 3]         → elemen unik
```

### 3.4 Kondisional & Where

```python
arr = np.array([1, 2, 3, 4, 5, 6])

# np.where → seperti if-else untuk array
result = np.where(arr > 3, "besar", "kecil")
print(result)  # ['kecil' 'kecil' 'kecil' 'besar' 'besar' 'besar']

# np.where → cari index
indices = np.where(arr > 3)
print(indices)  # (array([3, 4, 5]),)

# np.clip → batasi nilai
print(np.clip(arr, 2, 4))  # [2 2 3 4 4 4]

# np.any & np.all
print(np.any(arr > 5))   # True  → ada elemen > 5?
print(np.all(arr > 0))   # True  → semua elemen > 0?
print(np.all(arr > 3))   # False → tidak semua > 3
```

### 3.5 Tipe Data NumPy

```python
# Menentukan tipe data saat membuat array
arr_float = np.array([1, 2, 3], dtype=np.float64)
arr_int = np.array([1.5, 2.7, 3.9], dtype=np.int32)  # [1 2 3] → dipotong
arr_bool = np.array([1, 0, 1], dtype=np.bool_)        # [True False True]

# Konversi tipe data
arr = np.array([1, 2, 3])
arr_float = arr.astype(np.float64)
print(arr_float)  # [1. 2. 3.]

# Tipe data yang tersedia:
# np.int8, np.int16, np.int32, np.int64
# np.float16, np.float32, np.float64
# np.complex64, np.complex128
# np.bool_, np.str_, np.object_
```

### 3.6 Copy vs View

```python
arr = np.array([1, 2, 3, 4, 5])

# View (referensi → perubahan mempengaruhi asli)
view = arr[1:4]
view[0] = 99
print(arr)  # [1 99 3 4 5] → arr ikut berubah!

# Copy (salinan → independen)
arr = np.array([1, 2, 3, 4, 5])
copy = arr[1:4].copy()
copy[0] = 99
print(arr)  # [1 2 3 4 5] → arr tidak berubah
```

---

## 🚀 Level 4 — Praktik & Integrasi

### 4.1 Membaca/Menulis File

```python
# Simpan & muat array
arr = np.array([[1, 2, 3], [4, 5, 6]])

# Format .npy (binary NumPy)
np.save("data.npy", arr)
loaded = np.load("data.npy")

# Format .npz (multiple arrays, compressed)
np.savez("data.npz", x=arr, y=arr*2)
data = np.load("data.npz")
print(data["x"])
print(data["y"])

# Format CSV/Text
np.savetxt("data.csv", arr, delimiter=",", header="a,b,c")
loaded_csv = np.loadtxt("data.csv", delimiter=",")
```

### 4.2 Performance: NumPy vs Python List

```python
import time

size = 1_000_000

# Python list
py_list = list(range(size))
start = time.time()
result = [x * 2 for x in py_list]
print(f"Python list: {time.time() - start:.4f} detik")

# NumPy array
np_arr = np.arange(size)
start = time.time()
result = np_arr * 2
print(f"NumPy array: {time.time() - start:.4f} detik")

# NumPy biasanya 10-100x lebih cepat!
```

### 4.3 Integrasi dengan Pandas

```python
import pandas as pd

# NumPy → Pandas DataFrame
arr = np.array([[85, 90, 78],
                [92, 88, 95],
                [76, 82, 89]])

df = pd.DataFrame(arr,
                  columns=["Matematika", "Fisika", "Kimia"],
                  index=["Andi", "Budi", "Cici"])
print(df)

# Pandas → NumPy
np_data = df.to_numpy()  # atau df.values
print(np_data)
```

### 4.4 Integrasi dengan Matplotlib

```python
import matplotlib.pyplot as plt

# Plot fungsi matematika
x = np.linspace(0, 2 * np.pi, 100)
y_sin = np.sin(x)
y_cos = np.cos(x)

plt.figure(figsize=(10, 5))
plt.plot(x, y_sin, label="sin(x)", color="blue")
plt.plot(x, y_cos, label="cos(x)", color="red")
plt.title("Grafik Sin & Cos")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()
```

### 4.5 Studi Kasus: Analisis Data Sederhana

```python
# Simulasi data nilai ujian 100 siswa
np.random.seed(42)
nilai = np.random.normal(loc=75, scale=10, size=100).astype(int)
nilai = np.clip(nilai, 0, 100)  # Batasi 0-100

# Analisis
print(f"Jumlah siswa   : {nilai.size}")
print(f"Rata-rata      : {np.mean(nilai):.1f}")
print(f"Median         : {np.median(nilai):.1f}")
print(f"Standar Deviasi: {np.std(nilai):.1f}")
print(f"Nilai Tertinggi: {np.max(nilai)}")
print(f"Nilai Terendah : {np.min(nilai)}")
print(f"Lulus (>= 60)  : {np.sum(nilai >= 60)} siswa")
print(f"Tidak Lulus    : {np.sum(nilai < 60)} siswa")
print(f"Persentil 25%  : {np.percentile(nilai, 25):.1f}")
print(f"Persentil 75%  : {np.percentile(nilai, 75):.1f}")

# Distribusi grade
grade_A = np.sum(nilai >= 85)
grade_B = np.sum((nilai >= 70) & (nilai < 85))
grade_C = np.sum((nilai >= 60) & (nilai < 70))
grade_D = np.sum(nilai < 60)

print(f"\nDistribusi Grade:")
print(f"A (>= 85): {grade_A} siswa")
print(f"B (70-84): {grade_B} siswa")
print(f"C (60-69): {grade_C} siswa")
print(f"D (< 60) : {grade_D} siswa")
```

---

## 📋 Cheat Sheet Ringkas

| Kategori | Fungsi | Deskripsi |
|---|---|---|
| **Buat Array** | `np.array()` | Dari list |
| | `np.zeros()` | Array berisi 0 |
| | `np.ones()` | Array berisi 1 |
| | `np.arange()` | Range dengan step |
| | `np.linspace()` | Range dengan jumlah elemen |
| **Info** | `.shape` | Dimensi array |
| | `.dtype` | Tipe data |
| | `.size` | Jumlah elemen |
| **Manipulasi** | `.reshape()` | Ubah bentuk |
| | `.flatten()` | Jadikan 1D |
| | `.T` | Transpose |
| **Matematika** | `np.sum()` | Total |
| | `np.mean()` | Rata-rata |
| | `np.std()` | Standar deviasi |
| | `np.min()` / `np.max()` | Minimum / Maksimum |
| **Gabung/Pisah** | `np.concatenate()` | Gabung array |
| | `np.vstack()` / `np.hstack()` | Stack vertikal / horizontal |
| | `np.split()` | Pisah array |
| **Linear Algebra** | `np.dot()` / `@` | Perkalian matriks |
| | `np.linalg.inv()` | Invers |
| | `np.linalg.det()` | Determinan |
| **Random** | `np.random.randint()` | Random integer |
| | `np.random.normal()` | Distribusi normal |
| | `np.random.choice()` | Pilih acak |
| **Kondisi** | `np.where()` | If-else untuk array |
| | `np.clip()` | Batasi range nilai |

---

## 🎯 Tips Belajar

1. **Ketik sendiri** semua contoh kode, jangan copy-paste
2. **Eksperimen** dengan mengubah parameter dan lihat hasilnya
3. **Gunakan `print()`** untuk melihat shape, dtype, dan isi array
4. **Baca error message** dengan teliti — NumPy memberikan pesan yang informatif
5. **Praktik dengan data nyata** setelah menguasai dasar

## 📚 Sumber Belajar Tambahan

- [Dokumentasi Resmi NumPy](https://numpy.org/doc/stable/)
- [NumPy Quickstart Tutorial](https://numpy.org/doc/stable/user/quickstart.html)
- [NumPy for Absolute Beginners](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [100 NumPy Exercises](https://github.com/rougier/numpy-100)

---

> 💡 **Catatan**: Roadmap ini dirancang untuk dipelajari secara berurutan.
> Kuasai setiap level sebelum lanjut ke level berikutnya.
> Estimasi waktu belajar: **2-4 minggu** (1-2 jam per hari).
