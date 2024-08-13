#from rawweb import RawWeb
from xml.etree import ElementTree as ET
import urllib
import base64
import csv
#from urllib.parse import unquote
log_path = 'sql_bad_demotestfire_all.log'
output_csv_log='sql_bad_demotestfire_all.csv'
class_flag = "bad"
class LogParse:
	def __init__(self):
		pass
	def parse_log(self,log_path):
		'''
		This fucntion accepts burp log file path.
		and returns a dict. of request and response
		result = {'GET /page.php...':'200 OK HTTP / 1.1....','":'',..-+e}
		'''
		result = {}
		try:
			with open(log_path): pass
		except IOError:
			print "[+] Error!!! ",log_path,"doesn't exist.."
			exit ()
		try:
			tree = ET.parse(log_path)
		except Exception, e:
			print '[+] Opps..!Please make sure binary data is not present in Log, Like raw image dump.....'
			exit ()
		root = tree.getroot()
		for reqs in root.findall('item'):
			raw_req = reqs.find('request').text
			raw_req = urllib.unquote(raw_req).decode('utf-8')
			raw_resp = reqs.find('response').text
			result[raw_req] = raw_resp
		return result
	def parseRawHTTPReq (self,rawreq) :
		try:
			raw = rawreq.decode('utf-8')
		except Exception,e:
			raw = rawreq
		global headers,method,body,path
		headers = {}
		sp = raw.split('\r\n\r\n',1)
		#print len(sp),sp[1]
		if sp[1] !="":
			head=sp[0]
			body=sp[1]
		else :
			head=sp[0]
			body=""
		cl = head.split('\n',head.count('\n'))
		method = cl[0].split(' ',2)[0]
		path = cl[0].split(' ',2)[1]
		for i in range(1, head.count('\n')+1):
			slicel = cl[i].split(': ',1)
			if slicel[0] != "": #if slice([0]) != "":
				try:
					headers[slicel[0]] = slicel[1]
				except:
					pass
		#print body
		return headers,method,body,path

badwords = ['OR','or', 'AND','and', 'LIKE','like','HAVING','having','where','WHERE',
            'INJECTX','injectx','ORDER','order','ORDER BY','order by','RLIKE','rlike',
            'SELECT','select','CASE','case','WHEN','when','DROP','drop','UNION','union',
            'group by','GROUP BY','LIMIT','limit','system_user','SYSTEM_USER','table_schema',
            'table_name','FROM','from','information_Schema','tables','substring','sysserverse',
            'sysusers','xp_cmdshell','BACKUP','backup','database','create','CREATE','table',
            'insert','INSERT','NULL','null','exec','sp_addlogin','sp_addsrvrolemember','sysadmin',
            'mysql.user','connect','char','waitfor','WAITFOR','DELAY','delay','pg_sleep','hex',
            'delete','DELETE','sleep','SLEEP','nvarchar','benchmark','MD5','PRINT','print',
            'objectclass','sqlvuln','members','load_file','sqlattempt2','nslookup','begin',
            'BEGIN','bfilename','replace','REPLACE','COUNT','count','tabname','syscolumns',
            'SELECTCHAR','CONVERT','CHAR']

def ExtractFeatures(method,path,body,headers):
    badwords_count = 0
    path=urllib.unquote_plus(path)
    path=urllib.unquote_plus(path)################sonradan eklenen
    body=urllib.unquote (body)
    body=urllib.unquote (body)################sonradan eklenen
    #double_q=path.count("\"")+body.count("\"")
    stars=path.count("*")+body.count("*")
    dashes=path.count ("--")+body.count("--")
    or_sign=path.count ("||")+body.count("||")
    and_sign=path.count ("&&")+body.count("&&")
    sub_line=path.count ("__")+body.count("__")
    comment_sign=path.count ("/*")+body.count("/*")
    at_sign=path.count ("@")+body.count("@")
    #greaters=path.count(">")+body.count(">")
    #less_thans=path.count("<")+body.count("<")
    #braces=path.count("(")+body.count("(")
    #spaces=path.count(" ")+body.count(" ")
    #dots=path.count(".")
    #semicolons=path.count(";")+body.count(";")
    #slashes=path.count("/")
    #hashes=path.count("#")+body.count("#")
    for word in badwords:
        badwords_count += path.count(word)+body.count(word)
	for header in headers:
		#single_q += headers[header].count("'")
		#double_q += headers[header].count("\"")
		#dashes   += headers(header).count("-")
		#braces   += headers[header].countr("(")
		badwords_count += headers[header].count(word) + headers[header].count(word) 
	
	return [stars,dashes,or_sign,and_sign,sub_line,comment_sign,at_sign,badwords_count,class_flag] 
	raw_input('>>>') 
#Open the log file 
f = open(output_csv_log, "w") 
c = csv.writer(f) 
c.writerow(['stars','dashes','or_sign','and_sign','sub_line','comment_sign','at_sign','badwords_count',"class_flag"]) 
f.close()
lp = LogParse()
result = lp.parse_log(log_path)
f = open(output_csv_log, "ab")
c = csv.writer(f)
for items in result:
	raaw= base64.b64decode(items)
	raaw = urllib.unquote(raaw).decode('utf-8',errors='ignore')#bad requestler icin url decoding yap,good requestlerde kullanma... bu satir orjinal kodda yok.
	headers,method,body,path = lp.parseRawHTTPReq(raaw)
	result = ExtractFeatures(method,path,body,headers)
	c.writerow(result)
f.close()