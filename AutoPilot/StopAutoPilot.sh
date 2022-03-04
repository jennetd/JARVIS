echo "stop" > AutoPilot.status
echo "ready" > /home/daq/SensorBeam2022/ScopeHandler/Lecroy/Acquisition/RunLog.txt
echo "0" > /home/daq/SensorBeam2022/ScopeHandler/Lecroy/Acquisition/ScopeStatus.txt
echo "The scope might still be acquiring. If it is, then it might be a screwed up run for the scope. This script will make the autopilot stop. 
Please make sure the scope is ready before you start the AutoPilot next."
