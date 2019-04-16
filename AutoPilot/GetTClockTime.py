import os
import time

while True:
	os.system(':> TClock') #Emptying the TClock File 
	os.system('curl https://www-ad.fnal.gov/notifyservlet/www?action=raw | grep -Eoi "SC time</a> \=(.+)/" | cut -c"15-19" >> TClock')
	time.sleep(600)