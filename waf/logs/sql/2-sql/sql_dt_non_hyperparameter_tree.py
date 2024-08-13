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
###############################################################

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import RandomizedSearchCV
from sklearn import tree


#2.veri onisleme
#2.1.veri yukleme
veriler = pd.read_csv("C:/Users/ersin/Desktop/makale_sonuc/2-sql/good_bad_all.csv")
#pd.read_csv("veriler.csv")
#test

x = veriler.iloc[:,0:8].values #bağımsız değişkenler
y = veriler.iloc[:,8:].values #bağımlı değişken

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
dtc = DecisionTreeClassifier()

dtc.fit(X_train,y_train)
y_pred_dtc = dtc.predict(X_test)

cm_dtc = confusion_matrix(y_test,y_pred_dtc)
print('DTC ID3')
print(cm_dtc)
f1_skor_dtc=f1_score(y_test, y_pred_dtc, average='micro')
print(f1_skor_dtc)
feature_names_sql = veriler.iloc[:,0:8].columns
class_names_sql = veriler.iloc[:,8:].columns

#feature_names=["greaters","less_thans","dashes","hashes","stars","badwords_count"]
#class_names=["bad","good"]

fig = plt.figure(figsize=(25,20))
_ = tree.plot_tree(dtc, 
                   feature_names=feature_names_sql ,  
                   class_names=["bad","good"],
                   filled=True)
print(dtc.get_params())
# Ağaçtaki tüm düğümlerin sayısını yazdırma
print("Ağaçtaki tüm düğümlerin sayısı:", dtc.tree_.node_count)

# Ağaçtaki yaprak düğümlerinin sayısını yazdırma
#print("Ağaçtaki yaprak düğümlerinin sayısı:", dtc.tree_.leaf_count)
# Ağaçtaki en derin düğümün derinliğini yazdırma
print("Ağaçtaki en derin düğümün derinliği:", dtc.tree_.max_depth)

print("Number of nodes:", dtc.tree_.node_count)
print("Maximum depth:", dtc.tree_.max_depth)
print("Feature used for splitting at node 0:", dtc.tree_.feature[0])
print("Threshold used for splitting at node 0:", dtc.tree_.threshold[0])
print("Impurity at node 0:", dtc.tree_.impurity[0])
#print("Number of samples at node 0:", dtc.tree_.n_samples[0])
print("Index of left child node for node 0:", dtc.tree_.children_left[0])
print("Index of right child node for node 0:", dtc.tree_.children_right[0])
#print("Index of parent node for node 0:", dtc.tree_.parent[0])
