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
			
			if ColumnNames == 'Configuration number':
			CMD = am.CurlBaseCommandSensor + '/' + ID

			if ColumnNames == '':
			response = am.requests.get(CMD, headers=headers)
			ResponseDict = am.ast.literal_eval(response.text)
			for ColumnNames,ColumnEntries in ResponseDict["fields"].items():
				if ColumnNames == 'Name':
					SensorNameList = SensorNameList.append(ColumnEntries)
				if ColumnNames == 'Number of channels':
					NumberOfChannels = NumberofChannelsList.append(ColumnEntries)
			print ColumnNames, ColumnEntries

	else:
		print '%s was not present in this run' % Digitizer



