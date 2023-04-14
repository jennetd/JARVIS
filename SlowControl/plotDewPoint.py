from glob import glob
from datetime import datetime
import time as t
import ROOT
from array import array
import numpy as np

outputtag= "batch3install"
#StartDate_ = '[2023-04-12T21:00:00]:'
StartDate_ = '[2023-04-13T20:00:00]:'
EndDate_ = '[2023-04-13T23:00:00]:'


# outputtag = "batch_one_set_one"
# StartDate_ = '[2021-03-26T18:00:00]:'
# EndDate_ = None

ROOT.gROOT.SetBatch(True)

colors = {9:ROOT.kGreen+2,16:ROOT.kGreen+2,17:ROOT.kGreen+2,18:ROOT.kCyan+1,19:ROOT.kMagenta+2,14:ROOT.kBlack,15:ROOT.kYellow+1,20:ROOT.kOrange+1,21:ROOT.kWhite,22:ROOT.kWhite}

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

def Resistance_calc(T): #Function to calculate resistance for any temperature                                                                                                                                                                 
    R0 = 100 #Resistance in ohms at 0 degree celsius                                                                                                                                                                                          
    alpha = 0.00385
    Delta = 1.4999 #For pure platinum                                                                                                                                                                                                         
    if T < 0:
        Beta = 0.10863
    elif T > 0:
        Beta = 0
    RT = (R0 + R0*alpha*(T - Delta*(T/100 - 1)*(T/100) - Beta*(T/100 - 1)*((T/100)**3)))*100
    return RT

#### for FNAL 16 ch board
def Temp_calc(R): #Function to calculate temperature for any resistance                                                                                                                                                                       
    Temp_x = np.linspace(-30, 30, num=100) #Points to be used for interpolation                                                                                                                                                               
    Resis_y = np.array([])
    for i in range(len(Temp_x)):
        Resis_y = np.append(Resis_y,Resistance_calc(Temp_x[i]))
    Temperature_R = np.interp(R, Resis_y, Temp_x)
    #plt.plot(Temp_x, Resis_y, 'o')                                                                                                                                                                                                           
    #plt.show()                                                                                                                                                                                                                               
    return Temperature_R

def parseDewPointline(l):
    data = l.split()
    timeStamp = data[0]
    boardTemps = {}
    for i in range(1,len(data)-1):
        val = float(data[i])
        if val != 0.0 and val < 1000.0:
            boardTemps[i] = [val]
    #ETLTimeStamp = getDateTime(data[0])
    #StartDate = getDateTime(StartDate_)
    #print ETLTimeStamp, to_seconds(ETLTimeStamp) - to_seconds(StartDate), t.time() - to_seconds(StartDate)
    #date = list(int(i) for i in timeStamp[0][1:].split('-'))
    #time = list(int(i) for i in timeStamp[1][:-2].split(':'))
    #return {"date":date, "time":time, "ch":int(data[5][1:-1]), "par":data[7][1:-1], "val":float(data[9][1:-2]), "ETLTimeStamp":ETLTimeStamp}
    return {"ch":1,"val":float(data[-1]), "time":float(data[0]), "boardTemps":boardTemps}

def plotTGraph(l, x, y, color):
    g = ROOT.TGraph(l, x, y)
    #g.SetLineStyle(ROOT.kDashed)
    g.SetLineColor(color)
    g.SetMarkerColor(color)
    g.SetMarkerStyle(20)
    g.SetMarkerSize(0.6)
    return g

def drawTimeHisto(Ymax, Yname, plotLog, pdfName, startTime, endTime, plotDict=None):
    c1 = ROOT.TCanvas("c1","c1",1000,1000)
    ROOT.gPad.SetGridy(); ROOT.gPad.SetGridx()
    ROOT.gPad.SetTopMargin(0.15)
    ROOT.gPad.SetLeftMargin(0.15)
    ROOT.gPad.SetBottomMargin(0.15)
    ROOT.gPad.SetRightMargin(0.15)

    legend = ROOT.TLegend(0.9, 0.6, 1.0, 0.8)
    
    Xmin = 0.0
    Xmax = (endTime - startTime)/3600.
    Ymin = -60.0
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
        try:
            g = plotTGraph(len(plotLog[channel]['x']), array('d', plotLog[channel]['x']), array('d', plotLog[channel]['y']), plotLog[channel]["color"])
        except:
            print("-------------------------")
            print("Warning: No Data for ", channel, plotLog[channel])
            print("-------------------------")
            continue
        g.Draw("P same")
        history.append(g)
        legend.AddEntry(g, channel, "l")

    for channel in plotDict.keys():
        g1 = None
        try:
            #for i in range(len(plotDict[channel])):
            #    plotDict[channel][i] = Temp_calc(plotDict[channel][i])
            g1 = plotTGraph(len(plotLog['ch1']['x']), array('d', plotLog['ch1']['x']), array('d', plotDict[channel]), ROOT.kBlack)
        except:
            print("Broken lol")
            continue
        g1.SetMarkerColor(colors[channel])
        g1.Draw("P same")
        history.append(g1)
        legend.AddEntry(g1, str(channel), "p")

    legend.Draw()
    c1.Print(pdfName)

def main():
    dewPointLocalPath = "tempLogs"
    files = glob(dewPointLocalPath+"/*.txt")
    startTime = to_seconds(getDateTime(StartDate_))
    endTime = to_seconds(getDateTime(EndDate_)) if EndDate_ else to_seconds(datetime.now()) + 2*3600

    # Loop through all log files and collect the data
    data = []
    for name in files:
        f = open(name, 'r')
        for line in f.readlines():
            l = line.strip()
            d = parseDewPointline(l)
            data.append(d)

    # Get log data
    allBoardTemps = None
    channelInfo = [("1",ROOT.kRed)]
    dewpointLog = {"ch"+i:{'x':[],'y':[],'color':color} for i, color in channelInfo}
    for d in data:
        channel = "ch"+str(d["ch"])
        ETLTimeStamp = d["time"] + to_seconds(datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"))
        if ETLTimeStamp < to_seconds(getDateTime(StartDate_)): continue
        if EndDate_ is not None and ETLTimeStamp > to_seconds(getDateTime(EndDate_)): continue
    
        t_sec = d["time"] - startTime + to_seconds(datetime.strptime("2000-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"))

        dewpointLog[channel]['x'].append(t_sec/3600.)
        dewpointLog[channel]['y'].append(d['val'])

        if allBoardTemps:
            allBoardTemps = dict_merge(allBoardTemps, d['boardTemps'])
        else:
            allBoardTemps = d['boardTemps']

    # Draw histograms
    drawTimeHisto(50.0, "Temp. [C]", dewpointLog, "dewPoint_%s.png"%outputtag, startTime, endTime, allBoardTemps)

if __name__ == '__main__':
    main()
