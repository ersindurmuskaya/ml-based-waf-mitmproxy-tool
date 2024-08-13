# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 21:25:56 2023

@author: ersin
"""
#1.kutuphaneler
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#2.veri onisleme
#2.1.veri yukleme
veriler = pd.read_csv("C:/Users/ersin/Desktop/makale_sonuc/4-lfi/lfi_all_bad_good2.csv")
#pd.read_csv("veriler.csv")
#test

x = veriler.iloc[:,0:7].values #bağımsız değişkenler
y = veriler.iloc[:,7:].values #bağımlı değişken

#verilerin egitim ve test icin bolunmesi
from sklearn.model_selection import train_test_split

x_train, x_test,y_train,y_test = train_test_split(x,y,test_size=0.3, random_state=10)

#verilerin olceklenmesi
from sklearn.preprocessing import StandardScaler

sc=StandardScaler()

X_train = sc.fit_transform(x_train)
X_test = sc.transform(x_test)

#########################################################################
from sklearn.linear_model import LogisticRegression
logr = LogisticRegression(random_state=0)
logr.fit(X_train,y_train)

y_pred_lr = logr.predict(X_test)

from sklearn.metrics import confusion_matrix
cm_lr = confusion_matrix(y_test,y_pred_lr)

print("lr")
print(cm_lr)
from sklearn.metrics import f1_score
f1_skor_lr=f1_score(y_test, y_pred_lr, average='macro')
print(f1_skor_lr)

#########################################################################
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb.fit(X_train, y_train)

y_pred_gnb = gnb.predict(X_test)

cm_gnb = confusion_matrix(y_test,y_pred_gnb)
print('GNB')
print(cm_gnb)
f1_skor_gnb=f1_score(y_test, y_pred_gnb, average='micro')
print(f1_skor_gnb)
#########################################################################
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=1, metric='minkowski')
knn.fit(X_train,y_train)

y_pred_knn = knn.predict(X_test)

cm_knn = confusion_matrix(y_test,y_pred_knn)
print('KNN')
print(cm_knn)
f1_skor_knn=f1_score(y_test, y_pred_knn, average='micro')
print(f1_skor_knn)
#########################################################################
from sklearn.svm import SVC
svc = SVC(kernel='rbf')
svc.fit(X_train,y_train)

y_pred_svc = svc.predict(X_test)

cm_svc = confusion_matrix(y_test,y_pred_svc)
print('SVC')
print(cm_svc)
f1_skor_svc=f1_score(y_test, y_pred_svc, average='micro')
print(f1_skor_svc)
#########################################################################
from sklearn.tree import DecisionTreeClassifier
dtc = DecisionTreeClassifier(criterion = 'entropy')

dtc.fit(X_train,y_train)
y_pred_dtc = dtc.predict(X_test)

cm_dtc = confusion_matrix(y_test,y_pred_dtc)
print('DTC')
print(cm_dtc)
f1_skor_dtc=f1_score(y_test, y_pred_dtc, average='micro')
print(f1_skor_dtc)

from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder

# Label encoding işlemi
label_encoder = LabelEncoder()
y_test_encoded = label_encoder.fit_transform(y_test)

# Modellerin tahmin ettiği olasılık skorları
y_scores_lr = logr.predict_proba(X_test)[:,1]  # Logistic Regression
y_scores_gnb = gnb.predict_proba(X_test)[:,1]  # Gaussian Naive Bayes
y_scores_knn = knn.predict_proba(X_test)[:,1]  # K-Nearest Neighbors
y_scores_svc = svc.decision_function(X_test)   # Support Vector Machine
y_scores_dtc = dtc.predict_proba(X_test)[:,1]  # Decision Tree Classifier

# ROC eğrileri çizme
fpr_lr, tpr_lr, _ = roc_curve(y_test_encoded, y_scores_lr)
roc_auc_lr = auc(fpr_lr, tpr_lr)

fpr_gnb, tpr_gnb, _ = roc_curve(y_test_encoded, y_scores_gnb)
roc_auc_gnb = auc(fpr_gnb, tpr_gnb)

fpr_knn, tpr_knn, _ = roc_curve(y_test_encoded, y_scores_knn)
roc_auc_knn = auc(fpr_knn, tpr_knn)

fpr_svc, tpr_svc, _ = roc_curve(y_test_encoded, y_scores_svc)
roc_auc_svc = auc(fpr_svc, tpr_svc)

fpr_dtc, tpr_dtc, _ = roc_curve(y_test_encoded, y_scores_dtc)
roc_auc_dtc = auc(fpr_dtc, tpr_dtc)

# ROC eğrilerini çizme
plt.figure(figsize=(10, 8))
plt.plot(fpr_lr, tpr_lr, color='darkorange', lw=2, label='LR ROC curve (area = {:.2f})'.format(roc_auc_lr))
plt.plot(fpr_gnb, tpr_gnb, color='green', lw=2, label='GNB ROC curve (area = {:.2f})'.format(roc_auc_gnb))
plt.plot(fpr_knn, tpr_knn, color='blue', lw=2, label='KNN ROC curve (area = {:.2f})'.format(roc_auc_knn))
plt.plot(fpr_svc, tpr_svc, color='red', lw=2, label='SVC ROC curve (area = {:.2f})'.format(roc_auc_svc))
plt.plot(fpr_dtc, tpr_dtc, color='purple', lw=2, label='DTC ROC curve (area = {:.2f})'.format(roc_auc_dtc))

plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curves for LFI')
plt.legend(loc='lower right')
plt.show()

# AUC değerlerini yazdırma
print("LR AUC:", roc_auc_lr)
print("GNB AUC:", roc_auc_gnb)
print("KNN AUC:", roc_auc_knn)
print("SVC AUC:", roc_auc_svc)
print("DTC AUC:", roc_auc_dtc)