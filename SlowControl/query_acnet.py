import urllib.request
# import numpy as np
import sys

# this is static and is the first part of the Acnet URL
webString = 'http://www-bd.fnal.gov/cgi-bin/acl.pl?acl=logger_get/start='

# output file name
results = "/home/daq/SensorBeam2022/JARVIS/SlowControl/acnet_buffer.txt"

# Function to construct URL and write results to text file
def get_acnet_data(T1, T2, device):
# build URL to be queried and decode data to human readable content
	URL = webString+str(T1)+'/end='+str(T2)+'/node=Swyd'+'+'+str(device)
	#print(URL)
	response = urllib.request.urlopen(URL).read()
	decoded_response = response.decode()
	yesData = not "No values" in decoded_response
	# print(decoded_response)
	total = 0
	buff = '-9998'
	if yesData:
		buff = decoded_response.split("\n")[-2]
		buff = buff.replace("+","")
		if len(buff.split("   ")) >1:
			buff = buff.split("   ")[1]

	# write acnet data to file
	f = open(results, "w")
	f.write(buff)
	f.close()
	return buff

## define counters
counts1 = 'F:MW1SEM'
counts2 = 'F:MT6SC2'

# set time frame with these two lines

### For first bias config, (387,388,389)
startTime = '3-mar-2022-00:00:00' #38372
endTime = '3-apr-2022-18:15:00' #39422

total_sc1_day1 = get_acnet_data(startTime, endTime, counts2)
print("%s from %s to %s in %s:" %(counts2, startTime,endTime,counts1), "{:.2e}".format(float(total_sc1_day1)))
