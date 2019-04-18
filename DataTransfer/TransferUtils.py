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
    for f in tmp:
        a = f.split("/")[-1]
        localList.append(a)

    return localList

def XrdCopyLocalToRemote(remoteSite, remoteDir, localDir):

    RemoteFileList = ListXrdRemote(remoteSite, remoteDir)
    LocalFileList = ListLocalFiles(localDir)
    
    for f in LocalFileList:        
        if f in RemoteFileList:
            print f, " : Already present at Remote site " + remoteSite
        else:
            command = "xrdcp " + localDir+"/" + f + " root://" + remoteSite + "//" + remoteDir + "/"
            os.system(command)
            

