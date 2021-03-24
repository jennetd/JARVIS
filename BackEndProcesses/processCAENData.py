from glob import glob
from datetime import datetime
import time as t
import ROOT
from array import array


#outputtag= "splti3_625V"
#StartDate_ = '[2020-12-22T14:05:00]:'

#EndDate_ = None #'[2020-12-20T14:00:00]:'
outputtag= "prebeam"
StartDate_ = '[2020-12-18T1:00:00]:'
EndDate_ = '[2020-12-19T14:00:00]:'
#outputtag= "firstbeam"
#StartDate_ = '[2020-12-20T14:00:00]:'
# EndDate_ = '[2020-12-20T19:30:00]:'
#outputtag= "secondbeam"
#StartDate_ = '[2020-12-21T18:30:00]:'
#EndDate_ = '[2020-12-21T23:59:00]:'
#EndDate_ = '[2020-12-22T01:30:00]:' 
#outputtag= "thirdbeam"
#StartDate_ = '[2020-12-22T9:55:00]:'
#EndDate_ = '[2020-12-22T15:30:00]:'
#EndDate_ = None

#outputtag="split2death"
#StartDate_= '[2020-12-21T18:30:06]:'
#EndDate_='[2020-12-22T01:30:06]:'
ROOT.gROOT.SetBatch(True)
CAENUnsyncLocalPath = '/home/daq/LabviewData/CAENUnsyncData/CAENData/'
CAENUnsyncLocalPath = '/home/daq/CAEN_backup_december2021/'
outputdir = "CAENPlots/"
#StartDate_ = '[2020-12-19T13:00:00]:'

def getDateTime(date):
    return datetime.strptime(date, "[%Y-%m-%dT%H:%M:%S]:")

def to_seconds(date):
    return t.mktime(date.timetuple())

def parseCAENline(l):
    data = l.split()
    timeStamp = data[0].split('T')
    ETLTimeStamp = getDateTime(data[0])
    #StartDate = getDateTime(StartDate_)
    #print ETLTimeStamp, to_seconds(ETLTimeStamp) - to_seconds(StartDate), t.time() - to_seconds(StartDate)
    date = list(int(i) for i in timeStamp[0][1:].split('-'))
    time = list(int(i) for i in timeStamp[1][:-2].split(':'))
    return {"date":date, "time":time, "ch":int(data[5][1:-1]), "par":data[7][1:-1], "val":float(data[9][1:-2]), "ETLTimeStamp":ETLTimeStamp}

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
        if channel == "ch1" or channel=="ch6": continue
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
        g.Draw("LP same")
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
    files = glob(CAENUnsyncLocalPath+"/*.log")
    startTime = to_seconds(getDateTime(StartDate_))
    endTime = to_seconds(getDateTime(EndDate_))

    # Loop through all log files and collect the data
    data = []
    for name in files:
        f = open(name, 'r')
        for line in f.readlines():
            l = line.strip()
            d = parseCAENline(l)
            data.append(d)

    # Get log data
    channelInfo = [("1",ROOT.kRed),("2",ROOT.kBlack),("3",ROOT.kCyan),("4",ROOT.kMagenta),("5",ROOT.kGreen+2),("6",ROOT.kBlue)]
    currentLog = {"ch"+i:{'x':[],'y':[],'color':color} for i, color in channelInfo}
    voltageLog = {"ch"+i:{'x':[],'y':[],'color':color} for i, color in channelInfo}
    for d in data:
        channel = "ch"+str(d["ch"])
        if to_seconds(d["ETLTimeStamp"]) < to_seconds(getDateTime(StartDate_)): continue
        if EndDate_ is not None and to_seconds(d["ETLTimeStamp"]) > to_seconds(getDateTime(EndDate_)): continue
        if channel not in currentLog.keys(): continue

        t_sec = to_seconds(d["ETLTimeStamp"]) - startTime
        if d['par'] == "IMonH":                
            currentLog[channel]['x'].append(t_sec/3600.)
            currentLog[channel]['y'].append(d['val'])
        elif d['par'] == "VMon":                
            voltageLog[channel]['x'].append(t_sec/3600.)
            voltageLog[channel]['y'].append(d['val'])

    # Draw histograms
    drawTimeHisto(60.0, "Current [#muA]", currentLog, "%s/current_%s.png" % (outputdir,outputtag), startTime,endTime)
    drawTimeHisto(800.0, "Voltage [V]", voltageLog, "%s/voltage_%s.png" % (outputdir,outputtag), startTime,endTime)

#    draw1D("current channel 3", currentLog['ch3']['y'], 100, 0.0, 70.0, "%s/current_ch3_1D_%s.pdf" % (outputdir,outputtag))
 #   draw1D("current channel 4", currentLog['ch4']['y'], 100, 0.0, 70.0, "%s/current_ch4_1D_%s.pdf" % (outputdir,outputtag))

if __name__ == '__main__':
    main()
