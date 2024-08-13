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
'''
#verilerin olceklenmesi
from sklearn.preprocessing import StandardScaler

sc=StandardScaler()

X_train = sc.fit_transform(x_train)
X_test = sc.transform(x_test)
################################################
'''
from sklearn.preprocessing import MinMaxScaler
mmscaler = MinMaxScaler()
X_train = mmscaler.fit_transform(x_train)
X_test = mmscaler.transform(x_test)
#########################################################################

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.naive_bayes import BernoulliNB

ber_nb = BernoulliNB()
ber_nb.fit(X_train, y_train)

y_pred_gnb = ber_nb.predict(X_test)

cm_ber_nb = confusion_matrix(y_test,y_pred_gnb)
print('Ber-NB')
print(cm_ber_nb)
f1_skor_ber_nb=f1_score(y_test, y_pred_gnb, average='macro')
accuracy_score_ber_nb=accuracy_score(y_test,y_pred_gnb)
precision_score_ber_nb=precision_score(y_test,y_pred_gnb, average='macro')
recall_score_ber_nb=recall_score(y_test,y_pred_gnb, average='macro')
print('f1_skor_ber_nb: ',f1_skor_ber_nb)
print('accuracy_score_ber_nb: ',accuracy_score_ber_nb)
print('precision_score_ber_nb: ',precision_score_ber_nb)
print('recall_score_ber_nb: ',recall_score_ber_nb)
#########################################################################


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