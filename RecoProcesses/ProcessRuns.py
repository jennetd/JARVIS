import ParseFunctions as pf
import AllModules as am

def TrackingRuns(RunNumber, MyKey, Debug):
    MyKey = MyKey
    RunList = []  
    FieldIDList = [] 

    if RunNumber == -1:
        #Retrieve the list of all runs that have not been processed yet

        FilterByFormula = pf.ORFunc([am.ProcessDict[0].keys()[0],am.ProcessDict[0].keys()[0]],[am.StatusDict[3], am.StatusDict[5]])                                                                 
        headers = {'Authorization': 'Bearer %s' % MyKey, } 
    
        if pf.QueryGreenSignal(True): response = am.requests.get(am.CurlBaseCommand  + '?filterByFormula=' + FilterByFormula, headers=headers)

        ResponseDict = am.ast.literal_eval(response.text)  
        if Debug: return ResponseDict, FilterByFormula

        for i in ResponseDict["records"]: 
            RunList.append(i['fields'][am.QueryFieldsDict[0]]) 
            FieldIDList.append(i['id']) 
                                                                             
    else: 
        #If RunNumber is specified, then run only on that run
        RunList.append(RunNumber)
        FieldIDList.append(pf.GetFieldID(am.QueryFieldsDict[0], RunNumber, False, MyKey))

    return RunList, FieldIDList 

def ConversionRuns(RunNumber, Digitizer, MyKey, Debug, condor):
    RunList = []                                                                                                                                                                                                                                                                         
    FieldIDList = []   
    MyKey = MyKey
    if RunNumber == -1:                                                                                                                                                                                                                                                                  

        ProcessName = am.ProcessDict[1].keys()[0] + Digitizer
        if not condor: 
            FilterByFormula = pf.ORFunc([ProcessName, ProcessName],[am.StatusDict[3], am.StatusDict[5]])                                                                 
        else:   
            OR1 = pf.ORFunc([am.ProcessDict[6].keys()[0] + Digitizer],[am.StatusDict[0]]) ## xrd raw files is complete
            OR2 = pf.ORFunc([ProcessName, ProcessName],[am.StatusDict[3], am.StatusDict[5]]) ## conversion not started or on retry
            FilterByFormula = 'AND(' + OR1 + ',' + OR2 + ')'
            # OR1 = pf.EqualToFunc(pf.Curly(am.ProcessDict[6].keys()[0]+ Digitizer), pf.DoubleQuotes(am.StatusDict[3]))
            
        headers = {'Authorization': 'Bearer %s' % MyKey, }                                                                                                                                                                                                                                
        if pf.QueryGreenSignal(True): response = am.requests.get(am.CurlBaseCommand  + '?filterByFormula=' + FilterByFormula, headers=headers)                                                                                                                                                                                
        ResponseDict = am.ast.literal_eval(response.text)                                                                                                                                                                                                                                       
        if Debug: return ResponseDict, FilterByFormula

        for i in ResponseDict["records"]:                                                                                                                                                                                                                                                    
            RunList.append(i['fields'][am.QueryFieldsDict[0]])                                                                                                                                                                                                                                        
            FieldIDList.append(i['id'])                                                                                                                                                                                                                                                      
    else:
        RunList.append(RunNumber)
        FieldIDList.append(pf.GetFieldID(am.QueryFieldsDict[0], RunNumber, False, MyKey))

    return RunList, FieldIDList      

def LabviewRuns(RunNumber, Digitizer, MyKey, Debug):
    RunList = []                                                                                                                                                                                                                                                                         
    FieldIDList = []   
    MyKey = MyKey
    if RunNumber == -1:                                                                                                                                                                                                                                                                  

        ProcessName = am.ProcessDict[4].keys()[0] + Digitizer
        OR1 = pf.ORFunc([am.ProcessDict[2].keys()[0] + Digitizer, am.ProcessDict[2].keys()[0] + Digitizer],[am.StatusDict[0], am.StatusDict[7]])
        OR2 = pf.ORFunc([ProcessName, ProcessName],[am.StatusDict[3], am.StatusDict[5]])                                                                 
        FilterByFormula = 'AND(' + OR1 + ',' + OR2 + ')'

        headers = {'Authorization': 'Bearer %s' % MyKey, }                                                                                                                                                                                                                                
        if pf.QueryGreenSignal(True): response = am.requests.get(am.CurlBaseCommand  + '?filterByFormula=' + FilterByFormula, headers=headers)                                                                                                                                                                                
        ResponseDict = am.ast.literal_eval(response.text)                                                                                                                                                                                                                                       
        if Debug: return ResponseDict, FilterByFormula

        for i in ResponseDict["records"]:                                                                                                                                                                                                                                                    
            RunList.append(i['fields'][am.QueryFieldsDict[0]])                                                                                                                                                                                                                                        
            FieldIDList.append(i['id'])                                                                                                                                                                                                                                                      
    else:
        RunList.append(RunNumber)
        FieldIDList.append(pf.GetFieldID(am.QueryFieldsDict[0], RunNumber, False, MyKey))

    return RunList, FieldIDList                                                                                                                                                                                                               

def TimingDAQRuns(RunNumber, DoTracking, Digitizer, MyKey, Debug, condor=False):  
    RunNumber = RunNumber
    DoTracking = DoTracking
    Digitizer = Digitizer                                                                                                                                                                                                                                           
    RunList = []                                                                                                                                                                                                                                                                         
    FieldIDList = []                                                                                                                                                                                                                                                                     
    DigitizerList = []   
    MyKey = MyKey                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

    if DoTracking: 
        ProcessName = am.ProcessDict[2].keys()[0] + Digitizer
    else:
        ProcessName = am.ProcessDict[3].keys()[0] + Digitizer

    if RunNumber == -1:            
        OR1 = pf.ORFunc([am.ProcessDict[1].keys()[0] + Digitizer, am.ProcessDict[1].keys()[0] + Digitizer],[am.StatusDict[0], am.StatusDict[7]])                                                                 
        OR2 = pf.ORFunc([am.ProcessDict[0].keys()[0],am.ProcessDict[0].keys()[0]],[am.StatusDict[0], am.StatusDict[7]])                                                                                                                                                              
        OR3 = pf.ORFunc([ProcessName, ProcessName],[am.StatusDict[3], am.StatusDict[5]])
        OR4 = pf.ORFunc([am.ProcessDict[3].keys()[0] + Digitizer],[am.StatusDict[0]])                                                                                                                                                                                                  
        xrdcpDone = pf.ORFunc([am.ProcessDict[6].keys()[0] + Digitizer],[am.StatusDict[0]])                                                                                                                                                                                                  
        AND1 = pf.ANDFunc([am.ProcessDict[0].keys()[0], ProcessName],[am.StatusDict[0], am.StatusDict[3]])
        if Digitizer == am.DigitizerDict[0] or Digitizer == am.DigitizerDict[1] or Digitizer == am.DigitizerDict[5]:
            if DoTracking and not Digitizer == am.DigitizerDict[5]: 
                FilterByFormula = 'AND(' + OR3 + ',' + OR2 + ')'
            elif DoTracking and Digitizer == am.DigitizerDict[5]:
                #FilterByFormula = 'AND(' + OR4 + ',' + OR3 + ',' + OR2 + ')'
                FilterByFormula = AND1
            else:
                FilterByFormula = OR3 
        else:
            FilterByFormula = 'AND(' + OR1 + ',' + OR3   
            if DoTracking: FilterByFormula = FilterByFormula + ',' + OR2 
            if condor:  FilterByFormula = FilterByFormula + ',' + xrdcpDone 
            FilterByFormula = FilterByFormula + ')'

        headers = {'Authorization': 'Bearer %s' % MyKey, }                                                                                                                                                                                                                                
        if pf.QueryGreenSignal(True): response = am.requests.get(am.CurlBaseCommand  + '?filterByFormula=' + FilterByFormula, headers=headers)                                                                                                                                                                               
        ResponseDict = am.ast.literal_eval(response.text) 
        if Debug: return ResponseDict, FilterByFormula                                                                                                                                                                                                                                    

        for i in ResponseDict["records"]:                                                                                                                                                                                                                                   
            RunList.append(i['fields'][am.QueryFieldsDict[0]])                                                                                                                                                                                                                                        
            FieldIDList.append(i['id'])
    else:
        RunList.append(RunNumber)
        FieldIDList.append(pf.GetFieldID(am.QueryFieldsDict[0], RunNumber, False, MyKey))

    # print RunList
    return RunList, FieldIDList                                                                                                                                                                                                                  


def WatchCondorRuns(RunNumber, DoTracking, Digitizer, MyKey, False):
    RunNumber = RunNumber
    DoTracking = DoTracking
    Digitizer = Digitizer                                                                                                                                                                                                                                           
    RunList = []                                                                                                                                                                                                                                                                         
    FieldIDList = []                                                                                                                                                                                                                                                                     
    ProcessList=[]  
    MyKey = MyKey                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
    # ProcessName = am.ProcessDict[5].keys()[0] + Digitizer

    # condition = pf.ORFunc([am.ProcessDict[2].keys()[0]],[am.StatusDict[8]])
   
    ### Get TimingDAQ condor runs
    Condition = pf.EqualToFunc(pf.Curly(am.ProcessDict[2].keys()[0]+ Digitizer), pf.DoubleQuotes(am.StatusDict[8]))

    # print am.CurlBaseCommand  + '?filterByFormula=' + Condition
    headers = {'Authorization': 'Bearer %s' % MyKey, }                                                                                                                                                                                                                                
    if pf.QueryGreenSignal(True): response = am.requests.get(am.CurlBaseCommand  + '?filterByFormula=' + Condition, headers=headers)                                                                                                                                                                               
    ResponseDict = am.ast.literal_eval(response.text) 
  #  print ResponseDict
    for i in ResponseDict["records"]:                                                                                                                                                                                                                                   
        RunList.append(i['fields'][am.QueryFieldsDict[0]])                                                                                                                                                                                                                                        
        FieldIDList.append(i['id'])
        ProcessList.append(2)

    am.time.sleep(1)

    ### Get Conversion condor runs
    Condition = pf.EqualToFunc(pf.Curly(am.ProcessDict[1].keys()[0]+ Digitizer), pf.DoubleQuotes(am.StatusDict[8]))
    # print am.CurlBaseCommand  + '?filterByFormula=' + Condition
    headers = {'Authorization': 'Bearer %s' % MyKey, }                                                                                                                                                                                                                                
    if pf.QueryGreenSignal(True): response = am.requests.get(am.CurlBaseCommand  + '?filterByFormula=' + Condition, headers=headers)                                                                                                                                                                               
    ResponseDict = am.ast.literal_eval(response.text) 
    # print ResponseDict
    for i in ResponseDict["records"]:                                                                                                                                                                                                                                   
        RunList.append(i['fields'][am.QueryFieldsDict[0]])                                                                                                                                                                                                                                        
        FieldIDList.append(i['id'])
        ProcessList.append(1)

    # print RunList,ProcessList,FieldIDList
    return RunList, FieldIDList, ProcessList    

def xrdcpRawRuns(RunNumber, Digitizer, MyKey, False):
    RunNumber = RunNumber
    Digitizer = Digitizer                                                                                                                                                                                                                                           
    RunList = []                                                                                                                                                                                                                                                                         
    FieldIDList = []                                                                                                                                                                                                                                                                     
    DigitizerList = []   
    MyKey = MyKey     
    # Condition = pf.EqualToFunc(pf.Curly(am.ProcessDict[6].keys()[0]+ Digitizer), pf.DoubleQuotes(am.StatusDict[3]))
    ProcessName = am.ProcessDict[6].keys()[0]+ Digitizer
    conversion_done = pf.EqualToFunc(pf.Curly(am.ProcessDict[1].keys()[0]+ Digitizer), pf.DoubleQuotes(am.StatusDict[0]))
    needsxrdp = pf.ORFunc([ProcessName, ProcessName],[am.StatusDict[3], am.StatusDict[5]])  
    FilterByFormula = FilterByFormula = 'AND(' + needsxrdp + ',' + conversion_done + ')'
    # FilterByFormula = pf.ORFunc([ProcessName, ProcessName],[am.StatusDict[3], am.StatusDict[5]])  
    headers = {'Authorization': 'Bearer %s' % MyKey, }                                                                                                                                                                                                                                
    if pf.QueryGreenSignal(True): response = am.requests.get(am.CurlBaseCommand  + '?filterByFormula=' + FilterByFormula, headers=headers)                                                                                                                                                                               
    ResponseDict = am.ast.literal_eval(response.text) 
    # print ResponseDict
    for i in ResponseDict["records"]:                                                                                                                                                                                                                                   
        RunList.append(i['fields'][am.QueryFieldsDict[0]])                                                                                                                                                                                                                                        
        FieldIDList.append(i['id'])

    print RunList
    return RunList, FieldIDList        


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
