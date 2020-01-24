import sys 
sys.path.append('../BackEndProcesses/')
import ParseFunctions as pf
from AllModules import *

key = GetKey()
RunNumber = int(sys.argv[1])
Configuration = int(sys.argv[2])

ConfigID = pf.GetFieldIDOtherTable('Config', 'Configuration number', str(Configuration), False, key)
pf.NewRunRecord5(RunNumber, key, ConfigID)