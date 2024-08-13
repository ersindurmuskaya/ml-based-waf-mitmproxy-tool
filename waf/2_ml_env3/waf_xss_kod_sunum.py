# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 16:21:12 2023

@author: ersin
"""
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
output_csv_path_content_host = 'kaggle_xss_path_content_host.csv'
# we can change badwords list.It depends on website structure and vulnerability.
badwords = ['script','src', 'alert', 'onload', 'string', 
			'fromcharcode', 'meta', 'input', 'button', 'action', 
			'iframe', 'javascript', 'onmouseover', 'document.', 
			'onerror', 'confirm', 'formaction', 'NewLine', 'Tab', 'svg', 
			'onload', 'onafterprint', 'onbeforeprint', 'onbeforeunload', 
			'onhashchange', 'onmessage', 'ononline', 'onoffline', 
			'onpagehide', 'onpageshow', 'onpopstate', 'onresize', 
			'onstorage', 'onunload', 'onblur', 'onchange', 'oncontextmenu',
			'oninput', 'oninvalid', 'onreset', 'onsearch', 'onselect', 
			'onsubmit', 'onkeydown', 'onkeypress', 'onkeyup', 'onclick', 
			'ondblclick', 'onmousedown', 'onmousemove', 'onmouseout', 
			'onmouseover', 'onmouseup', 'onmousewheel', 'onwheel', 'ondrag', 
			'ondragend', 'ondragenter', 'ondragleave', 'ondragover', 'ondragstart',
			'ondrop', 'onscroll', 'oncopy', 'oncut', 'onpaste', 'onabort', 
			'oncanplay', 'oncanplaythrough', 'oncuechange', 'ondurationchange', 
			'onemptied', 'onended', 'onerror', 'onloadeddata', 'onloadedmetadata', 
			'onloadstart', 'onpause', 'onplay', 'onplaying', 'onprogress', 
			'onratechange', 'onseeked', 'onseeking', 'onstalled', 'onsuspend', 
			'ontimeupdate', 'onvolumechange', 'onwaiting', 'onshow', 'ontoggle', 
			'href', 'prompt', 'formaction', 
			'body', 'onLoad', 'frameset ', 'applet', 'BASE', 'import', 'namespace']
veriler = pd.read_csv('xss_all.csv')
# xss_all.csv : firstly we read http request and parsing it as path,body,header,method vs. by using burpsuite from another programme
#				secondly we count badwords and vulnerable signs which we already defined 
#				lastly we save as a csv file including counting element 
x = veriler.iloc[:,0:6].values 
y = veriler.iloc[:,6:].values 


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
f.close()

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
	#live_data = ExtractFeatures(path,body)	#path ve body den gelenler: request_content;request_path
	host_site=flow.request.host
	
	if host_site=="demo.testfire.net": #if host_site=='192.168.174.135' or  'localhost': ------if host_site=="juice-shop.herokuapp.com" or '46.137.15.86':
		print('#################################istek baslangici#########################################')
		print(f"HTTP Request HOST: {flow.request.host}")
		#print(f'\033[93mHTTP Request HOST: {flow.request.host}\033[0m')
		print(f"HTTP Request Content: {flow.request.text}")
		print(f"HTTP Request Path: {flow.request.path}")
		print(f"HTTP Request Headers: {flow.request.headers}")
		print(f"HTTP Request Message.raw_content: {flow.request.content}")
		#path2=request_content #mitmproxy de content olan
		path2=request_path #girdilerin nerede olduguna gore degisir ayni anda hem request_content hemde request_path okunabilir.
		#print("path2 : : : :" , path2)
		#path2_list= path2.tolist()
		path2_list= path2
		raaw_path=path2_list
		#raaw_body=body_list[i]
		raaw_path=urllib.parse.unquote_plus(raaw_path)
		#sign and badwords list must be chosen to depend on web site where waf is running
		#for different website structure(like different database;different content) which we knew beforehand  
		
		greaters=raaw_path.count(">")
		less_thans=raaw_path.count("<")
		dashes=raaw_path.count ("--")
		hashes=raaw_path.count("#") 
		stars=raaw_path.count("*")
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
		data = {'badwords_count': [badwords_list],
				'greaters': [greaters],
				'less_thans': [less_thans],
				'dashes': [dashes],
				'hashes': [hashes],
				'stars': [stars]}

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