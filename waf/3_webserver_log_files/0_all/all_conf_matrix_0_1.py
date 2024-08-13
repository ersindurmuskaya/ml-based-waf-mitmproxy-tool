# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 11:55:18 2024

@author: ersin
"""
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

# Excel dosyanızı okuyun
df = pd.read_excel('C:/Users/ersin/Desktop/webserver_log_files/0_all/all_bad_good_0_1_real.xlsx')  # dosya_adı.xlsx dosyanızın adını doğru şekilde girin

# 'pred' sütununu y_pred'e, 'real' sütununu y_test'e atayın
y_pred = df['pred']
y_test = df['real']

# Confusion Matrix'i hesaplayın
cm = confusion_matrix(y_test, y_pred)

# Confusion Matrix'i görselleştirin
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()

# Figure'ı JPG olarak kaydet
plt.savefig('confusion_matrix.jpg')

plt.show()


from sklearn.metrics import precision_score, recall_score, f1_score,accuracy_score

# Accuracy hesapla
accuracy = accuracy_score(y_test, y_pred)

# Precision hesapla
precision = precision_score(y_test, y_pred, pos_label="[0]")

# Recall hesapla
recall = recall_score(y_test, y_pred, pos_label="[0]")

# F1-score hesapla
f1 = f1_score(y_test, y_pred, pos_label="[0]")

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1-score:", f1)