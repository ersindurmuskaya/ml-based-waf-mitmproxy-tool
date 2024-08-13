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
from sklearn.metrics import classification_report

###############################################################

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn import tree


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
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score

######################################################################
from sklearn.tree import DecisionTreeClassifier
dtc = DecisionTreeClassifier(criterion = 'entropy', random_state=42)

dtc.fit(X_train,y_train)
y_pred_dtc = dtc.predict(X_test)

cm_dtc = confusion_matrix(y_test,y_pred_dtc)
print('DTC ID3')
print(cm_dtc)
f1_skor_dtc=f1_score(y_test, y_pred_dtc, average='micro')
print(f1_skor_dtc)
'''
# Hiperparametrelerin aralığını tanımlama
parametre_dagitimi ={
    "criterion": ["gini", "entropy"],
    "max_depth": range(1, 21),
    "min_samples_split": range(2, 11),
    "min_samples_leaf": range(1, 5),
    "splitter": ["best", "random"],
    "min_weight_fraction_leaf": np.linspace(0.0, 0.5, 10),
    "max_features": ["log2","sqrt", None],
    "random_state": [None, 42],
    "min_impurity_decrease": np.linspace(0.0, 0.1, 10),
    "class_weight": ["balanced", None],
}

# RandomizedSearchCV kullanarak optimum hiperparametreleri bulma
model = DecisionTreeClassifier()
random_search = RandomizedSearchCV(estimator=model, param_distributions=parametre_dagitimi, 
                                   cv=10, n_iter=100,error_score='raise')
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
'''
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

feature_names_xss = veriler.iloc[:,0:6].columns
class_names_xss = veriler.iloc[:,6:].columns

#feature_names=["greaters","less_thans","dashes","hashes","stars","badwords_count"]
#class_names=["bad","good"]


fig = plt.figure(figsize=(35,20))
_ = tree.plot_tree(en_iyi_model, 
                   feature_names=feature_names_xss,  
                   class_names=["bad","good"],
                   fontsize=20,
                   filled=True)


en_iyi_model.fit(X_train,y_train)
y_pred_dtc = en_iyi_model.predict(X_test)
f1_skor_dtc=f1_score(y_test, y_pred_dtc, average='micro')
print(f1_skor_dtc)

