import ParseFunctions as pf
import GetTemp as gt


runtable = pf.DownloadRuntable(True,'key6YLnKb2sY2XnR7')

print len(runtable['records'])

# data = {"Run number": 10000,"Start time": "2021-11-23 17:18:09", "Duration": "1000"}
# gt.GetTemperaturesSimple(data)
# gt.GetACNetYield(data)

# # pf.NewRunRecordSimple(data,'recLvlYLA1GzK4bEG',True,'key6YLnKb2sY2XnR7')
# ConfigDict, LecroyDict,KeySightDict,CAENDict,SensorDict = pf.DownloadConfigs(True,'key6YLnKb2sY2XnR7')

# print ConfigDict['records'][0]['fields']['ConfigurationLecroyScope']

# print LecroyDict['records'][0]['fields']['Sensor Ch1']

# # print SensorDict

# # print LecroyDict

# print ConfigDict

# def getSensorById(SensorDict,idnum):
# 	for item in SensorDict['records']: 
# 		if item['id']==idnum:
# 			return item['fields']['Name no commas allowed']

# def getConfigsByGConf(ConfigDict,gconf):
# 	for item in ConfigDict['records']:
# 		if item['fields']['Configuration number']==gconf:
# 			lecroyConfID = item['fields']['ConfigurationLecroyScope'][0]
# 			caenConfID = item['fields']['ConfigurationCAENHV'][0]
# 			return lecroyConfID,caenConfID


# def getSimpleLecroyDict(LecroyDict,lecroyConfID):
# 	for item in LecroyDict['records']: 
# 		if item['id']==lecroyConfID:
# 			simpleLecroyDict =  LecroyDict['records'][0]['fields']
# 			for key in simpleLecroyDict: 
# 				if "Sensor" in key:
# 					simpleLecroyDict[key] = getSensorById(SensorDict,simpleLecroyDict[key][0])
# 		# print key, test['records'][0]['fields'][key]
# 			return simpleLecroyDict

# def getSimpleCAENDict(CAENDict,caenConfID):
# 	for item in CAENDict['records']: 
# 		if item['id']==caenConfID:
# 			simpleCAENDict =  CAENDict['records'][0]['fields']
# 			for key in simpleCAENDict: 
# 				if "Sensor" in key:
# 					simpleCAENDict[key] = getSensorById(SensorDict,simpleCAENDict[key][0])
# 		# print key, test['records'][0]['fields'][key]
# 			return simpleCAENDict


# lecroyConfID,caenConfID = getConfigsByGConf(ConfigDict,438)

# simpleLecroy= getSimpleLecroyDict(LecroyDict,lecroyConfID)
# simpleCAEN= getSimpleCAENDict(CAENDict,caenConfID)

# print simpleLecroy
# print simpleCAEN
# # print getSensorById(SensorDict,LecroyDict['records'][0]['fields']['Sensor Ch1'][0])


