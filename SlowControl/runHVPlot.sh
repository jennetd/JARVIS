#!/bin/bash

python processCAENData.py
scp CAENPlots//current_*.png daq@timingdaq02.dhcp.fnal.gov:/home/daq/.
scp CAENPlots//voltage_*.png daq@timingdaq02.dhcp.fnal.gov:/home/daq/.
