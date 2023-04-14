import urllib2 as url #python2
#import urllib.request as url #python3
# import numpy as np
import sys

# this is static and is the first part of the Acnet URL
acnet_webString = 'http://www-bd.fnal.gov/cgi-bin/acl.pl?acl=logger_get/start='

# output file name
acnet_results = "/home/daq/2023_04_ETL_ACLGAD/JARVIS/SlowControl/acnet_buffer.txt"

# Function to construct URL and write results to text file
def get_acnet_data(T1, T2, device):
# build URL to be queried and decode data to human readable content
	URL = acnet_webString+str(T1)+'/end='+str(T2)+'/node=Swyd'+'+'+str(device)
	#print(URL)
	response = url.urlopen(URL).read()
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
	return buff

def return_acnet_data(): 
	## define counters

	counts1 = 'F:MW1SEM'
	counts2 = 'F:MT6SC2'
	counts3 = 'F:MT6SC1'
	MT61AH = 'E:1AH'
	MT61AV = 'E:1AV'

	### For first bias config, (387,388,389)
	startTime = '12-apr-2023-00:00:00' #38372
	endTime = '30-apr-2023-00:00:00' #39422

	counts1_buff = get_acnet_data(startTime, endTime, counts1)
	counts2_buff = get_acnet_data(startTime, endTime, counts2)
	counts3_buff = get_acnet_data(startTime, endTime, counts3)
	MT61AH_buff  = get_acnet_data(startTime, endTime, MT61AH)
	MT61AV_buff  = get_acnet_data(startTime, endTime, MT61AV)
	buff = "{:.2e}, {:.2e}, {:.2e}, {:.6e}, {:.6e}\n".format(float(counts1_buff), float(counts2_buff), float(counts3_buff),float(MT61AH_buff), float(MT61AV_buff))

	#print("%s from %s to %s in %s:" %(counts2, startTime,endTime,counts1) + "{:.6e}".format(float(counts2_buff)))

	# write acnet data to file
	f = open(acnet_results, "w")
	f.write(buff)
	f.close()
	return buff

if __name__=="__main__":
	buff = return_acnet_data()
	print(buff)
