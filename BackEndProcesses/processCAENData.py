from glob import glob
from datetime import datetime
import time as t
import ROOT
from array import array

CAENUnsyncLocalPath = '/home/daq/LabviewData/CAENUnsyncData/CAENData/'

# outputtag= "prebeam"
# StartDate_ = '[2021-03-25T11:30:00]:'
# EndDate_ = '[2021-03-25T23:00:00]:'
# CAENUnsyncLocalPath = '/home/daq/LabviewData/CAENUnsyncData/CAENData/prebeam/'

# outputtag= "batch_one_set_one"
# StartDate_ = '[2021-03-26T17:00:00]:'
# EndDate_ = '[2021-03-27T01:00:00]:'
# CAENUnsyncLocalPath = '/home/daq/LabviewData/CAENUnsyncData/CAENData/batch_one/'

# outputtag= "batch_one_day_two"
# StartDate_ = '[2021-03-27T09:00:00]:'
# EndDate_ = '[2021-03-27T20:30:00]:'

#outputtag= "batch_one_day_three"
#StartDate_ = '[2021-03-28T08:00:00]:'
#EndDate_ = '[2021-03-28T13:30:00]:'

#outputtag= "prebeam_two"
#StartDate_ = '[2021-03-29T08:00:00]:'
#EndDate_ = '[2021-03-29T21:00:00]:'

#outputtag= "batch_two_day_one"
#StartDate_ = '[2021-03-30T08:00:00]:'
#EndDate_ = '[2021-03-31T22:00:00]:'

#outputtag= "prebeam_three"
#StartDate_ = '[2021-04-01T18:00:00]:'
#EndDate_ = '[2021-04-02T09:00:00]:'

# outputtag= "batch_three_day_one"
# StartDate_ = '[2021-04-02T08:00:00]:'
# EndDate_ = '[2021-04-03T09:00:00]:'


outputtag= "batch_three_day_two"
StartDate_ = '[2021-04-03T09:00:00]:'
EndDate_ = None

ROOT.gROOT.SetBatch(True)
#CAENUnsyncLocalPath = '/home/daq/LabviewData/CAENUnsyncData/CAENData/'
#CAENUnsyncLocalPath = '/home/daq/CAEN_backup_december2021/'
outputdir = "CAENPlots/"

sensorNames = {
    'ch0':'FBK W7 8e14', 'ch1':'FBK W7 1.5e15', 'ch2':'FBK W13 8e14','ch3':'FBK W13 1.5e15',
    'ch4':'Board111 NC', 'ch5':'Board112 NC', 'ch6':'Board113 NC', 'ch7':'Board16', 'ch8':'Board7', 'ch9':'B30 NC'
    }

def getDateTime(date):
    return datetime.strptime(date, "[%Y-%m-%dT%H:%M:%S]:")

def to_seconds(date):
    return t.mktime(date.timetuple())

def parseCAENline(l):
    data = l.split()
    try:
        timeStamp = data[0].split('T')
        if len(data[0]) < 10 or "[" not in data[0]: 
            raise(Exception, "Bad log line")
    except:
        return None
    ETLTimeStamp = getDateTime(data[0])
    #StartDate = getDateTime(StartDate_)
    #print ETLTimeStamp, to_seconds(ETLTimeStamp) - to_seconds(StartDate), t.time() - to_seconds(StartDate)
    date = list(int(i) for i in timeStamp[0][1:].split('-'))
    time = list(int(i) for i in timeStamp[1][:-2].split(':'))
    channelNum = int(data[5][1:-1])
    if data[1] == '[System(1)]':
        channelNum += 7
    return {"date":date, "time":time, "ch":channelNum, "par":data[7][1:-1], "val":float(data[9][1:-2]), "ETLTimeStamp":ETLTimeStamp}

def drawTimeHisto(Ymax, Yname, plotLog, pdfName, startTime,endTime):
    c1 = ROOT.TCanvas("c1","c1",1000,1000)
    ROOT.gPad.SetGridy(); ROOT.gPad.SetGridx()
    ROOT.gPad.SetTopMargin(0.15)
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetBottomMargin(0.15)
    ROOT.gPad.SetRightMargin(0.15)

    legend = ROOT.TLegend(0.9, 0.6, 1.0, 0.8)
    
    Xmin = 0.0
    Xmax = (endTime - startTime)/3600.
    Ymin = 0.0
    h = ROOT.TH1F("dummy","dummy",1, Xmin, Xmax)
    h.SetMaximum(Ymax)
    h.SetMinimum(Ymin)
    h.SetTitle("")
    h.SetStats(0)
    h.GetXaxis().SetLimits(Xmin,Xmax)
    h.GetXaxis().SetLabelSize(0.05)
    h.GetXaxis().SetTitleSize(0.05)
    h.GetXaxis().SetTitleOffset(1.3)
    h.GetYaxis().SetLabelSize(0.05)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetTitleOffset(1.3)
    h.GetXaxis().SetTitle("Time [hrs]")
    h.GetYaxis().SetTitle(Yname)
    h.Draw()
    
    history = []
    for channel in plotLog:
        g = None
        #if channel == "ch1" or channel=="ch6": continue
        try:
            g = ROOT.TGraph(len(plotLog[channel]['x']), array('d', plotLog[channel]['x']), array('d', plotLog[channel]['y']))
        except:
            print "-------------------------"
            print "Warning: No Data for ", channel, plotLog[channel]
            print "-------------------------"
            continue
        #g.SetLineStyle(ROOT.kDashed)
        g.SetLineColor(plotLog[channel]["color"])
        g.SetMarkerColor(plotLog[channel]["color"])
        g.SetMarkerStyle(20)
        g.SetMarkerSize(0.6)
        g.Draw("P same")
        history.append(g)
        legend.AddEntry(g, channel, "l")
    
    legend.Draw()
    c1.Print(pdfName)

def drawIV(Xname, Yname, dataIV, pdfName):
    c1 = ROOT.TCanvas("c1","c1",1000,1000)
    ROOT.gPad.SetGridy(); ROOT.gPad.SetGridx()
    ROOT.gPad.SetTopMargin(0.15)
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetBottomMargin(0.15)
    ROOT.gPad.SetRightMargin(0.15)

    legend = ROOT.TLegend(0.8, 0.5, 1.0, 0.8)
    
    ##Xmin = 0.0
    #Xmax = (endTime - startTime)/3600.
    Ymax = 60.0
    Ymin = 0.0
    #h = ROOT.TH1F("dummy","dummy",1, Xmin, Xmax)
    h = ROOT.TH1F("dummy","dummy",1, 0, 800)
    h.SetMaximum(Ymax)
    h.SetMinimum(Ymin)
    h.SetTitle("")
    h.SetStats(0)
    #h.GetXaxis().SetLimits(Xmin,Xmax)
    h.GetXaxis().SetLabelSize(0.05)
    h.GetXaxis().SetTitleSize(0.05)
    h.GetXaxis().SetTitleOffset(1.3)
    h.GetYaxis().SetLabelSize(0.05)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetTitleOffset(1.3)
    h.GetXaxis().SetTitle(Xname)
    h.GetYaxis().SetTitle(Yname)
    h.Draw()
    
    history = []
    for channel in dataIV:
        cIndex = int(channel.replace('ch',''))
        if cIndex >= 4: continue
        g = None
        #if channel == "ch1" or channel=="ch6": continue
        try:
            g = ROOT.TGraph(len(dataIV[channel]['data']['I']), array('d', dataIV[channel]['data']['V']), array('d', dataIV[channel]['data']['I']))
        except:
            print "-------------------------"
            print "Warning: No Data for ", channel, dataIV[channel]
            print "-------------------------"
            continue
        #g.SetLineStyle(ROOT.kDashed)
        g.SetLineColor(dataIV[channel]["color"])
        g.SetMarkerColor(dataIV[channel]["color"])
        g.SetMarkerStyle(20)
        g.SetMarkerSize(0.8)
        g.Draw("P same")
        history.append(g)
        legend.AddEntry(g, sensorNames[channel], "p")
    
    legend.Draw()
    c1.Print(pdfName)

def draw1D(histName, data, nbins, xlow, xhigh, pdfName):
    c1 = ROOT.TCanvas("c1","c1",1000,1000)
    ROOT.gPad.SetGridy(); ROOT.gPad.SetGridx()
    ROOT.gPad.SetTopMargin(0.15)
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetBottomMargin(0.15)
    ROOT.gPad.SetRightMargin(0.15)

    #Xmin = 0.0
    #Xmax = t.time() - startTime
    #Ymin = 0.0
    h = ROOT.TH1F(histName, histName, nbins, xlow, xhigh)
    for i in data:
        h.Fill(i)
    #h.SetMaximum(Ymax)
    #h.SetMinimum(Ymin)
    #h.SetTitle("")
    #h.SetStats(0)
    #h.GetXaxis().SetLimits(Xmin,Xmax)
    h.GetXaxis().SetLabelSize(0.05)
    h.GetXaxis().SetTitleSize(0.05)
    h.GetXaxis().SetTitleOffset(1.3)
    h.GetYaxis().SetLabelSize(0.05)
    h.GetYaxis().SetTitleSize(0.05)
    h.GetYaxis().SetTitleOffset(1.3)
    #h.GetXaxis().SetTitle("")
    #h.GetYaxis().SetTitle(Yname)
    h.Draw("hist")
    
    c1.Print(pdfName)

def main():
    files = glob(CAENUnsyncLocalPath+"/*.log")
    startTime = to_seconds(getDateTime(StartDate_))
    endTime = to_seconds(getDateTime(EndDate_)) if EndDate_ else to_seconds(datetime.now()) + 3600

    # Loop through all log files and collect the data
    data = []
    for name in files:
        f = open(name, 'r')
        for line in f.readlines():
            l = line.strip()
            d = parseCAENline(l)
            if d:
                data.append(d)

    # Get log data
    channelInfo = [
        ("0",ROOT.kAzure+4),("1",ROOT.kRed),("2",ROOT.kBlack),("3",ROOT.kGreen+2),("4",ROOT.kMagenta),("5",ROOT.kCyan+1),("6",ROOT.kBlue),
        ("7",ROOT.kOrange),("8",ROOT.kRed+2),("9",ROOT.kYellow+2),
    ]
    currentLog = {"ch"+i:{'x':[],'y':[],'color':color} for i, color in channelInfo}
    voltageLog = {"ch"+i:{'x':[],'y':[],'color':color} for i, color in channelInfo}
    for d in data:
        channel = "ch"+str(d["ch"])
        #if outputtag== "batch_one_set_one":
       # if channel!="ch0" and channel!="ch1" and channel!="ch4" and channel!="ch6":continue
        if to_seconds(d["ETLTimeStamp"]) < to_seconds(getDateTime(StartDate_)): continue
        if EndDate_ is not None and to_seconds(d["ETLTimeStamp"]) > to_seconds(getDateTime(EndDate_)): continue
        if channel not in currentLog.keys(): continue

        t_sec = to_seconds(d["ETLTimeStamp"]) - startTime
        if d['par'] == "IMonH" or d['par'] == "IMon":                
            currentLog[channel]['x'].append(t_sec/3600.)
            currentLog[channel]['y'].append(d['val'])
        elif d['par'] == "VMon":                
            voltageLog[channel]['x'].append(t_sec/3600.)
            voltageLog[channel]['y'].append(d['val'])

    # Draw histograms
    drawTimeHisto(105.0, "Current [#muA]", currentLog, "%s/current_%s.png" % (outputdir,outputtag), startTime,endTime)
    drawTimeHisto(1050.0, "Voltage [V]", voltageLog, "%s/voltage_%s.png" % (outputdir,outputtag), startTime,endTime)

    #draw1D("current channel 3", currentLog['ch3']['y'], 100, 0.0, 70.0, "%s/current_ch3_1D_%s.pdf" % (outputdir,outputtag))
    #draw1D("current channel 4", currentLog['ch4']['y'], 100, 0.0, 70.0, "%s/current_ch4_1D_%s.pdf" % (outputdir,outputtag))


    #dataIV = {"ch"+i:{'data':None,'color':color} for i, color in channelInfo}
    #for channel in currentLog.keys():
    #    data = {'I':[],'V':[]}
    #    for i in range(len(currentLog[channel]['x'])):
    #        val1=currentLog[channel]['y'][i]
    #        time1=currentLog[channel]['x'][i]
    #        bestMatchInfo = (999,-1,999)
    #        for j in range(len(voltageLog[channel]['x'])):
    #            time2=voltageLog[channel]['x'][j]
    #            val2=voltageLog[channel]['y'][j]
    #            deltaT = time1 - time2
    #            if(deltaT < bestMatchInfo[0] and deltaT >= 0):
    #                bestMatchInfo = (deltaT, j, val2)
    #        data['I'].append(val1)
    #        data['V'].append(bestMatchInfo[2])                
    #    dataIV[channel]['data'] = data
    #
    #drawIV("Voltage [V]", "Current [uA]", dataIV, "%s/IV_%s.png" % (outputdir,outputtag))


if __name__ == '__main__':
    main()
