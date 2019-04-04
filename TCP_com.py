import socket
import sys
import time
import os
import AllModules as am

def init_ots():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = "OtherRuns0,Initialize"
    sock.sendto(MESSAGE, (am.ip_address, am.use_socket))                                                                                                                                                                         
    time.sleep(5)

def config_ots():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                                                                                                                                                                                      
    MESSAGE = "OtherRuns0,Configure,T992Config"
    sock.sendto(MESSAGE, (am.ip_address, am.use_socket))                                                                                                                                                                          
    time.sleep(5)

def start_ots(Delay=False):
    copy_cmd = 'scp otsdaq@ftbf-daq-08.fnal.gov:' + am.runFileName + ' ' + am.localRunFileName       
    os.system(copy_cmd) 
    runFile = open(am.localRunFileName)
    nextRun = int(runFile.read().strip())
    runFile.close()
    incrementRunFile = open(am.localRunFileName,"w")
    incrementRunFile.write(str(nextRun+1)+"\n")
    incrementRunFile.close()
    copy_cmd = 'scp ' + am.localRunFileName +' otsdaq@ftbf-daq-08.fnal.gov:' + am.runFileName
    os.system(copy_cmd) 
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = "OtherRuns0,Start, %d" % (nextRun)
    sock.sendto(MESSAGE, (am.ip_address, am.use_socket))
    return nextRun
    if Delay: time.sleep(5)

def stop_ots(Delay=True):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    MESSAGE = "OtherRuns0,Stop"
    sock.sendto(MESSAGE, (am.ip_address, am.use_socket))
    if Delay: time.sleep(5)


