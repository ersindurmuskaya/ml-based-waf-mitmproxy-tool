# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 21:25:56 2023

@author: ersin
"""
#1.kutuphaneler
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score
import dtreeviz

#2.veri onisleme
#2.1.veri yukleme
veriler = pd.read_csv("C:/Users/ersin/Desktop/makale_sonuc/1-xss/xss_good_bad_all.csv")
#pd.read_csv("veriler.csv")
#test

x = veriler.iloc[:,0:6].values #bağımsız değişkenler
y = veriler.iloc[:,6:].values #bağımlı değişken

#verilerin egitim ve test icin bolunmesi
from sklearn.model_selection import train_test_split

x_train, x_test,y_train,y_test = train_test_split(x,y,test_size=0.33, random_state=42)
'''
#verilerin olceklenmesi
from sklearn.preprocessing import StandardScaler

sc=StandardScaler()

X_train = sc.fit_transform(x_train)
X_test = sc.transform(x_test)
'''
#########################################################################
from sklearn.tree import DecisionTreeClassifier
dtc = DecisionTreeClassifier()

dtc.fit(x_train,y_train)
y_pred_dtc = dtc.predict(x_test)
cm_dtc = confusion_matrix(y_test,y_pred_dtc)
print(cm_dtc)

########################################################################
from sklearn import tree

#text_representation = tree.export_text(dtc)
#print(text_representation)

feature_names = veriler.columns[:6].tolist()  # adjust this to match your column names
class_names = veriler.columns[6:].tolist()  # adjust this to match your column names

  

fig = plt.figure(figsize=(25,20))
_ = tree.plot_tree(dtc, 
                   feature_names=["greaters","less_thans","dashes","hashes","stars","badwords_count"],  
                   class_names=["bad","good"],
                   filled=True)
print(dtc.get_params())
print("Maximum depth:", dtc.tree_.max_depth)



########################################################################

