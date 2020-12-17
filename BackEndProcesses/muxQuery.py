import AllModules as am
import ParseFunctions as pf
import os

MuxConfFileName = "/home/daq/MuxMount/relay_control.txt"

def GetMuxStringConf(GlobalConfNum):
	MyKey = am.GetKey()
	
	## first find KeySight config number
	FilterByFormula = pf.EqualToFunc(pf.Curly("Configuration number"), pf.DoubleQuotes(GlobalConfNum))
	headers = {'Authorization': 'Bearer %s' % MyKey, } 
	if pf.QueryGreenSignal(True): response = am.requests.get(am.CurlBaseCommandConfig  + '?filterByFormula=' + FilterByFormula, headers=headers)
	ResponseDict = am.ast.literal_eval(response.text)  
	scopeconfID = ResponseDict['records'][0]['fields']['ConfigurationKeySightScope']


	## next find mux settings from keysight scope config
	if pf.QueryGreenSignal(True): 
		CMD = am.CurlBaseCommandKeySight + '/' + scopeconfID[0]
		response = am.requests.get(CMD, headers=headers)

	ResponseDict2 = am.ast.literal_eval(response.text)  
	mux1 = ResponseDict2['fields']['CH0 MUX']
	mux2 = ResponseDict2['fields']['CH1 MUX']
	mux3 = ResponseDict2['fields']['CH2 MUX']
	mux4 = ResponseDict2['fields']['CH3 MUX']

	# mux4 = 'k7'
	mux_setting =  "%s %s %s %s" %(mux1,mux2,mux3,mux4)
	print mux_setting
	return mux_setting


def ConfigureMux(GlobalConfNum):
	mux_setting = GetMuxStringConf(GlobalConfNum)

	MuxConfFile = open("mux_buffer.txt", "w")
	MuxConfFile.write(mux_setting)
	MuxConfFile.close()
	os.system("mv mux_buffer.txt %s"%MuxConfFileName)

# def GetMuxStringConf(ScopeConfNum):
# 	MyKey = am.GetKey()
# 	FilterByFormula = pf.EqualToFunc(pf.Curly("Configuration number"), pf.DoubleQuotes(ScopeConfNum))
	
# 	headers = {'Authorization': 'Bearer %s' % MyKey, } 
# 	if pf.QueryGreenSignal(True): response = am.requests.get(am.CurlBaseCommandKeySight  + '?filterByFormula=' + FilterByFormula, headers=headers)

# 	ResponseDict = am.ast.literal_eval(response.text)  
	
# 	mux1 = ResponseDict['records'][0]['fields']['CH0 MUX']
# 	mux2 = ResponseDict['records'][0]['fields']['CH1 MUX']
# 	mux3 = ResponseDict['records'][0]['fields']['CH2 MUX']
# 	mux4 = ResponseDict['records'][0]['fields']['CH3 MUX']

# 	print  "%s %s %s %s" %(mux1,mux2,mux3,mux4)

# 	return ResponseDict

	# for i in ResponseDict["records"]: 
	#     RunList.append(i['fields'][am.QueryFieldsDict[0]]) 
	#     FieldIDList.append(i['id']) 