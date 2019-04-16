# J.A.R.V.I.S.
Just A Rather Very Intelligent System


Need to use Meraj's airtable key file -- The key lives in RecoProcesses
All the paths for different processes are hard coded in All Modules. 
If one need's to run Jarvis for Processing on PCICITFNAL01, uncomment the paths in AllModules for PCICITFNAL01 and comment out the paths for timingdaq02
If the scope list 
Remember to enable messages from otsdaq configuration on udp communication. To know when OTSDAQ goes inot a failed state.
Instructions for running the AutoPilot:



Starting new autoPilot:
1. Make configurations on AirTable for each device.
2. Make global configuration pointing to every device config.
3. ./runAutoPilot.sh specifying global configuration number.

	Make sure listeners are running for each device:
		DT: TimingController
		Scope: readScopeStatus.py

NEVER kill autopilot during a run. Wait for run to complete.