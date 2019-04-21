import time
import numpy as np
from numpy import loadtxt
import getpass
import os
import subprocess as sp
import socket
import sys
import glob
from bisect import bisect_left


labview_unsync_base_path = '/home/daq/2019_04_April_CMSTiming/LabviewData/LabviewUnsyncData/'

def greatest_number_less_than_value(seq,value):
    if bisect_left(seq,value)>0:
        return seq[bisect_left(seq,value)-1]
    else: return seq[0]

def GetEnvMeas(timestamp):
                                                                                                                                                                                                                                
    LabviewFlag = False

    labview_file_list = sorted([float(x.split("lab_meas_unsync_")[-1].split(".txt")[0]) for x in glob.glob(labview_unsync_base_path + "/lab_meas_unsync_*")])
    exact_labview_file = greatest_number_less_than_value(labview_file_list, timestamp)
    index_labview_file = labview_file_list.index(exact_labview_file)

    all_labview_array = np.array([])
    labview_file_name = labview_unsync_base_path + "/lab_meas_unsync_%.3f.txt" % labview_file_list[index_labview_file]

    labview_array = np.array(np.loadtxt(labview_file_name, delimiter='\t', unpack=False))
    all_labview_array = labview_array
    if len(all_labview_array.shape) == 1:
        all_labview_array_time_list = all_labview_array[0]
    else:
        all_labview_array_time_list = all_labview_array[:,0].tolist()
                                                                                                                                                                                
    synced_array = np.array([])
    if (not isinstance(all_labview_array_time_list,list)):
        labview_time = all_labview_array_time_list
        delta_time = labview_time - timestamp
        if abs(delta_time) > 100:
            LabviewFlag = True
        else:
            Resis13 = all_labview_array[1]
            Resis14 = all_labview_array[2]
            Resis15 = all_labview_array[3]
            Resis16 = all_labview_array[4]
            Resis17 = all_labview_array[5]
            Resis18 = all_labview_array[6]
            Resis19 = all_labview_array[7]
            Resis20 = all_labview_array[8]
            Voltage1 = all_labview_array[9]
            Current1 = all_labview_array[10]
            Voltage2 = all_labview_array[11]
            Current2 = all_labview_array[12]
            Voltage3 = all_labview_array[13]
            Current3 = all_labview_array[14]
    else:
        labview_time = min(all_labview_array_time_list, key=lambda x:abs(x-float(timestamp)))
        delta_time = labview_time - timestamp
        if abs(delta_time) > 100:
            LabviewFlag = True
        else:
            index_labview_time = all_labview_array_time_list.index(float(labview_time))
            Resis13 = all_labview_array[index_labview_time,1]
            Resis14 = all_labview_array[index_labview_time,2]
            Resis15 = all_labview_array[index_labview_time, 3]
            Resis16 = all_labview_array[index_labview_time, 4]
            Resis17 = all_labview_array[index_labview_time, 5]
            Resis18 = all_labview_array[index_labview_time, 6]
            Resis19 = all_labview_array[index_labview_time, 7]
            Resis20 = all_labview_array[index_labview_time, 8]
            Voltage1 = all_labview_array[index_labview_time, 9]
            Current1 = all_labview_array[index_labview_time, 10]
            Voltage2 = all_labview_array[index_labview_time, 11]
            Current2 = all_labview_array[index_labview_time, 12]
            Voltage3 = all_labview_array[index_labview_time, 13]
            Current3 = all_labview_array[index_labview_time, 14]

    if LabviewFlag:
            Resis13 = -1
            Resis14 = -1
            Resis15 = -1
            Resis16 = -1
            Resis17 = -1
            Resis18 = -1
            Resis19 = -1
            Resis20 = -1
            Voltage1 = -1
            Current1 = -1
            Voltage2 = -1
            Current2 = -1
            Voltage3 = -1
            Current3 = -1
    return Resis13, Resis14, Resis15, Resis16, Resis17, Resis18, Resis19, Resis20, Voltage1, Current1, Voltage2, Current2, Voltage3, Current3



def Resistance_calc(T): #Function to calculate resistance for any temperature                                                                                                                                                                 
    R0 = 100 #Resistance in ohms at 0 degree celsius                                                                                                                                                                                          
    alpha = 0.00385
    Delta = 1.4999 #For pure platinum                                                                                                                                                                                                         
    if T < 0:
        Beta = 0.10863
    elif T > 0:
        Beta = 0
    RT = (R0 + R0*alpha*(T - Delta*(T/100 - 1)*(T/100) - Beta*(T/100 - 1)*((T/100)**3)))*100
    return RT


def Temp_calc(R): #Function to calculate temperature for any resistance                                                                                                                                                                       
    Temp_x = np.linspace(-30, 30, num=100) #Points to be used for interpolation                                                                                                                                                               
    Resis_y = np.array([])
    for i in range(len(Temp_x)):
        Resis_y = np.append(Resis_y,Resistance_calc(Temp_x[i]))
    Temperature_R = np.interp(R, Resis_y, Temp_x)
    #plt.plot(Temp_x, Resis_y, 'o')                                                                                                                                                                                                           
    #plt.show()                                                                                                                                                                                                                               
    return Temperature_R

def ConvertEnv(timestamp):
	Resis13, Resis14, Resis15, Resis16, Resis17, Resis18, Resis19, Resis20, Voltage1, Current1, Voltage2, Current2, Voltage3, Current3 = GetEnvMeas(timestamp)
	if Resis13 != -1 and Resis14 != -1 and Resis15 != -1 and Resis16 != -1  and Resis17 != -1 and Resis18 != -1 and Resis19 != -1 and Resis20 != -1:
		Temp13 = Temp_calc(Resis13)
		Temp14 = Temp_calc(Resis14)
		Temp15 = Temp_calc(Resis15)
		Temp16 = Temp_calc(Resis16)
		Temp17 = Temp_calc(Resis17)
		Temp18 = Temp_calc(Resis18)
		Temp19 = Temp_calc(Resis19)
		Temp20 = Temp_calc(Resis20)
	else: 
		Temp13 = -1
		Temp14 = -1
		Temp15 = -1
		Temp16 = -1
		Temp17 = -1
		Temp18 = -1
		Temp19 = -1
		Temp20 = -1
	return Temp13, Temp14, Temp15, Temp16, Temp17, Temp18, Temp19, Temp20, Voltage1, Current1, Voltage2, Current2, Voltage3, Current3