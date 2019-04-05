IncludeTelescope=1
IncludeVME=0
IncludeSampic=0
IncludeDesktopDRS=1
IncludeTekScope=0
IncludeKeysightScope=1
SensorConfigurationNumber=1
DAQConfigurationNumber=1


python AutoPilot.py -it $IncludeTelescope -iv $IncludeVME -is $IncludeSampic -its $IncludeTekScope -iks $IncludeKeysightScope -idt $IncludeDesktopDRS -se $SensorConfigurationNumber -conf $DAQConfigurationNumber

