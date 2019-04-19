import os
import glob

def ListXrdRemote(site, directory):
    command = "xrdfs root://" + site + " ls -l " + directory
    output = os.popen(command).read().splitlines()    
    processedRemoteFileDict = {}
    for f in output:
        tmp = f.split()
        filesize=tmp[3]
        filename=(tmp[4].split("/")[-1])        
        processedRemoteFileDict[filename] = filesize
    return processedRemoteFileDict

def ListLocalFiles(directory):
    localDict = {}
    tmp = glob.glob(directory+"/*")    
    for f in tmp:
        a = f.split("/")[-1]
        size = os.path.getsize(directory+"/"+a)
        localDict[a]=size

    return localDict

def XrdCopyLocalToRemote(remoteSite, remoteDir, localDir):

    RemoteFileDict = ListXrdRemote(remoteSite, remoteDir)
    LocalFileDict = ListLocalFiles(localDir)
    
    for f in LocalFileDict:        
        doCopy = False
        if f in RemoteFileDict.keys():
            print f, " : Already present at Remote site " + remoteSite
            print LocalFileDict[f] , RemoteFileDict[f]
            if not (str(LocalFileDict[f]).strip() == str(RemoteFileDict[f]).strip()):
                doCopy = True
                print "Remote file size does not match. Remove Remote Copy, and Copy Again"
                command = "xrdfs root://" + remoteSite + " rm " + remoteDir + "/" + f
                os.system(command)
        else:
            print f, " : Not present at Remote site " + remoteSite
            doCopy = True

        if doCopy:            
            command = "xrdcp " + localDir+"/" + f + " root://" + remoteSite + "//" + remoteDir + "/"            
            os.system(command)
            

