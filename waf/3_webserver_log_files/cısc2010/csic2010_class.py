import pandas as pd

# Load the dataset
veri_seti = pd.read_csv("web_class.csv")

# Kötücül kelime listelerini oluştur
badwords_xss = ['script', 'img','src', 'alert', 'onload', 'string', 
			'fromcharcode', 'meta', 'input', 'type', 'button', 'action', 
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
			'href', 'prompt', 'formaction', 'type', 'audio', 'video', 
			'body', 'image', 'object', 'title', 'onLoad', 'frameset ', 
			'applet', 'math', 'table', 'BASE',
			'classid', 'import', 'namespace']
badwords_sql = ['OR','or', 'AND','and', 'LIKE','like','HAVING','having','where','WHERE',
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
badwords_osc = ['type', 'necho','usr', 'bin', 'whoami', 'ipconfig', 
			'system', 'cat', 'phpinfo', 'exec', 'phpversion', 'pwd',
			'eval', 'echo', 'curl', 'wget', 'which', 'netstat', 
			'dir', 'uname', 'nid', 'perl', 'systeminfo', 'reg', 'print', 
			'netsh', 'hexdec', 'dechex', 'sysinfo', 'net', 'cmd', 'SERVER', 'route', 'ping', 'ifconfig']

badwords_lfi = ['etc','passwd','ZXRj','L3Bhc3N3ZA==','Li4v','shadow', 'aliases',
            'anacrontab', 'apache2','at.allow', 'at.deny','bashrc', 'bootptab',
            'hosts', 'httpd','opt', 'proc','root','usr','local','sbin', 'var',
            'mysql', 'atfp_history','bash','ssh', 'boot.ini',
            'proc', 'C:\\', 'c:\\','localstart.asp','apache','Volumes',
            'C:/', 'desktop.ini','ProgramFiles','xampp', 'bin','WINNT',
            'conf','MySQL','cmdline','database',
            'hostname', 'c:/']

# Create new columns for each vulnerability type
def check_xss(x):
    if isinstance(x, str):
        return any(kelime in x for kelime in badwords_xss)
    return False

veri_seti["xss"] = veri_seti["content"].apply(check_xss)

def check_sql(x):
    if isinstance(x, str):
        return any(kelime in x for kelime in badwords_sql)
    return False

veri_seti["sql"] = veri_seti["content"].apply(check_sql)

def check_osc(x):
    if isinstance(x, str):
        return any(kelime in x for kelime in badwords_osc)
    return False

veri_seti["osc"] = veri_seti["content"].apply(check_osc)

def check_lfi(x):
    if isinstance(x, str):
        return any(kelime in x for kelime in badwords_lfi)
    return False

veri_seti["lfi"] = veri_seti["content"].apply(check_lfi)

# Save the categorized dataset
veri_seti.to_csv("web_class_kategorilenmis.csv", index=False)

print("Veri seti kategorilere ayrıldı ve 'web_class_kategorilenmis.csv' dosyasına kaydedildi.")