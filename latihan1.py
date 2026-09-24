import numpy as np 
import pandas as pd

#arr1 = np.array([1, 2, 3, 4, 5])


#arr2d = np.array([[1, 2, 3],
 #                 [4, 5, 6]])


#arr3d = np.array([[[1, 2], [3, 4]],
 #                 [[5, 6], [7, 8]]])

#print(arr3d[1][0][0])
#print(type(arr1))

# NumPy → Pandas DataFrame
# arr = np.array([[85, 90, 78],
#                 [92, 88, 95],
#                 [76, 82, 89]])


# df = pd.DataFrame(arr,
#                   columns=["Matematika", "Fisika", "Kimia"],
#                   index=["Andi", "Budi", "Cici"])

#print(df)


# np_data = df.to_numpy()  # atau df.values
# print(np_data)

arr = np.array([10, 20, 30, 40, 50])

arr2d = np.array([[1, 2, 3],
                  [4, 5, 6]])

print(np.mean(arr2d, axis=0)) 




# data = {
#     'Nama'      : ['Andi', 'Budi', 'Cici', 'Deni', 'Eva', 'Fajar', 'Gita', 'Hana'],
#     'Kelas'     : ['X-A', 'X-B', 'X-A', 'X-B', 'X-A', 'X-B', 'X-A', 'X-B'],
#     'Matematika': [85, 90, 72, 88, 95, 60, 78, 83],
#     'IPA'       : [80, 85, 70, 92, 90, 65, 82, 79],
#     'Bahasa'    : [88, 75, 85, 80, 92, 70, 88, 91],
# }

# df = pd.DataFrame(data)
# print("=" * 50)
# print("DATA AWAL:")
# print("=" * 50)
# # Menampilkan keseluruhan isi tabel yang sudah dibuat
# print(df)

# df['Rata-rata'] = df[['Matematika', 'IPA', 'Bahasa']].mean(axis=1).round(2)
# print(df[[ 'Rata-rata']])