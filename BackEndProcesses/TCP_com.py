import socket
import sys
import time
import os
import shutil
import AllModules as am

def init_ots():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = b'OtherRuns0,Initialize'
    sock.sendto(MESSAGE, (am.ip_address, am.use_socket))                                                                                                                                                                         
    time.sleep(5)

def config_ots():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                                                                                                                                                
    MESSAGE = b'OtherRuns0,Configure,T992Config'
    sock.sendto(MESSAGE, (am.ip_address, am.use_socket))                                                                                                                                                                          
    time.sleep(5)

def start_ots(RunNumber, Delay=False):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = b'OtherRuns0,Start, %d' % (RunNumber)#(GetRunNumber()+1)
    sock.sendto(MESSAGE, (am.ip_address, am.use_socket))
    #data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes                                                                                                                                                                              
    print("Start: received message")
    return 
    
def stop_ots(Delay=True):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = b'OtherRuns0,Stop'
    sock.sendto(MESSAGE, (am.ip_address, am.use_socket))
    #data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes                                                                                                                                                                              
    print("Stop: received message")
    if Delay: time.sleep(5)

def RPComm(RunNumber, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = b'%s, %d' % (message, RunNumber)#(GetRunNumber()+1)
    sock.sendto(MESSAGE, ("192.168.133.220", 10001))
    print("Sent %s message to raspberry pi" % message)
    return 

def RPGlobalComm(message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = b'%s' % (message)#(GetRunNumber()+1)
    sock.sendto(MESSAGE, ("192.168.133.220", 10001))
    print("Sent %s message to raspberry pi" % message)
    return 

def GetRunNumber():
    runFile = open(am.localRunFileName)
    nextRun = int(runFile.read().strip()) 
    return nextRun

def UpdateRunNumber(nextRunNum):
    incrementRunFile = open(am.localRunFileName,"w")
    incrementRunFile.write(str(nextRunNum)+"\n")
    incrementRunFile.close()

def GetRunFile():
    print("Getting run file ",am.localRunFileName)
#    CMD = "cp /home/otsdaq/otsdaq/srcs/otsdaq_fermilabtestbeam/ftbf_telescope/2022_03_March_ftbf_telescope_userdata/ServiceData/RunNumber/" + am.runFileName + " " + am.localRunFileName
    #'scp cmstiming@ftbf-daq-06.fnal.gov:' + am.runFileName + ' ' + am.localRunFileName
#    print(CMD)
#    session = am.subprocess.Popen(CMD,stdout=am.PIPE, stderr=am.subprocess.PIPE, shell=True)       
#    stdout = session.communicate()
#    print(stdout)

    shutil.copyfile(am.runFileName,am.localRunFileName)

def SendRunFile():
    print("Sending run file ",am.localRunFileName)
    shutil.copyfile(am.localRunFileName,am.runFileName)
#    CMD = "cp " + am.localRunFileName + " /home/otsdaq/otsdaq/srcs/otsdaq_fermilabtestbeam/ftbf_telescope/2022_03_March_ftbf_telescope_userdata/ServiceData/RunNumber/" + am.runFileName
    #'scp ' + am.localRunFileName +' cmstiming@ftbf-daq-06.fnal.gov:' + am.runFileName
 #   session = am.subprocess.Popen(CMD,stdout=am.PIPE, stderr=am.subprocess.PIPE, shell=True) 
 #   stdout = session.communicate()
 #   print(stdout)

