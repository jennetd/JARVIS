from AllModules import *
import ParseFunctions as pf
import TCP_com as tp

#### Look at these parameters before running the listener
UsingAutoPilot = True
Configuration = 122   ##not used except in BTL mode

LongAcquisitionMode = False #True


numEvents = 25 ## not used in Long mode
numPoints = 25 ##MSa, only used in Long mode
sampleRate = 10 #GSa/s
horizontalWindow = 50 #ns

### if sample rate or horizontal window is changed, TimingDAQ must be recompiled to account for new npoints.
#trigCh = "C8"
#trig   = 0.15

trigCh = "EX"
#trigCh = "LINE" 
trig = 0.41 #0.15 # V

vScale1 = 0.05  
vScale2 = 0.05
vScale3 = 0.05 
vScale4 = 0.05
vScale5 = 0.05  
vScale6 = 0.05
vScale7 = 0.05 
vScale8 = 0.10

vPos1 = 3
vPos2 = 3
vPos3 = 3

timeoffset = 75#100 ##75 scintillator trigger

#2022 values  #105 ns (50D) 30 ns (SiPM self trigger) 85 (Lorenzo scin) 105 (SiPM telescope trigger)

############### Remember to source the otsdaq environment
############### Assuming the directory structure in the KeySightScope repository is the same as on this computer

AutoPilotStatusFile = LecroyScopeCommFileName
#AgilentScopeCommand = 'python %sAcquisition/acquisition.py --numEvents %d --sampleRate %d --horizontalWindow %d --trigCh %s --trig %f --vScale1 %f --vScale2 %f --vScale3 %f --vScale4 %f --timeoffset %i --trigSlope POS' % (ScopeControlDir, numEvents, sampleRate, horizontalWindow, trigCh, trig, vScale1, vScale2, vScale3, vScale4, timeoffset) 
#print AgilentScopeCommand
print "####################################"
print "## Starting Loop: Waiting for run ##"
print "####################################"
while True:

    inFile = open(AutoPilotStatusFile,"r")
    runNumber = inFile.readline().strip()
    time.sleep(1)

    if (runNumber != str(0)):

        ScopeStateHandle = open(ScopeStateFileName, "r")
        ScopeState = str(ScopeStateHandle.read().strip())

        if not UsingAutoPilot and ScopeState == "ready":

            ############### checking the status for the next runs #################  
            with open(AutoPilotStatusFile,'w') as file:
                file.write(str(0))
            print "\n ####################### Running the scope acquisition ##################################\n"
            
            #### Reading run number ####
            #RunNumber = tp.GetRunNumber()
            ScopeCommand = 'python %s/Acquisition/acquisition.py --runNum %s --numEvents %d --sampleRate %d --horizontalWindow %d --trigCh %s --trig %f --vScale1 %f --vScale2 %f --vScale3 %f --vScale4 %f --timeoffset %i --trigSlope POS --vPos1 %f --vPos2 %f --vPos3 %f ' % (LecroyScopeControlDir,runNumber, numEvents, sampleRate, horizontalWindow, trigCh, trig, vScale1, vScale2, vScale3, vScale4, timeoffset, vPos1, vPos2, vPos3) 
            print ScopeCommand
            #### Starting the acquisition script ####
            os.system(ScopeCommand)

            #### Updating the conversion field for "Not started" #####
            #key = GetKey()
            #FieldID = pf.GetFieldID(QueryFieldsDict[0], RunNumber, False, key)
            #pf.UpdateAttributeStatus(FieldID[0], "ConversionKeySightScope", "Not Started", False, key)
            
            print "\n ####################### Done with the scope acquisition ##################################\n"

            if not UsingAutoPilot:
                print "Updating the run table from the scope listener script"
                Command = "python ../AutoPilot/RunTableWithoutAutopilot.py %s %d" % (runNumber, Configuration)
                print Command
                os.system(Command)
                print "\n Updated the run table"
        elif UsingAutoPilot:

            ############### checking the status for the next runs #################  
            with open(AutoPilotStatusFile,'w') as file:
                file.write(str(0))
            print "\n ####################### Running the scope acquisition ##################################\n"
            
            if not LongAcquisitionMode: 
                ScopeCommand = 'python %s/Acquisition/acquisition.py --runNum %s --numEvents %d --sampleRate %d --horizontalWindow %d --trigCh %s --trig %f --vScale1 %f --vScale2 %f --vScale3 %f --vScale4 %f --vScale5 %f --vScale6 %f --vScale7 %f --vScale8 %f --timeoffset %i --trigSlope POS' % (LecroyScopeControlDir,runNumber, numEvents, sampleRate, horizontalWindow, trigCh, trig, vScale1, vScale2, vScale3, vScale4,vScale5, vScale6, vScale7, vScale8, timeoffset) 
            else: 
                newtimeoffset = -0.5*(int(runNumber) % 8)-0.25
                ScopeCommand = 'python %s/Acquisition/acquisition_one_event.py --display 1 --runNum %s --numPoints %d --sampleRate %d --trigCh %s --trig %f --vScale1 %f --vScale2 %f --vScale3 %f --vScale4 %f --vScale5 %f --vScale6 %f --vScale7 %f --vScale8 %f --timeoffset %0.2f --trigSlope NEG' % (LecroyScopeControlDir,runNumber, numPoints, sampleRate, trigCh, trig, vScale1, vScale2, vScale3, vScale4,vScale5, vScale6, vScale7, vScale8, newtimeoffset) 
            print ScopeCommand
            #### Starting the acquisition script ####
            os.system(ScopeCommand)

            #### Updating the conversion field for "Not started" #####
            #key = GetKey()
            #FieldID = pf.GetFieldID(QueryFieldsDict[0], RunNumber, False, key)
            #pf.UpdateAttributeStatus(FieldID[0], "ConversionKeySightScope", "Not Started", False, key)
            
            print "\n ####################### Done with the scope acquisition ##################################\n"

            if not UsingAutoPilot:
                print "Updating the run table from the scope listener script"
                Command = "python ../AutoPilot/RunTableWithoutAutopilot.py %s %d" % (runNumber, Configuration)
                print Command
                os.system(Command)
                print "\n Updated the run table"

        elif ScopeState == "ready":
            print 'Change the RunLog.txt file to ready'     
