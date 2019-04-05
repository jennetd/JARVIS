import ParseFunctions as pf
import AllModules as am

def TrackingRuns(RunNumber, Debug):
    RunList = []  
    FieldIDList = [] 
    print "run = ", RunNumber
    if (RunNumber == -1):
        #Retrieve the list of all runs that have not been processed yet

        FilterByFormula = pf.ORFunc(['Tracking','Tracking'],['Not started', 'Retry'])                                                                 
        headers = {'Authorization': 'Bearer %s' % am.MyKey, } 
    
        if pf.QueryGreenSignal(True): response = am.requests.get(am.CurlBaseCommand  + '?filterByFormula=' + FilterByFormula, headers=headers)

        ResponseDict = am.ast.literal_eval(response.text)  
        if Debug: return ResponseDict, FilterByFormula

        for i in ResponseDict["records"]: 
            RunList.append(i['fields']['Run number']) 
            FieldIDList.append(i['id']) 
                                                                             
    else: 
        #If RunNumber is specified, then run only on that run
        RunList.append(RunNumber)
        FieldIDList.append(pf.GetFieldID("Run number", RunNumber, False))

    return RunList, FieldIDList 


def ConversionRuns(Debug):
    RunList = []                                                                                                                                                                                                                                                                         
    FieldIDList = []                                                                                                                                                                                                                                                                     

    FilterByFormula = pf.ORFunc(['Conversion','Conversion'],['Not started', 'Retry'])                                                                 

    headers = {'Authorization': 'Bearer %s' % am.MyKey, }                                                                                                                                                                                                                                
    if pf.QueryGreenSignal(True): response = am.requests.get(am.CurlBaseCommand  + '?filterByFormula=' + FilterByFormula, headers=headers)                                                                                                                                                                                
    ResponseDict = am.ast.literal_eval(response.text)                                                                                                                                                                                                                                       
    if Debug: return ResponseDict, FilterByFormula

    for i in ResponseDict["records"]:                                                                                                                                                                                                                                                    
        RunList.append(i['fields']['Run number'])                                                                                                                                                                                                                                        
        FieldIDList.append(i['id'])                                                                                                                                                                                                                                                      
        
    return RunList, FieldIDList                                                                                                                                                                                                                   


def TimingDAQRuns(DoTracking, Debug):                                                                                                                                                                                                                                               
    RunList = []                                                                                                                                                                                                                                                                         
    FieldIDList = []                                                                                                                                                                                                                                                                     
    DigitizerList = []                                                                                                                                                                                                                                                                   
    RedoList = []                                                                                                                                                                                                                                                                        
    VersionList = []                                                                                                                                                                                                                                                                     
    
    if DoTracking:
        ProcessName = 'TimingDAQ'
    else:
        ProcessName = 'TimingDAQNoTracks'

    OR1 = pf.ORFunc(['Conversion','Conversion'],['Complete', 'N/A'])                                                                 
    OR2 = pf.ORFunc(['Tracking','Tracking'],['Complete', 'N/A'])                                                                                                                                                              
    OR3 = pf.ORFunc([ProcessName, ProcessName,'Redo'],['Not started', 'Retry','Redo'])                                                                                                                                                                                                  

    FilterByFormula = 'AND(' + OR1 + ',' + OR3   
    if DoTracking: FilterByFormula = FilterByFormula + ',' + OR2 
    FilterByFormula = FilterByFormula + ')'

    headers = {'Authorization': 'Bearer %s' % am.MyKey, }                                                                                                                                                                                                                                
    if pf.QueryGreenSignal(True): response = am.requests.get(am.CurlBaseCommand  + '?filterByFormula=' + FilterByFormula, headers=headers)                                                                                                                                                                               
    ResponseDict = am.ast.literal_eval(response.text)  
    if Debug: return ResponseDict, FilterByFormula                                                                                                                                                                                                                                    
    
    for i in ResponseDict["records"]:                                                                                                                                                                                                                                                    
        RunList.append(i['fields']['Run number'])                                                                                                                                                                                                                                        
        FieldIDList.append(i['id'])                                                                                                                                                                                                                                                      
        DigitizerList.append(i['fields']['Digitizer'])                                                                                                                                                                                                                                   
        RedoList.append(i['fields']['Redo'])                                                                                                                                                                                                                                             
        VersionList.append(i['fields']['Version'])                                                                                                                                                                                                                                       
        
    return RunList, FieldIDList, DigitizerList, RedoList, VersionList                                                                                                                                                                                                                   
  



def TimingDAQRunsMoreQueries():

    #Selection criteria for run numbers for running TimingDAQ 
    OrList1, FieldID1 = pf.ParsingQuery(1, 'Conversion', 'N/A', 'Run number')
    OrList2, FieldID2 = pf.ParsingQuery(1, 'Conversion', 'Complete', 'Run number')
    OrList3, FieldID3 = pf.ParsingQuery(1, 'Tracking', 'N/A', 'Run number')
    OrList4, FieldID4 = pf.ParsingQuery(1, 'Tracking', 'Complete', 'Run number')
    OrList5, FieldID5 = pf.ParsingQuery(1, 'TimingDAQ', 'Not started', 'Run number') 
    OrList6, FieldID6 = pf.ParsingQuery(1, 'TimingDAQ', 'Retry', 'Run number') 
    OrList7, FieldID7 = pf.ParsingQuery(1, 'Redo', 'Redo', 'Run number') 

    AndList1 = list(set().union(OrList5, OrList6, OrList7))
    AndList2 = list(set(OrList1).union(OrList2))
    AndList3 = list(set().union(OrList3, OrList4))

    RunList = list(set().intersection(AndList1,AndList2,AndList3))
    
    #Get Digitizer, field ID for this runlist
    DigitizerList = []
    RedoList = []
    FieldIDList = []
    VersionList = []
    for run in RunList:
        Digitizer, FieldID = pf.ParsingQuery(1, 'Run Numbers', run, 'Digitizer')
        Redo, FieldID = pf.ParsingQuery(1, 'Run Numbers', run, 'Redo')
        Version, FieldID = pf.ParsingQuery(1, 'Run Numbers', run, 'Version')
        DigitizerList.append(Digitizer)
        RedoList.append(Redo)
        VersionList.append(Version)
        FieldIDList.append(FieldID)

    return RunList, DigitizerList, FieldIDList, RedoList, VersionList 

                                                                                    
def TrackingRunsMoreQueries():

    OrList1, FieldID1 = pf.ParsingQuery(1, 'Tracking', 'Not started', 'Run number')
    OrList2, FieldID2 = pf.ParsingQuery(1, 'Tracking', 'Retry', 'Run number')

    RunList = list(set(OrList1).union(OrList2))
    FieldIDList = list(set(FieldID1).union(FieldID2))
    
    return RunList, FieldIDList


def ConversionRunsMoreQueries():

    OrList1, FieldID1 = pf.ParsingQuery(1, 'Tracking', 'Not started', 'Run number')
    OrList2, FieldID2 = pf.ParsingQuery(1, 'Tracking', 'Retry', 'Run number')

    RunList = list(set(OrList1).union(OrList2))
    FieldIDList = list(set(FieldID1).union(FieldID2))
    
    return RunList, FieldIDList
