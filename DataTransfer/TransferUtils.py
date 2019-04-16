import os
import glob

def ListXrdRemote(site, directory):
    tmpRemoteFileList = os.popen("xrdfs root://" + site + " ls " + directory).read().splitlines()    
    processedRemoteFileList = []
    for f in tmpRemoteFileList:
        processedRemoteFileList.append(f.split("/")[-1])

    return processedRemoteFileList

def ListLocalFiles(directory):
    localList = []
    tmp = glob.glob(directory+"/*")    
    print tmp
    for f in tmp:
        #print f
        a = f.split("/")[-1]
        localList.append(a)

    return localList

def XrdCopyLocalToRemote(remoteSite, remoteDir, localDir):

    RemoteFileList = ListXrdRemote(remoteSite, remoteDir)
    LocalFileList = ListLocalFiles(localDir)
    
    for f in LocalFileList:        
        if f in RemoteFileList:
            print f, "yes"
        else:
            print f, "no"
            command = "xrdcp " + localDir+"/" + f + " root://cmseos.fnal.gov//" + remoteDir + "/"
            print command
