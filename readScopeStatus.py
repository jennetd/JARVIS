import os
from AllModules import ScopeStatusFileName

while True:
      inFile = open('file.txt',"r")
      status = int(inFile.read())

      if ( status ==  1 ):
          with open('file.txt','w') as file:
            file.write(str(0))
          print "Running the scope acquisition"    
          os.system("python ../fnal_tb_18_11/LocalData/RECO/ETL_Agilent_MSO-X-92004A/Acquisition/acquisition.py --numEvents 20000 --numPoints 8000 --trigCh 2 --trig -0.05")
