#from rawweb import RawWeb
from xml.etree import ElementTree as ET
import urllib
import base64
from HTMLParser import HTMLParser
import csv
#from urllib.parse import unquote
log_path = 'all_good.log'
output_csv_log='all_good.csv'
class_flag = "good"
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
			raw_req = urllib.unquote(raw_req).decode('latin1')
			raw_resp = reqs.find('response').text
			result[raw_req] = raw_resp
		return result
	def parseRawHTTPReq (self,rawreq) :
		try:
			raw = rawreq.decode('latin1')
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

badwords = ['type', 'necho','usr', 'bin', 'whoami', 'ipconfig', 
			'system', 'cat', 'phpinfo', 'exec', 'phpversion', 'pwd',
			'eval', 'echo', 'sleep', 'curl', 'wget', 'which', 'netstat', 
			'dir', 'uname', 'nid', 'perl', 'systeminfo', 'reg', 'print', 
			'netsh', 'hexdec', 'dechex', 'sysinfo', 'net', 'cmd', 'SERVER', 'route', 'ping', 'ifconfig']
def ExtractFeatures(method,path_enc,body_enc,headers):
	badwords_count = 0
	path=urllib.unquote_plus(path_enc)
	body=urllib.unquote (body_enc)
	#double_q			=	path.count("\"") + body.count("\"")
	dashes				=	path.count ("--") + body.count("--")
	#braces				=	path.count("(") + body.count("(")
	#backslash			=	path.count("\\") + body.count("\\")
	andsign				=	path.count("&&") + body.count("&&")
	#semicolon			=	path.count(";") + body.count(";")
	dolar				=	path.count("$") + body.count("$")
	orsign				=	path.count("|") + body.count("|")
	#paranthesis			=	path.count("\[") + body.count("\[")
	#backparanthesis	=	path.count("\]") + body.count("\]")
	#curlyparanthesis	=	path.count("\{") + body.count("\{")
	#curlybackparanthesis=	path.count("\}") + body.count("\}")
	lessthan			=	path.count("<") + body.count("<")
	greaterthan			=	path.count(">") + body.count(">")
	exclamation			=	path.count("!") + body.count("!")
	#sharp				=	path.count(" #") + body.count(" #")
	for word in badwords:
		badwords_count += path.count (word) + body.count (word)
	for header in headers:
		#single_q += headers[header].count("'")
		#double_q += headers[header].count("\"")
		#dashes	  += headers(header).count("-")
		#braces	  += headers[header].countr("(")
		badwords_count += headers[header].count(word) + headers[header].count(word) 
	
	return [method,path_enc.encode('latin1').strip(),body_enc.encode('latin1').strip(),dashes,andsign,dolar,orsign,lessthan,greaterthan,exclamation,badwords_count,class_flag] 
	raw_input('>>>') 
#Open the log file 
f = open(output_csv_log, "w") 
c = csv.writer(f) 
c.writerow(["method","path","body","dashes","andsign","dolar","orsign",
			"lessthan","greaterthan","exclamation","badwords","class"]) 
f.close()
lp = LogParse()
result = lp.parse_log(log_path)
f = open(output_csv_log, "ab")
c = csv.writer(f)
h = HTMLParser()
for items in result:
	try:
		raaw = base64.b64decode(items)
		raaw = h.unescape(raaw)
		raaw = urllib.unquote(raaw).decode('latin1', errors='ignore')
	except UnicodeDecodeError as e:
		print(e)
		pass
	headers,method,body,path = lp.parseRawHTTPReq(raaw)
	result = ExtractFeatures(method,path,body,headers)
	c.writerow(result)
f.close()