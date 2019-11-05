# J.A.R.V.I.S.


Need to use Meraj's airtable key file -- The key lives in RecoProcesses
All the paths for different processes are hard coded in All Modules. 
If one need's to run Jarvis for Processing on PCICITFNAL01, uncomment the paths in AllModules for PCICITFNAL01 and comment out the paths for timingdaq02
If the scope list 
Remember to enable messages from otsdaq configuration on udp communication. To know when OTSDAQ goes inot a failed state.
Instructions for running the AutoPilot:



Starting AutoPilot for the first time:

1) 	Make configurations on AirTable for each device.
2) 	Make global configuration pointing to every device config.
3) 	Source the otsdaq, and launch the ots server if not already done:
		Go to cmstiming@ftbf-daq-08
		In the home directory do
				source cmstiming_setup.sh
		Launch the OTS server using the command
				ots 
4) 	Go to otsdaq webpage and make sure the otsdaq is correctly configured for all the digitizers in the otsdaq configuration.
5) 	Now run the listeners for different digitizers.
			* For DT5742:
				ssh daq@192.168.133.167
				Do -- cd lorenzo/TimingBone/ 
				Do -- ./TimingController
				Make sure it says on the screen that it binds to the socket, if it doesn't then probably the listener is already running somewhere else. 
			* For VME:

			* For KeySightScope:
				ssh -XY daq@timingdaq02.dhcp.fnal.gov
				Go to /home/daq/JARVIS/BackEndProcesses/
				Open readScopeStatus.py and adjust the scope acquisition parameters.
				Through remote desktop make sure the scope is ready for acquisition
				To setup the environment for the listener, do
					source ~/otsdaq/setup_ots.sh
				Now start the listener using
				 	python readScopeStatus.py
6)	Go back to otsdaq webpage to initialize and configure the otsdaq.
7)	Now to run the autopilot:
		ssh -XY daq@timingdaq02.dhcp.fnal.gov 
		Go to /home/daq/JARVIS/AutoPilot
		./runAutoPilot.sh <Global Configuration number> 	example: ./runAutoPilot.sh 1


To stop the Autopilot:

1) Go to /home/daq/JARVIS/AutoPilot on timingdaq02. 
2) Run ./StopAutoPilot.sh






NEVER kill autopilot during a run. Wait for run to complete. It won't make an entry in the run table.
