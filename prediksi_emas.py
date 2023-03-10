# -*- coding: utf-8 -*-
"""Prediksi Emas.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nnqnzIiU0QZvFpJsuUzs_MH8z830z5m6
"""

# This Python 3 environment comes with many helpful analytics libraries installed
# It is defined by the kaggle/python Docker image: https://github.com/kaggle/docker-python
# For example, here's several helpful packages to load

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)

# Input data files are available in the read-only "../input/" directory
# For example, running this (by clicking run or pressing Shift+Enter) will list all files under the input directory

import os
for dirname, _, filenames in os.walk('/kaggle/input'):
    for filename in filenames:
        print(os.path.join(dirname, filename))

# You can write up to 20GB to the current directory (/kaggle/working/) that gets preserved as output when you create a version using "Save & Run All" 
# You can also write temporary files to /kaggle/temp/, but they won't be saved outside of the current session

"""**Import library**"""

import matplotlib.pyplot as plt
import sklearn.metrics as metrics
# import seaborn as sns
# import warnings
# warnings.simplefilter('ignore')
#pandas dan numpy done

"""**Load data**"""

data_location = '1990-2021.csv'
row_data = pd.read_csv(data_location)
row_data.shape

#membaca data 5 teratas
row_data.head()

"""**Membersihkan data yang tidak lengkap (Jika ada)**"""

df = row_data.dropna(axis=0)
df.describe()

print(df.dtypes)

"""**Menentukan variabel independen dan dependen**"""

#Menentukan varibel independen dari data sehingga, menghapus varibel dependen yaitu harga
x = df.drop(["Indonesia(IDR)"],axis = 1)
x.head()

#Menampilkan data varibel dependen
y = df["Indonesia(IDR)"]
y.head()

"""**Membagi data untuk training dan validasi**"""

from sklearn.model_selection import train_test_split
train_x, test_x, train_y, test_y = train_test_split(x,y,test_size = 0.2, random_state = 70)

"""**Membangun model dengan algoritma K-Nearest Neighbors**"""

from sklearn.neighbors import KNeighborsRegressor as KNN_Reg
from sklearn.metrics import mean_squared_error as mse

model  = KNN_Reg(n_neighbors = 1)

#training model
model.fit(train_x, train_y)
acc1 = model.score(test_x, test_y)

# test for prediction
test_predict = model.predict(test_x)
score = mse(test_predict, test_y)
print(' MSE: ', score, '\n', 'Accuracy: ', acc1)

"""**Menggunakan elbow method untuk menentukan nilai K terbaik**"""

def Elbow(K):
  #inisialisasi list kosong
  test_mse =[]

  #train model pada setiap nilai K
  for i in K:
    model = KNN_Reg(n_neighbors=i)
    model.fit(train_x, train_y)
    tmp = model.predict(test_x)
    tmp = mse(tmp, test_y)
    test_mse.append(tmp)
  
  return test_mse

"""**Menampilkan grafik nilai k berdasarkan MSE**"""

K = range(1, 10)
test = Elbow(K)

#plotting
plt.plot(K,test)
plt.xlabel('K Neighbors')
plt.ylabel('Mean Squared Error (MSE)')
plt.title('Elbow Curve for Test')

"""**Melakukan improvisasi dengan menerapkan nilai k yang menghasilkan MSE minimum**"""

new_model  = KNN_Reg(n_neighbors = 3)

# Train model
new_model.fit(train_x, train_y)
acc2 = new_model.score(test_x, test_y)

# Prediction test
print(' Accuracy of new model (%):', acc2*100, '\n',
      'Accuracy of old model (%):', acc1*100, '\n Improvement (%):', (acc2-acc1)*100)

data_emas = np.array([[12,2]])
pred_old = model.predict(data_emas)
pred_new = new_model.predict(data_emas)

print(' Hasil Prediksi harga emas dengan old model: Rp', pred_old, 'Juta\n',
      'Hasil Prediksi harga emas dengan new model: Rp', pred_new, 'Juta')