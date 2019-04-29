import sys 
sys.path.append('/home/daq/JARVIS/BackEndProcesses/')
import AllModules as am
import ParseFunctions as pf

Table = {
                    0 : 'tblecUNuCEfrPxXnl',
                    1 : 'tblZ8GeBsg5UhJoiw',
                    2 : 'TekScope',
                    3 : 'tbl4xS3mzqGDTuXAC',
                    4 : 'Sampic',
        }

key = am.GetKey()

def DumpConfiguration(RunNumber, DigitizerKey, Debug):
	Digitizer = am.DigitizerDict[DigitizerKey]
	TableName = Table[DigitizerKey]
	ColumnNamesList = []
	ColumnEntriesList = []
	SensorNameList = []
	NumberofChannelsList = []
	DigitizerChannelList = []
	SensorChannelList = []
	ChannelForSensorList = []

	GlobalConfigIDList, RecordID = pf.ParsingQuery(1, ["Run number"], [RunNumber], "Configuration", False, key)
	GlobalConfigID = GlobalConfigIDList[0][0]

	#### Making query to global config table
	headers = {'Authorization': 'Bearer %s' % key, }
	CMD = am.CurlBaseCommandConfig + '/' + GlobalConfigID
	response = am.requests.get(CMD, headers=headers)
	ResponseDict = am.ast.literal_eval(response.text)
	if Debug: print ResponseDict, CMD


	QueryName = 'Configuration' + Digitizer
	for ColumnNames,ColumnEntries in  ResponseDict["fields"].items():
		ColumnNamesList.append(ColumnNames)
		ColumnEntriesList.append(ColumnEntries)

	if QueryName in ColumnNamesList:
		index = ColumnNamesList.index(QueryName)
		DigiConfigID = ColumnEntriesList[index][0]

		#### Querying the Digi Config table
		DigiCMD =am.CurlBaseCommandWithoutTable + '/' + TableName + '/' + DigiConfigID
		response = am.requests.get(DigiCMD, headers=headers)
		DigiResponseDict = am.ast.literal_eval(response.text)
		if Debug: print DigiResponseDict, DigiCMD

		for ColumnNames,ColumnEntries in DigiResponseDict["fields"].items():
			#print ColumnNames, ColumnEntries
			if 'Ch ' in ColumnNames:
				DigitizerChannelList.append(ColumnNames.split("Ch ")[1])
				SensorChannelList.append(ColumnEntries)

			if 'Sensor' in ColumnNames:
				ChannelForSensorList.append(ColumnNames.split(' Ch')[1])
				ID = ColumnEntries[0]
				SensorCMD = am.CurlBaseCommandSensor + '/' + ID
				response = am.requests.get(SensorCMD, headers=headers)
				ResponseDict = am.ast.literal_eval(response.text)
				
				for ColumnNames,ColumnEntries in ResponseDict["fields"].items():
					if ColumnNames == 'Name':
						SensorNameList.append(ColumnEntries)
					if ColumnNames == 'Number of channels':
						NumberofChannelsList.append(ColumnEntries)

		DigitizerChannelListInt = map(int,DigitizerChannelList)
		ChannelForSensorListInt = map(int,ChannelForSensorList)

		zipped_pair1 = zip(ChannelForSensorListInt, SensorNameList)
		zipped_pair2 = sorted(zipped_pair1, key=lambda x: x[0])

		zipped_pair3 = zip(DigitizerChannelListInt, SensorChannelList)
		zipped_pair4 = sorted(zipped_pair3, key=lambda x: x[0])

		flatlist1 = zip(*zipped_pair2)
		flatlist2 = zip(*zipped_pair4)

		ziplist = zip(flatlist2[0], flatlist1[1], flatlist2[1])
		
		return ziplist

	else:
		print '%s was not present in this run' % Digitizer


def GetRunNumbersFromConfig(ConfigNumber, DigitizerKey): # DigitizerKey = 0 for VME, 1 for DT5742, 3 for KeySightScope
	##### This function gives you the list of run numbers which have
	################ 1) A given configuration 
	################ 2) Complete reco
	################ 3) A specific Digitizer
	
	key = am.GetKey()
	Digitizer = am.DigitizerDict[DigitizerKey]	
	RunNumberList, RunNumberIDList = pf.ParsingQuery(2, ["Configuration", "TimingDAQ" + Digitizer], [ConfigNumber, "Complete"], "Run number", False, key)
	return RunNumberList

def GetRunNumbersForConditions(QueryItem, QueryItemBoundsList, DigitizerKey, ConfigNumber = -1):

	#### This function gives you the list of the run numbers which have 
	#################### 1) Complete reco
	#################### 2) The value of a specific QueryItem between the lower and upper bound
	#################### 3) A specific config number 
	#################### 4) A specific digitizer

	ModifiedRunList = []
	key = am.GetKey()
	Digitizer = am.DigitizerDict[DigitizerKey]
	if ConfigNumber != -1:
		OutputDict = pf.ParsingQuery3(2, ["Configuration", "TimingDAQ" + Digitizer], [ConfigNumber, "Complete"], ["Run number", QueryItem], False, key)
	else:
		OutputDict = pf.ParsingQuery3(1, ["TimingDAQKeySightScope"], ["Complete"], ["Run number", QueryItem], False, key)		
	RunNumberList = OutputDict[0]
	QueryItemListFloat = map(float,OutputDict[1])
	print 
	for item in QueryItemListFloat:
		print item
		if item >= QueryItemBoundsList[0] and item <= QueryItemBoundsList[1]:
			ModifiedRunList.append(RunNumberList[QueryItemListFloat.index(item)])
			print ModifiedRunList
	return RunNumberList