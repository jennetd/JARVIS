import os
import ROOT as rt

def MakeXYEffPlots(mytree, ChannelAmpThresholdDict, outputDir, Label):
    
    if mytree is None:
        print "tree not found"
    else :
        for channel in ChannelAmpThresholdDict :

            print "Channel " + str(channel)

            #make canvas
            mycanvas = rt.TCanvas("cv","cv",800,600)
            mytree.Draw("amp["+str(channel)+"]>"+str(ChannelAmpThresholdDict[channel])+":y_dut[0]:x_dut[0]","ntracks==1","profcolz");

            mycanvas.SaveAs(outputDir+"/EffXY_" + Label + "_CH"+str(channel)+".png")

