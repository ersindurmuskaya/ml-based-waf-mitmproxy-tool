import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, KFold
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from sklearn.metrics import accuracy_score
import pickle

############################################################

#2.veri onisleme
#2.1.veri yukleme
veriler = pd.read_csv("C:/Users/ersin/Desktop/makale_sonuc/3-osc/osc_all_bad_good2.csv")
#pd.read_csv("veriler.csv")
#test

X = veriler.iloc[:,0:8].values #bağımsız değişkenler
y = veriler.iloc[:,8:].values #bağımlı değişken
############################################################


# K-Fold için parametreleri belirle
#k_folds_degerleri = [2, 3, 5, 7, 10]
k_folds_degerleri = [2, 3, 4, 5, 6, 7, 8, 9, 10]

shuffle = True

# En iyi k-folds değerini bulmak için döngü
en_iyi_k_folds = 0
en_yuksek_dogruluk = 0
scores_dict = {}

for k_folds in k_folds_degerleri:
  scores = []

  # K-Fold cross validation için döngü
  kf = KFold(n_splits=k_folds, shuffle=shuffle)
  for train_index, test_index in kf.split(X, y):
    # Eğitim ve test veri kümelerini ayır
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    # Verileri standartlaştır
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # DT modelini oluştur ve eğit
    model = DecisionTreeClassifier(criterion = 'entropy', random_state=42)
    model.fit(X_train, y_train)

    # Modelin doğruluğunu test et
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)

    scores.append(accuracy)

  # Ortalama doğruluğu hesapla ve kaydet
  ortalama_dogruluk = sum(scores) / len(scores)
  scores_dict[k_folds] = ortalama_dogruluk

  # En yüksek doğruluğu ve k-folds değerini kaydet
  if ortalama_dogruluk > en_yuksek_dogruluk:
    en_yuksek_dogruluk = ortalama_dogruluk
    en_iyi_k_folds = k_folds

# Grafiği oluştur
plt.plot(k_folds_degerleri, scores_dict.values())
plt.xlabel("K-Folds Değeri")
plt.ylabel("Ortalama Doğruluk")
plt.title("K-Folds Değerine Göre Doğruluk (OSC)")
plt.show()

print("En İyi K-Folds Değeri:", en_iyi_k_folds)
print("En Yüksek Doğruluk:", en_yuksek_dogruluk)

# En iyi k-folds değeri ile modeli eğit ve kaydet
kf = KFold(n_splits=en_iyi_k_folds, shuffle=shuffle)
for train_index, test_index in kf.split(X, y):
  # Eğitim ve test veri kümelerini ayır
  X_train, X_test = X[train_index], X[test_index]
  y_train, y_test = y[train_index], y[test_index]

  # Verileri standartlaştır
  scaler = StandardScaler()
  X_train = scaler.fit_transform(X_train)
  X_test = scaler.transform(X_test)

  # SVM modelini oluştur ve eğit
  model = DecisionTreeClassifier(criterion = 'entropy', random_state=42)
  model.fit(X_train, y_train)
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print("En İyi K-Folds Değeri ile DT modelinin accuracy değeri:",accuracy )  

# Modeli kaydet
pickle.dump(model, open("waf_model.pkl", "wb"))
