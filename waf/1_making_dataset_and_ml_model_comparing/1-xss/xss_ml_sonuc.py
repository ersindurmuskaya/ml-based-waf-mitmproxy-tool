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
veriler = pd.read_csv("C:/Users/ersin/Desktop/makale_sonuc/1-xss/xss_good_bad_all.csv")
#pd.read_csv("veriler.csv")
#test

x = veriler.iloc[:,0:6].values #bağımsız değişkenler
y = veriler.iloc[:,6:].values #bağımlı değişken

#verilerin egitim ve test icin bolunmesi
from sklearn.model_selection import train_test_split

x_train, x_test,y_train,y_test = train_test_split(x,y,test_size=0.33, random_state=0)

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
dtc = DecisionTreeClassifier(criterion = 'entropy', random_state=42)

dtc.fit(X_train,y_train)
y_pred_dtc = dtc.predict(X_test)

cm_dtc = confusion_matrix(y_test,y_pred_dtc)
print('DTC ID3')
print(cm_dtc)
f1_skor_dtc=f1_score(y_test, y_pred_dtc, average='micro')
print(f1_skor_dtc)
########################################################################
from sklearn.tree import DecisionTreeClassifier
dtc_id = DecisionTreeClassifier(random_state=42)

dtc_id.fit(X_train,y_train)
y_pred_dtc = dtc_id.predict(X_test)

cm_dtc = confusion_matrix(y_test,y_pred_dtc)
print('DTC CART')
print(cm_dtc)
f1_skor_dtc=f1_score(y_test, y_pred_dtc, average='micro')
print(f1_skor_dtc)
