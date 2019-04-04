UseOTSDAQ=1
IncludeTelescope=1
IncludeVME=0
IncludeSampic=0
IncludeDesktopDRS=1
IncludeTekScope=0
IncludeKeysightScope=0
SensorConfigurationNumber=1
DAQConfigurationNumber=1


python AutoPilot2.py -io $UseOTSDAQ -it $IncludeTelescope -iv $IncludeVME -is $IncludeSampic -its $IncludeTekScope -iks $IncludeKeysightScope -idt $IncludeDesktopDRS -se $SensorConfigurationNumber -conf $DAQConfigurationNumber

