# /usr/bin/python

#Author: Ben Tannenwald
#Date: April 18, 2019
#Purpose: Script to wrap Andrea's analysis code

import os,sys, argparse

# *** 0. setup parser for command line
parser = argparse.ArgumentParser()
parser.add_argument("--bar", help="which bar to process, e.g. box1, box2, box3, bar")
parser.add_argument("--firstRun", help="first run to analyze")
parser.add_argument("--lastRun", help="last run to analyze")
args = parser.parse_args()

if (len(vars(args)) != 3): # 3 --> three: one for each options
    os.system('python submitSampleToCondor.py -h')
    quit()

# ** A. Test bar option and exit if unexpected
if(args.bar is None):
    print "#### Need to bar to analyze using --bar <Box1/Box2/Box3/Bar> ####\nEXITING"
    quit()
else:
    if (args.bar == "box1" or args.bar == "box2" or args.bar == "box3" or args.bar == "bar")==False:
        print "#### Need to bar to analyze using --bar <Box1/Box2/Box3/Bar> ####\nEXITING"
        quit()
    else:
        print '-- Setting  bar = {0}'.format(args.bar)

# ** B. first run
if(args.firstRun is None):
    print "#### Need to specify first run to analyze --firstRun <run number###\nEXITING"
    quit()
else:
    if (args.firstRun).isdigit == False:
        print "#### Need to specify first run to analyze --firstRun <run number###\nEXITING"
        quit()
    else:
        print '-- Setting firstRun = {0}'.format(args.firstRun)

# ** B. last run
if(args.lastRun is None):
    print "#### Need to specify last run to analyze --lastRun <run number###\nEXITING"
    quit()
else:
    if (args.lastRun).isdigit == False:
        print "#### Need to specify last run to analyze --lastRun <run number###\nEXITING"
        quit()
    else:
        print '-- Setting lastRun = {0}'.format(args.lastRun)



# *** 1. run code
os.system("""root -l 'analyze_FNAL.C("{0}", {1}, {2})'""".format(args.bar, args.firstRun, args.lastRun))
