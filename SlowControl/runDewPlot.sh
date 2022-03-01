#!/bin/bash

python plotDewPoint.py
scp dewPoint_prebeam.png daq@timingdaq02.dhcp.fnal.gov:/home/daq/.
