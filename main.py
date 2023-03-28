import requests as r
from getpass import getpass

# subvert ssl errors: thanks to https://stackoverflow.com/a/41041028 [user: Larry Cai, edited: Qlimax]
r.packages.urllib3.disable_warnings ()
r.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'

try:
	r.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
except AttributeError:
	pass
# end of external code

PASS 		 = 1
FAIL_CONNECT = -1
FAIL_AUTH 	 = -2
FAIL_REQUEST = -3

# approval method
def approve (username, password):
	S = r.Session ()
	try:
		# login
		x = S.post ('https://netaccess.iitm.ac.in/account/login',
	      			data={'userLogin':username,'userPassword':password,'submit':''},
					verify=False)

		# check login
		if str (x.content).find ('Authorized') == -1:
			# failed
			return FAIL_AUTH
	
		# approve (1 day)
		y = S.post ('https://netaccess.iitm.ac.in/account/approve',
	      			data={'duration':'2','approveBtn':''},
					verify=False)

		# check approval
		if str (y.content).find ('Authorized') == -1:
			return FAIL_AUTH

		return PASS
	except r.ConnectionError:
		return FAIL_REQUEST


# does cred file exist?
import os, json
MYPATH = os.path.dirname (__file__)
cred_file = '/cred.json'
FILEPATH = MYPATH + cred_file

cred = {}

try:
	# read cred file
	with open (FILEPATH, 'r') as inf:
		cred = json.load (inf)
except FileNotFoundError:
	# create cred file
	print ('Enter your LDAP username: ', end='')
	username = input ()
	password = getpass ("Enter your LDAP password: ")

	cred = {'username':username, 'password':password}
	
	with open (FILEPATH, 'w') as outf:
		json.dump (cred, outf)

	print (f"Saved credentials (as {FILEPATH}).")

# begin auth
print ('Authorizing... ', end = '', flush=True)

v = approve (cred['username'], cred['password'])

# feedback
if v == PASS:
	print ('Done.')
elif v == FAIL_CONNECT:
	print ('Failed.')
	print ('> Request failed. Are you connected?')
elif v == FAIL_AUTH:
	# remove cred file on auth failure
	print ('Failed.')
	print ('> Authorization failed. Removing stored credentials. Please run again.')
	os.remove (FILEPATH)
elif v == FAIL_REQUEST:
	print ('Failed.')
	print ('> Request failed. Are you connected to IITM Lan?')
