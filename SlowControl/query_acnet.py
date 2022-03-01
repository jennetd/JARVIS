import urllib.request
# import numpy as np
import sys

# this is static and is the first part of the Acnet URL
webString = 'http://www-bd.fnal.gov/cgi-bin/acl.pl?acl=logger_get/start='

# output file name
results = "acnet_buffer.txt"

# Function to construct URL and write results to text file
def get_acnet_data(T1, T2, device):
# build URL to be queried and decode data to human readable content
	URL = webString+str(T1)+'/end='+str(T2)+'/node=Swyd'+'+'+str(device)
	response = urllib.request.urlopen(URL).read()
	decoded_response = response.decode()
	#print(decoded_response)
	total =0
	for line in decoded_response.split("\n"):
		#print(line.split("   "))
		#print(line)
		line.replace("+","")
		if len(line.split("   ")) >1:
			buff = line.split("   ")[1]
		# 	print(line.split("   ")[1])
		# 	total += int(line.split("   ")[1].replace("+",""))
	# write acnet data to file
	f = open(results, "w")
	f.write(buff)
	f.close()
	return total

## define counters
counts1 = 'F:MW1SEM'
#counts2 = 'F:MT6SC2'

# set time frame with these two lines

### For first bias config, (387,388,389)
startTime = '2-dec-2021-02:15:00' #38372
endTime = '12-dec-2021-03:15:00' #39422

total_sc1_day1 = get_acnet_data(startTime, endTime, counts1)
#print("MW1SEM from %s to %s in %s:" %(startTime,endTime,counts1), "{:.2e}".format(total_sc1_day1))

