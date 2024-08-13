# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 16:21:12 2023

@author: ersin
"""
#1.kutuphaneler
##############M
import csv
import numpy as np
#import scapy.all as scapy
import urllib.parse
import urllib
#from scapy.layers import http
import urllib
from urllib.parse import quote
from urllib.parse import unquote
#from pycaret.clustering import *
import pandas as pd
#import statsmodels.api as sm
#import matplotlib.pyplot as plt


from mitmproxy import http
from urllib.parse import unquote

log_path='XSS_dataset.csv'
output_csv_sayma='kaggle_xss.csv'
class_flag = "bad"
output_csv_path_content_host = 'osc__bad_webserver_log_file.csv'

badwords = ['type', 'necho','usr', 'bin', 'whoami', 'ipconfig', 
			'system', 'cat', 'phpinfo', 'exec', 'phpversion', 'pwd',
			'eval', 'echo', 'sleep', 'curl', 'wget', 'which', 'netstat', 
			'dir', 'uname', 'nid', 'perl', 'systeminfo', 'reg', 'print', 
			'netsh', 'hexdec', 'dechex', 'sysinfo', 'net', 'cmd', 'SERVER',
			'route', 'ping', 'ifconfig','script','passwd','bash']
veriler = pd.read_csv('osc_all.csv')

x = veriler.iloc[:,0:8].values #bağımsız değişkenler
y = veriler.iloc[:,8:].values #bağımlı değişken -classes class_req


'''path = veriler.iloc[:,0]
path_list= path.tolist()

#body = veriler.iloc[:,1]
#body_list = body.tolist()

class_req=veriler.iloc[:,1]
'''



f = open(output_csv_sayma, "wb") 
c = csv.writer(f) 
#c.writerow(['double_q'])
#c.writerow(['double_q','greaters','less_thans','dashes','braces',
#		   'semicolons','hashes','badwords_count',"class_flag"]) 
f.close()

f = open(output_csv_sayma, "ab")
c = csv.writer(f)
'''
badwords_list  =[0]*len(path_list)
#stars	   =[0]*len(path_list)
hashes	  =[0]*len(path_list)
semicolons=[0]*len(path_list)
#spaces	   =[0]*len(path_list)
braces	  =[0]*len(path_list)
dashes	  =[0]*len(path_list)
less_thans=[0]*len(path_list)
greaters  =[0]*len(path_list)
double_q  =[0]*len(path_list)
items=range(len(path_list))
'''
'''
for i in items:
	raaw_path=path_list[i]
	#raaw_body=body_list[i]
	raaw_path=urllib.parse.unquote_plus(raaw_path)
	#raaw_body=urllib.parse.unquote_plus(raaw_body)
	#double_q[i]  =raaw_path.count("\"")+raaw_body.count("\"")
	double_q[i]	 =raaw_path.count("\"")
	greaters[i]	 =raaw_path.count(">")
	less_thans[i]=raaw_path.count("<")
	dashes[i]	 =raaw_path.count("--")
	braces[i]	 =raaw_path.count("(")
	#spaces[i]	  =raaw_path.count(" ")+raaw_body.count(" ")
	semicolons[i]=raaw_path.count(";")
	hashes[i]	 =raaw_path.count("#")
	#stars[i]	  =raaw_path.count("*")+raaw_body.count("*")
	
	
	#headers,method,body,path = parseRawHTTPReq(raaw)
	#result = ExtractFeatures(method,path,body,headers)
	#c.writerow([int(double_q)])
for i in items:
	raaw_path=path_list[i]
	#raaw_body=body_list[i]
	raaw_path=urllib.parse.unquote_plus(raaw_path)
	#raaw_body=urllib.parse.unquote_plus(raaw_body)
	badwords_count = 0
	for word in badwords:
		#badwords_count += raaw_path.count(word)+raaw_body.count(word)
		badwords_count += raaw_path.count(word)
	badwords_list[i]=badwords_count
'''
f.close()


'''
df = pd.DataFrame(list(zip(badwords_list,hashes,semicolons,
						   braces,dashes,less_thans,greaters,double_q)),
			   columns =['badwords_list','hashes','semicolons',
						 'braces','dashes','less_thans','greaters',
						 'double_q'])
############ df im diğer koddaki result olarak 
df_2=df
'''

'''
import statsmodels.api as sm
X=np.append(arr=np.ones((len(path_list),1)).astype(int), values=df_2,axis=1)
X1=df_2.iloc[:,[0,1,2,3,4,5,6]].values
X1=np.array(X1,dtype=float)
model=sm.OLS(class_req,X1).fit()
#print(model.summary())
#################### ###################### ####################### ###########
'''
'''
x=df
y=class_req
#x = veriler.iloc[:,0:10].values #bağımsız değişkenler
#y = veriler.iloc[:,10:].values #bağımlı değişken -classes
'''

#verilerin egitim ve test icin bolunmesi
from sklearn.model_selection import train_test_split

x_train, x_test,y_train,y_test = train_test_split(x,y,test_size=0.33, random_state=0)

#verilerin olceklenmesi
from sklearn.preprocessing import StandardScaler

sc=StandardScaler()

X_train = sc.fit_transform(x_train)
X_test = sc.transform(x_test)

#CONFUSİON MATRİX
from sklearn.metrics import confusion_matrix

#random_forest
from sklearn.ensemble import RandomForestClassifier
rfc = RandomForestClassifier(n_estimators=3, criterion = 'entropy')
rfc.fit(X_train,y_train)

y_pred = rfc.predict(X_test)

cm = confusion_matrix(y_test,y_pred)
#print('rf')
#print(cm)


def request(flow: http.HTTPFlow):
	request_content = unquote(flow.request.text)
	request_path = unquote(flow.request.path)
	# HTTP Request bilgilerini ekrana yazdır
	#print(f"HTTP Request Path: {flow.request.path}")
	#print(f"HTTP Request Method: {flow.request.method}")
	#print(f"HTTP Request Headers: {flow.request.headers}")
	#print(f"HTTP Request HOST: {flow.request.host}")
	#print(f"HTTP Request Content: {flow.request.text}")
	#live_data = ExtractFeatures(path,body)	 path ve body den gelenler: request_content;request_path
	host_site=flow.request.host
	
	if host_site=="demo.testfire.net": #if host_site=='192.168.174.135' or  'localhost': 
		print('#################################istek baslangici#########################################')
		print(f"HTTP Request HOST: {flow.request.host}")
		print(f'\033[93mHTTP Request HOST: {flow.request.host}\033[0m')
		print(f"HTTP Request Content: {flow.request.text}")
		print(f"HTTP Request Path: {flow.request.path}")
		print(f"HTTP Request Headers: {flow.request.headers}")
		print(f"HTTP Request Message.raw_content: {flow.request.content}")
		#path2=request_content #mitmproxy de content olan
		path2=request_path
		#print("path2 : : : :" , path2)
		#path2_list= path2.tolist()
		path2_list= path2
		raaw_path=path2_list
		#raaw_body=body_list[i]
		raaw_path=urllib.parse.unquote_plus(raaw_path)
		#raaw_body=urllib.parse.unquote_plus(raaw_body)
		#double_q[i]  =raaw_path.count("\"")+raaw_body.count("\"")
		
		#sign1=path.count ("../") + body.count("../")
		#sign2=path.count ("..\\") + body.count("..\\")
		#sign3=path.count (".\\.") + body.count(".\\.")
		#sign4=path.count ("..\\..") + body.count("..\\..")
		#sign5=path.count ("....\\") + body.count("....\\")
		#sign6=path.count ("..../") + body.count("..../")
		
		dashes				=	raaw_path.count ("--")
		andsign				=	raaw_path.count("&&")
		dolar				=	raaw_path.count("$")
		orsign				=	raaw_path.count("|")
		lessthan			=	raaw_path.count("<")
		greaterthan			=	raaw_path.count(">")
		exclamation			=	raaw_path.count("!")
		
				
		#double_q	 =raaw_path.count("\"")
		#greaters	 =raaw_path.count(">")
		#less_thans	 =raaw_path.count("<")
		#dashes		 =raaw_path.count("--")
		#braces		 =raaw_path.count("(")
		#spaces[i]	  =raaw_path.count(" ")+raaw_body.count(" ")
		#semicolons	 =raaw_path.count(";")
		#hashes		 =raaw_path.count("#")
		
		# badwords count
		raaw_path=path2_list
		#raaw_body=body_list[i]
		raaw_path=urllib.parse.unquote_plus(raaw_path)
		#raaw_body=urllib.parse.unquote_plus(raaw_body)
		badwords_count = 0
		for word in badwords:
			#badwords_count += raaw_path.count(word)+raaw_body.count(word)
			badwords_count += raaw_path.count(word)
		badwords_list=badwords_count
		'''
		print("bodwords için type : : :" , type(badwords_list), "içerik :::: ", badwords_list)
		print("hashes için type : : :" , type(hashes), "içerik :::: ", hashes)
		df22 = pd.DataFrame(list(zip(badwords_list,hashes,semicolons,
								   braces,dashes,less_thans,greaters,double_q)),
					   columns =['badwords_list','hashes','semicolons',
								 'braces','dashes','less_thans','greaters',
								 'double_q'])
		'''
		data = {'badwords': [badwords_list],
			'dashes': [dashes],
			'andsign': [andsign],
			'dolar': [dolar],
			'orsign': [orsign],
			'lessthan': [lessthan],
			'greaterthan': [greaterthan],
			'exclamation': [exclamation]}

		df22 = pd.DataFrame(data)
		live_data=df22
		live_data= live_data.iloc[:,:].values
		live_data = sc.transform(live_data)
		
		print(df22)
		print(live_data)
		result= rfc.predict(live_data)
		print("machine learning result :::::::::::",result)
		#class_req2=?  belli degil daha ml soyleyecek 
		
		#kotucul isteklerde result=1 oluyor. 
		if result=='bad':
			print("request_path_renkli=",path2)
			print("Script içeren istek engellendi.")
			flow.response = http.Response.make(403, b"Forbidden")  # 403 Forbidden yanıtı gönder
		
		
		#print(result)
		print('#################################istek sonu#########################################')
		
		# CSV dosyasına ekleme
		with open(output_csv_path_content_host, 'a', newline='') as csvfile:
			fieldnames = ['path', 'content', 'host','class_flag']
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

			# Dosya daha önce boşsa header'ları yaz
			if csvfile.tell() == 0:
				writer.writeheader()

			# Verileri CSV dosyasına ekle
			writer.writerow({
				'path': request_path,
				'content': flow.request.text,
				'host': flow.request.host,
				'class_flag':result
			})
	return


def response(flow: http.HTTPFlow):
	# Eğer HTTP yanıtı hakkında bilgi almak isterseniz burada işlemler yapabilirsiniz
	pass

if __name__ == "__main__":
	from mitmproxy.tools.main import mitmdump
	mitmdump(['-s', __file__])