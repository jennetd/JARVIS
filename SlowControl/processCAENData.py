from glob import glob
from datetime import datetime
import time as t
import ROOT
from array import array


CAENUnsyncLocalPath = '/home/daq/SurvivalBeam2021/JARVIS/SlowControl/CAENLogs/'

#outputtag= "batch_12-5"
#outputtag= "batch_three_day_two"
outputtag= "death_batch" 
#StartDate_ = '[2021-12-05T01:00:00]:'
#EndDate_ = '[2021-12-06T01:00:00]:'
StartDate_ = '[2021-12-05T23:00:00]:'
EndDate_ = '[2021-12-06T08:00:00]:'
#StartDate_ = '[2021-12-05T21:30:00]:'
#EndDate_ = '[2021-12-05T22:00:00]:'


outputtag= "death_slot19"
StartDate_ = '[2021-12-05T04:30:00]:'                                                                                                                                                                                                       
EndDate_ = '[2021-12-05T05:30:00]:'  
ROOT.gROOT.SetBatch(True)
outputdir = "CAENPlots/"

sensorNames = {
    'ch0':'FBK W7 8e14', 'ch1':'FBK W7 1.5e15', 'ch2':'FBK W13 8e14','ch3':'FBK W13 1.5e15',
    'ch4':'Board111 NC', 'ch5':'Board112 NC', 'ch6':'Board113 NC', 'ch7':'Board16', 'ch8':'Board7', 'ch9':'B30 NC'
    }

def getDateTime(date):
    return datetime.strptime(date, "[%Y-%m-%dT%H:%M:%S]:")

def to_seconds(date):
    return t.mktime(date.timetuple())

def dict_merge(y, x):
    for k, v in x.items(): 
        if k in y.keys(): 
            y[k] += v 
        else: 
            y[k] = v 
    return y

def parseCAENline(l):
    data = l.split()
    timeStamp = float(data[1][:-1])
    channelV = {}
    channelI = {}

    for i in range(1,len(data)-1):
        splitData = data[i][:-1].split("_")
        if(len(splitData) is 1): 
            continue
        else:
            if splitData[0] is 'V':
                channelV["ch"+splitData[2]] = [float(data[i+1][:-1])]
            elif splitData[0] is 'I':
                channelI["ch"+splitData[2]] = [float(data[i+1][:-1])]

    return {"time":timeStamp, "V":channelV, "I":channelI}

def drawTimeHisto(Ymax, Yname, time, plotLog, pdfName, startTime,endTime):
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
    h.GetXaxis().SetTitle("Time since %s [hrs]"%StartDate_)
    h.GetYaxis().SetTitle(Yname)
    h.Draw()
    
    colors = [
        ROOT.kAzure+4, ROOT.kRed, ROOT.kBlack, 
        ROOT.kGreen+2, ROOT.kMagenta, ROOT.kCyan+1, ROOT.kBlue,
        ROOT.kOrange, ROOT.kRed+2, ROOT.kYellow+2,
        ROOT.kAzure+4, ROOT.kRed, ROOT.kBlack, 
        ROOT.kGreen+2, ROOT.kMagenta, ROOT.kCyan+1, ROOT.kBlue,
        ROOT.kOrange, ROOT.kRed+2, ROOT.kYellow+2,
        ROOT.kAzure+4, ROOT.kRed, ROOT.kBlack, 
        ROOT.kGreen+2, ROOT.kMagenta, ROOT.kCyan+1, ROOT.kBlue,
        ROOT.kOrange, ROOT.kRed+2, ROOT.kYellow+2,
    ]
    history = []
    for i, channel in enumerate(plotLog):
        g = None
        #if not channel is "ch2": continue
        try:
            g = ROOT.TGraph(len(time), array('d', time), array('d', plotLog[channel]))
        except:
            print "-------------------------"
            print "Warning: No Data for ", channel, plotLog[channel]
            print "-------------------------"
            continue
        #g.SetLineStyle(ROOT.kDashed)
        g.SetLineColor(colors[i])
        g.SetMarkerColor(colors[i])
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
    files = glob(CAENUnsyncLocalPath+"/*.txt")
    startTime = to_seconds(getDateTime(StartDate_))
    endTime = to_seconds(getDateTime(EndDate_)) if EndDate_ else to_seconds(datetime.now()) + 3600

    # Loop through all log files and collect the data
    data = []
    for i, name in enumerate(files):
        f = open(name, 'r')
        rl = f.readlines()
        print("Open file {} {} of {} with {} lines".format(name, i, len(files), len(rl)))
        for line in rl:
            l = line.strip()
            d = parseCAENline(l)
            if d:
                data.append(d)

    time = []
    allChannelV = None
    allChannelI = None
    for d in data:
        time.append((d["time"] - startTime)/3600.0)

        if allChannelV:
            allChannelV = dict_merge(allChannelV, d['V'])
        else:
            allChannelV = d['V']

        if allChannelI:
            allChannelI = dict_merge(allChannelI, d['I'])
        else:
            allChannelI = d['I']

    # Get log data
    #currentLog = {"ch"+i:{'x':[],'y':[],'color':color} for i, color in channelInfo}
    #voltageLog = {"ch"+i:{'x':[],'y':[],'color':color} for i, color in channelInfo}
    #for d in data:
    #    channel = "ch"+str(d["ch"])
    #    #if outputtag== "batch_one_set_one":
    #   # if channel!="ch0" and channel!="ch1" and channel!="ch4" and channel!="ch6":continue
    #    if to_seconds(d["ETLTimeStamp"]) < to_seconds(getDateTime(StartDate_)): continue
    #    if EndDate_ is not None and to_seconds(d["ETLTimeStamp"]) > to_seconds(getDateTime(EndDate_)): continue
    #    if channel not in currentLog.keys(): continue
    #
    #    t_sec = to_seconds(d["ETLTimeStamp"]) - startTime
    #    if d['par'] == "IMonH" or d['par'] == "IMon":                
    #        currentLog[channel]['x'].append(t_sec/3600.)
    #        currentLog[channel]['y'].append(d['val'])
    #    elif d['par'] == "VMon":                
    #        voltageLog[channel]['x'].append(t_sec/3600.)
    #        voltageLog[channel]['y'].append(d['val'])
    
    # Draw histograms
    drawTimeHisto(180.0, "Current [#muA]", time, allChannelI, "%s/current_%s.png" % (outputdir,outputtag), startTime,endTime)
    drawTimeHisto(800.0, "Voltage [V]", time, allChannelV, "%s/voltage_%s.png" % (outputdir,outputtag), startTime,endTime)
    #
    ##draw1D("current channel 3", currentLog['ch3']['y'], 100, 0.0, 70.0, "%s/current_ch3_1D_%s.pdf" % (outputdir,outputtag))
    ##draw1D("current channel 4", currentLog['ch4']['y'], 100, 0.0, 70.0, "%s/current_ch4_1D_%s.pdf" % (outputdir,outputtag))
    #
    #
    ##dataIV = {"ch"+i:{'data':None,'color':color} for i, color in channelInfo}
    ##for channel in currentLog.keys():
    ##    data = {'I':[],'V':[]}
    ##    for i in range(len(currentLog[channel]['x'])):
    ##        val1=currentLog[channel]['y'][i]
    ##        time1=currentLog[channel]['x'][i]
    ##        bestMatchInfo = (999,-1,999)
    ##        for j in range(len(voltageLog[channel]['x'])):
    ##            time2=voltageLog[channel]['x'][j]
    ##            val2=voltageLog[channel]['y'][j]
    ##            deltaT = time1 - time2
    ##            if(deltaT < bestMatchInfo[0] and deltaT >= 0):
    ##                bestMatchInfo = (deltaT, j, val2)
    ##        data['I'].append(val1)
    ##        data['V'].append(bestMatchInfo[2])                
    ##    dataIV[channel]['data'] = data
    ##
    ##drawIV("Voltage [V]", "Current [uA]", dataIV, "%s/IV_%s.png" % (outputdir,outputtag))


if __name__ == '__main__':
    main()
