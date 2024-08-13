# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 21:25:56 2023

@author: ersin
"""
#1.kutuphaneler
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random
from scipy.stats import uniform, poisson
from sklearn.metrics import classification_report
###############################################################

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import GridSearchCV
from sklearn import tree


#2.veri onisleme
#2.1.veri yukleme
veriler = pd.read_csv("C:/Users/ersin/Desktop/makale_sonuc/4-lfi/lfi_all_bad_good2.csv")
#pd.read_csv("veriler.csv")
#test

x = veriler.iloc[:,0:7].values #bağımsız değişkenler
y = veriler.iloc[:,7:].values #bağımlı değişken

#verilerin egitim ve test icin bolunmesi

x_train, x_test,y_train,y_test = train_test_split(x,y,test_size=0.3, random_state=42)

#verilerin olceklenmesi
from sklearn.preprocessing import StandardScaler

sc=StandardScaler()

X_train = sc.fit_transform(x_train)
X_test = sc.transform(x_test)



from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score

######################################################################
dtc = DecisionTreeClassifier(criterion = 'gini', random_state=42)

dtc.fit(X_train,y_train)
y_pred_dtc = dtc.predict(X_test)

cm_dtc = confusion_matrix(y_test,y_pred_dtc)
print('DTC ID3')
print(cm_dtc)
f1_skor_dtc=f1_score(y_test, y_pred_dtc, average='micro')
print(f1_skor_dtc)
#agac grafigi
feature_names_lfi = veriler.iloc[:,0:7].columns
fig1 = plt.figure(figsize=(25,20))
_ = tree.plot_tree(dtc, 
                   feature_names=feature_names_lfi ,  
                   class_names=["0","1"],
                   filled=True)


# Hiperparametrelerin aralığını tanımlama
parametre_dagitimi ={
    "max_depth": range(1, 9),
    "min_samples_split": range(2, 102,10),
    "min_samples_leaf": range(2, 102,5),
}
# RandomizedSearchCV kullanarak optimum hiperparametreleri bulma
model = DecisionTreeClassifier( criterion='entropy')
random_search = RandomizedSearchCV(estimator=model, param_distributions=parametre_dagitimi, 
                                   cv=100, n_iter=10,error_score='raise')
random_search.fit(X_train, y_train)

# En iyi hiperparametreleri ve modeli alma
en_iyi_parametreler = random_search.best_params_
en_iyi_model = random_search.best_estimator_

# En iyi modelin eğitim ve test kümelerindeki performansını değerlendirme
eğitim_skoru = en_iyi_model.score(X_train, y_train)
test_skoru = en_iyi_model.score(X_test, y_test)

print("En iyi parametreler:", en_iyi_parametreler)
print("Eğitim skoru:", eğitim_skoru)
print("Test skoru:", test_skoru)

min_samples_split = en_iyi_parametreler['min_samples_split']
min_samples_leaf = en_iyi_parametreler['min_samples_leaf']
max_depth = en_iyi_parametreler['max_depth']

model = DecisionTreeClassifier(criterion='entropy',min_samples_split=min_samples_split,random_state=42,
                               min_samples_leaf=min_samples_leaf,max_depth=max_depth)
model.fit(X_train, y_train)


feature_names_lfi = veriler.iloc[:,0:7].columns
class_names_lfi = veriler.iloc[:,7:].columns

#feature_names=["greaters","less_thans","dashes","hashes","stars","badwords_count"]
#class_names=["bad","good"]

fig = plt.figure(figsize=(35,20))
_ = tree.plot_tree(en_iyi_model, 
                   feature_names=feature_names_lfi ,  
                   class_names=["0","1"],
                   fontsize=20,
                   filled=True)

en_iyi_model.fit(X_train,y_train)
y_pred_dtc = en_iyi_model.predict(X_test)
f1_skor_dtc=f1_score(y_test, y_pred_dtc, average='micro')
print(f1_skor_dtc)