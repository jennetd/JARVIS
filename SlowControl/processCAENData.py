from glob import glob
from datetime import datetime
import time as t
import ROOT
from array import array


CAENUnsyncLocalPath = '/home/daq/SensorBeam2022/JARVIS/SlowControl/CAENLogs/'

#outputtag= "batch_12-5"
#outputtag= "batch_three_day_two"
#outputtag= "death_batch" 
#StartDate_ = '[2021-12-05T01:00:00]:'
#EndDate_ = '[2021-12-06T01:00:00]:'
#StartDate_ = '[2021-12-05T23:00:00]:'
#EndDate_ = '[2021-12-06T08:00:00]:'
#StartDate_ = '[2021-12-05T21:30:00]:'
#EndDate_ = '[2021-12-05T22:00:00]:'


#outputtag= "death_slot19"
#StartDate_ = '[2021-12-05T04:30:00]:'                                                                                                                                                                                                       
#EndDate_ = '[2021-12-05T05:30:00]:' 

outputtag= "pre_beam"
StartDate_ = '[2022-04-23T00:00:00]:'                                                                                                                                                                                                       
EndDate_ = '[2022-04-23T23:00:00]:'  



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

def drawIV(Xmax, Ymax, Xname, Yname, V, I, pdfName):
    c1 = ROOT.TCanvas("c1","c1",1000,1000)
    ROOT.gPad.SetGridy(); ROOT.gPad.SetGridx()
    ROOT.gPad.SetTopMargin(0.15)
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetBottomMargin(0.15)
    ROOT.gPad.SetRightMargin(0.15)

    legend = ROOT.TLegend(0.9, 0.6, 1.0, 0.8)
    
    Xmin = 0.0
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
    h.GetXaxis().SetTitle(Xname)
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
    for i, channel in enumerate(V):
        g = None
        #if not channel is "ch2": continue
        try:
            g = ROOT.TGraph(len(V[channel]), array('d', V[channel]), array('d', I[channel]))
        except:
            print "-------------------------"
            print "Warning: No Data for ", channel, V[channel], I[channel]
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

    print(files)

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
    
    # Draw histograms
    drawTimeHisto(80.0, "Current [#muA]", time, allChannelI, "%s/current_%s.png" % (outputdir,outputtag), startTime,endTime)
    drawTimeHisto(720.0, "Voltage [V]", time, allChannelV, "%s/voltage_%s.png" % (outputdir,outputtag), startTime,endTime)

    drawIV(720.0, 80.0, "Voltage [v]", "Current [#muA]", allChannelV, allChannelI, "%s/IV_%s.png" % (outputdir,outputtag))

if __name__ == '__main__':
    main()
