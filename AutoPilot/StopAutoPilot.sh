echo "stop" > AutoPilot.status
echo "ready" > /home/daq/2019_04_April_CMSTiming/KeySightScope/ETL_Agilent_MSO-X-92004A/Acquisition/RunLog.txt
echo "The scope might still be acquiring. If it is, then it might be a screwed up run for the scope. This script will make the autopilot stop. 
Please make sure the scope is ready before you start the AutoPilot next."
