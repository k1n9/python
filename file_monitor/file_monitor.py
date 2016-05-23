#k1n9
import os
import sys
import time
import hashlib
import threading

files_list = list()
md5_log = {}
ISOTIMEFORMAT = '%Y-%m-%d %X'
flag = 0
threads = 10

def get_files(rootdir):
	files_list = list()

	for parent,dirnames,filenames in os.walk(rootdir):
		for filename in filenames:
			files_list.append(os.path.join(parent,filename))

	return files_list

def get_file_md5(filename):
	f = open(filename,'r')
	c = f.read()
	f.close()

	return hashlib.md5(c).hexdigest()

def get_log():
	md5_log = {}

	for f in files_list:
		md5_log[f] = get_file_md5(f)

	return md5_log

def output(keyword,filename):
	print '[%s] %s %s\n' % (keyword,filename,time.strftime(ISOTIMEFORMAT,time.localtime( time.time())))

def check_file(c_files_list,st,en):
	global flag

	for i in range(st,en):
		filename = c_files_list[i]
		if filename not in files_list:
			flag = 1
			output('Create',filename)
		else:
			f = open(filename,'r')
			c = f.read()
			f.close()
			if hashlib.md5(c).hexdigest() != md5_log[filename]:
				flag = 1
				output('Modify',filename)

def init(rootdir):
	global files_list
	global md5_log

	files_list = []
	md5_log = {}
	files_list = get_files(rootdir)
	md5_log = get_log()
	print 'Init complete!\n'

if __name__=="__main__":
	temp = list()

	rootdir = sys.argv[1]
	init(rootdir)

	while 1:
		flag = 0
		temp = []
		ts = []
		temp = get_files(rootdir)
		list_len = len(temp)
		num = list_len / threads

		if not num:
			ts.append(threading.Thread(target=check_file,args=(temp,0,list_len)))
		else:
			st = 0
			while list_len - st >= num:
				en = st + num
				ts.append(threading.Thread(target=check_file,args=(temp,st,en)))
				st = en
			ts.append(threading.Thread(target=check_file,args=(temp,st,list_len)))
		for t in ts:
			t.start()
		for t in ts:
			t.join()

		for filename in files_list:
			if filename not in temp:
				flag = 1
				output('Delete',filename)
		if flag:
			print '---------------------Warning---------------------'
			#c = raw_input("Continue? [Y/n]:")
			#if c == 'n':
			#	exit()
			#else:
			#	init(rootdir)	
		time.sleep(5) 
