#source /home/daq/otsdaq/setup_ots.sh
import visa
import time
import sys
from datetime import datetime
import os
import signal

tempCMD = "MEAS:TEMP?"
resCMD  = "MEAS:RES?"

def getResourceDMM(debug=False):    
    # Setup resource that will talk to DMM
    rm = visa.ResourceManager('@py')

    # Connect to DMM and setup default settings
    #my_instrument = rm.open_resource('ASRL/dev/ttyUSB0::INSTR') #KEITHLEY INSTRUMENTS INC.,MODEL 2410,4105344,C33   Mar 31 2015 09:32:39/A02  /J/K
    #my_instrument = rm.open_resource('TCPIP0::192.168.133.159::inst0::INSTR') #KEYSIGHT TECHNOLOGIES,MSOX92004A,MY53240102,05.70.00901
    #my_instrument = rm.open_resource('TCPIP0::192.168.133.169::inst0::INSTR') #LECROY,WR8208HD,LCRY5003N60377,9.4.0
    #my_instrument = rm.open_resource('TCPIP::192.168.99.53::1394::SOCKET') #Keithley DMM
    my_instrument = rm.open_resource('TCPIP::192.168.133.163::1394::SOCKET') #Keithley DMM
    my_instrument.write("*RST; status:preset; *CLS")
    my_instrument.write("TEMP:TRAN FRTD")
    my_instrument.read_termination = '\n'
    my_instrument.write_termination = '\n'
    my_instrument.timeout = 5000
    my_instrument.baud_rate = 57600

    # Print stuff for debugging if needed
    if debug:
        print(rm.list_resources())
        print(my_instrument.query('*IDN?'))

    return my_instrument

def sendCMD(my_instrument, cmd):
    # Query intrument 
    val = str(my_instrument.query(cmd))
    time.sleep(0.5)
    val = val.split(",")[0].replace("+","")
    return val

def queryVal(my_instrument, cmd, typeRead):
    # Parse output of pyvisa and convert to float
    try:
        if typeRead == "temp":
            my_instrument.write("*RST; status:preset; *CLS")
            my_instrument.write("TEMP:TRAN FRTD") 
            val = sendCMD(my_instrument, cmd)
            val = float(val.replace(" C",""))
        elif typeRead == "amp":
            val = sendCMD(my_instrument, cmd)
            val = float(val.replace("ADC",""))
        else:
            val = sendCMD(my_instrument, cmd)
            val = float(val.replace("OHM",""))
    except:
        raise ValueError('Could not convert string to float: ', val)

    return val

def queryMultiVal(my_instrument, channels):
    t = round((datetime.now() - datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).total_seconds(), 3)
    vals = []
    for ch, doRead, cmd in channels:
        typeRead = "temp" if cmd == tempCMD else "res"
        val = 0
        if doRead:
            val = queryVal(my_instrument, "{0} (@{1})".format(cmd, ch), typeRead)
            #print ch, doRead, typeRead, cmd, val
        vals.append(val)

    line = "{:.13f}\t".format(t)
    for x in vals:
        line += "{:.13f}\t".format(x)

    return line

def progressbar(it, prefix="", size=60, file=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        file.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), j, count))
        file.flush()        
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    file.write("\n")
    file.flush()

def dewPoint(current=None):
    tempHigh = 20.0 # degrees C
    tempLow = -80.0 # degrees C
    currentHigh = 20.0 # mA 
    currentLow = 4.0 # mA
    m = (tempHigh-tempLow)/(currentHigh-currentLow)
    return m*(current-currentLow) + tempLow

def main():
    print("Start logging temp")
    my_instrument = getResourceDMM()
    print("Connected to multi-meter")

    entriesPerLogFile = 1000    
    minChannel = 94; maxChannel = 132
    f=None

    allChannels = [
        ( 94,False,tempCMD),( 95,False,tempCMD),( 96,False,tempCMD),( 97,False,tempCMD),( 98,False,tempCMD),( 99,False,tempCMD),(100,False,tempCMD),(101,False,tempCMD),
        (102,False,tempCMD),(103,False,tempCMD),(104,False,tempCMD),(105,False,tempCMD),(106,False,tempCMD),(107,False,tempCMD),(108,False,tempCMD),(109,False,tempCMD),
        (110,False,tempCMD),(111,False,tempCMD),(112,False,tempCMD),(113,False,resCMD) ,(114, True,resCMD) ,(115, True,resCMD) ,(116,False,tempCMD),(117,False,tempCMD),
        (119,False,tempCMD),(120,False,tempCMD),(121,False,tempCMD),(122,False,tempCMD),(123,False,tempCMD),(124,False,tempCMD),(125,False,tempCMD),(126,False,tempCMD),
        (127,False,tempCMD),(128,False,tempCMD),(129,False,tempCMD),(130,False,tempCMD),(131,False,tempCMD),(132,False,tempCMD),
    ]

    try:
        while True:

            ################# HV Logger #################################################

            code = os.system("ReadAll -c ~/power_supply/config/CAEN1527_PowerSupply_Timing.xml -d 10 -n 10000")
            #if code == signal.SIGINT: break #### should automatically break on keyboardInterrupt



            ################## DMM Logger ###############################################
        
            fileName = "tempLogs/lab_meas_unsync_{:.3f}.txt".format((datetime.now() - datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")).total_seconds())
            print("-"*50)
            print("Sending measured temperature to: {}".format(fileName))
        
    
            lineCounter = 0
            for lineCounter in progressbar(range(entriesPerLogFile), "  Filling log file: ", 40):
                #for lineCounter in range(entriesPerLogFile):
                #queryVal(my_instrument, 'MEAS:TEMP? (@112)','temp')
                #my_instrument.write("TEMP:TRAN FRTD")
                #line = queryMultiVal(my_instrument, 'MEAS:TEMP?', allChannels, "temp")
                #line = queryMultiVal(my_instrument, 'MEAS:RES?', allChannels,"res")
                line = queryMultiVal(my_instrument, allChannels)
                dewCurr = queryVal(my_instrument, 'MEAS:CURR? (@142)', 'amp')
                dp = dewPoint(dewCurr*1000.0)
                line += "\t"+str(dp)
                f = open(fileName,"a")
                f.write(line+"\n")
                f.close()
            
                fActive = open("temp_dew_active.txt","w")
                fActive.write(line+"\n")
                fActive.close()
                
                time.sleep(1)
                
    except KeyboardInterrupt:
        print("\nStopped the logging of HV and DMM")
        if f:
            f.close()
        pass


if __name__ == "__main__":
    main()

