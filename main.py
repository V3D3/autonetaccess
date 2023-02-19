import requests as r
import urllib3

# subvert ssl errors: thanks to https://stackoverflow.com/a/41041028 [user: Larry Cai, edited: Qlimax]
r.packages.urllib3.disable_warnings ()
r.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

try:
	r.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
	pass
# end of external code

PASS = 1
FAIL_AUTH = -1
FAIL_CONNECT = -2

# approval method
def approve (username, password):
	S = r.Session ()
	try:
		# login
		x = S.post ('https://netaccess.iitm.ac.in/account/login', data={'userLogin':username,'userPassword':password,'submit':''}, verify=False)

		# check login
		if (str (x.content).find ('Authorized') == -1):
			# failed
			return FAIL_AUTH
	
		# approve (1 day)
		y = S.post ('https://netaccess.iitm.ac.in/account/approve', data={'duration':'2','approveBtn':''}, verify=False)

		# check approval
		if (str (y.content).find ('Authorized') == -1):
			return FAIL_AUTH

		return PASS
	except ConnectionError:
		return FAIL_CONNECT


# does cred file exist?
import os, sys, json
MYPATH = os.path.realpath (sys.argv [0])
MYPATH = MYPATH [0 : MYPATH.rfind ('/')]

if not os.path.isfile (MYPATH + '/cred.json'):
	# create cred file
	print ('Enter your LDAP username: ', end='')
	username = input ()
	print ('Enter your LDAP password: ', end='')
	password = input ()

	cred = {'username':username, 'password':password}
	
	with open (MYPATH + '/cred.json', 'w') as outf:
		json.dump (cred, outf)

	print (f"Saved credentials (as {MYPATH + '/cred.json'}).")

# read cred file
cred = {}
with open (MYPATH + '/cred.json', 'r') as inf:
	cred = json.load (inf)

# begin auth
print ('Authorizing... ', end = '', flush=True)

v = approve (cred ['username'], cred ['password'])

# feedback
if (v == PASS):
	print ('Done.')
elif (v == FAIL_AUTH):
	# remove cred file on auth failure
	print ('Failed.')
	print ('> Authorization failed. Removing stored credentials. Please run again.')
	os.remove (MYPATH + '/cred.json')
elif (v == FAIL_CONNECT):
	print ('Failed.')
	print ('> Request failed. Are you connected?')
