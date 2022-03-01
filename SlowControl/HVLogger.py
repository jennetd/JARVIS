import os
import signal

while True:
    code = os.system("ReadAll -c ~/power_supply/config/BurnInBoxPowerSupply.xml -d 10 -n 10000")
    if code == signal.SIGINT: break
