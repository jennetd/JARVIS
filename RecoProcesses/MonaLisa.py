
import sys 
sys.path.append('/home/daq/JarvisDevelopment/BackEndProcesses/')
import time                                                                                                                                                                                                                                             
import numpy as np                                                                                                                                                                                                                                                                      
import getpass                                                                                                                                                                                                                                                                          
import os                                                                                                                                                                                                                                                                                
import subprocess as sp                                                                                                                                                                                                                                                                  
import socket                                                                                                                                                                                                                                                                            
import sys                                                                                                                                                                                                                                                                               
import glob                                                                                                                                                                                                                                                                              
import subprocess                                                                                                                                                                                                                                                                        
from subprocess import Popen, PIPE                                                                                                                                                                                                                                                       
import pipes                                                                                                                                                                                                                                                                             
from pipes import quote                                                                                                                                                                                                                                                                  
import argparse                                                                                                                                                                                                                                                                          
import ParseFunctions as pf                                                                                                                                                                                                                                                           
import ProcessRuns as pr                                                                                                                                                                                                                                                                 
import ProcessCMDs as pc
import matplotlib                                                                                                                                                                                                                                                                        
matplotlib.use("Agg")                                                                                                                                                                                                                                                                    
import matplotlib.pyplot as plt                                                                                                                                                                                                                                                          
from PIL import Image                                                                                                                                                                                                                                                                    
import multiprocessing 
  
from multiprocessing import Pool


################################################################################################################################################################################################################                                                                         
################################################################################################################################################################################################################                                                                         
################################### MonaLisa is a wrapper for the automation program which interacts with the run table database and runs different reconstruction processes ###################################
################################################################################################################################################################################################################                                                                         
################################################################################################################################################################################################################                                                                         

def CodeImage(time):                                                                                                                                                                                                                                                                     
    ImageAddress = '/home/daq/MonaLisa/mona_lisa.png'                                                                                                                                                                                                                                    
    ImageItself = Image.open(ImageAddress)                                                                                                                                                                                                                                               
    ImageNumpyFormat = np.asarray(ImageItself)                                                                                                                                                                                                                                           
    plt.imshow(ImageNumpyFormat)                                                                                                                                                                                                                                                         
    plt.draw()                                                                                                                                                                                                                                                                           
    plt.pause(time) # pause how many seconds                                                                                                                                                                                                                                             
    plt.close()                                                                                                                                                                                                                                                                          
    os.system('display %s' % ImageAddress)                                                                                                                                                                                                  


def TrackFileRemoteExists(x):
    TrackFilePathRulinux = BaseTrackDirRulinux +'CMSTimingConverted/Run%i_CMSTiming_converted.root' % x
    return exists_remote(RulinuxSSH, TrackFilePathRulinux), TrackFilePathRulinux

def TrackFileLocalExists(x):
    TrackFilePathLocal = BaseTrackDirLocal + 'Run%i_CMSTiming_converted.root' % x
    return os.path.exists(TrackFilePathLocal), TrackFilePathLocal

def FileSizeBool(FilePath, SizeCut):
    return os.stat(FilePath).st_size < SizeCut
                                             


def FinalTracking(CMD): 

    session = subprocess.Popen(["ssh", RulinuxSSH, CMD], stderr=subprocess.PIPE, stdout=subprocess.PIPE)                                                                                                             
    stdout, stderr = session.communicate()                                                                                                                                                                                                                                       

        
    # Criteria for good tracking: file exist on both remote and local computer and the file size is greater than 5k                                                                                                                                                                      
    TrackExistsLocalBool, TrackFilePathLocal= TrackFileLocalExists(x)                                                                                                                                                                                                                    
    if stderr or not TrackExistsLocalBool or FileSizeBool(TrackFilePathLocal,SizeCut):                                                                                                                                                                                                   
    if TrackingCMDList:

    # printing process id 
    print("ID of process running worker1: {}".format(os.getpid())) 
  

def FinalConversion(): 
    # printing process id 
    print("ID of process running worker2: {}".format(os.getpid())) 
  
def FinalTimingDAQ(): 
    # printing process id 
    print("ID of process running worker2: {}".format(os.getpid())) 

def PoolHandler(Function,Input, MaxPoolInputs):
    p = Pool(MaxPoolInputs)
    p.map(Function, Input) # Input is the list of inputs out of which only two will be used at the same with the same function parallely
  
if __name__ == "__main__": 
    # printing main program process id 
    print("ID of main process: {}".format(os.getpid())) 
  
    # creating processes 
    p1 = multiprocessing.Process(target=worker1) 
    p2 = multiprocessing.Process(target=worker2) 
  
    # starting processes 
    p1.start() 
    p2.start() 
  
    # process IDs 
    print("ID of process p1: {}".format(p1.pid)) 
    print("ID of process p2: {}".format(p2.pid)) 
  
    # wait until processes are finished 
    p1.join() 
    p2.join() 
  
    # both processes finished 
    print("Both processes finished execution!") 
  
    # check if processes are alive 
    print("Process p1 is alive: {}".format(p1.is_alive())) 
    print("Process p2 is alive: {}".format(p2.is_alive())) 


    TrackingCMDList, FieldIDList = pc.TrackingCMDs()

    if TrackingCMDList:
        
        PoolHandler(FinalTracking, TrackingCMDList)


##Call tracking function to get the cmd list, wait if empty
##Call COnversion
