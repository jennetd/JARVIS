# /usr/bin/python

#Author: Ben Tannenwald
#Date: April 18, 2019
#Purpose: Script to wrap Andrea's analysis code

import os,sys, argparse

# *** 0. setup parser for command line
parser = argparse.ArgumentParser()
parser.add_argument("--bar", help="which bar to process, e.g. box1, box2, box3, single")
parser.add_argument("--firstRun", help="first run to analyze")
parser.add_argument("--lastRun", help="last run to analyze")
parser.add_argument("--timeAlgo", help="time fitting algorithm", default="LP2_30")
parser.add_argument("--isCondor", help="flag to turn off display of plots for condor submission")
args = parser.parse_args()

if len(sys.argv)==1: # no options, easy way to get help
    os.system('python analyzeBarForTiming.py -h')
    quit()

# ** A. Test bar option and exit if unexpected
if(args.bar is None):
    print "#### Need to bar to analyze using --bar <box1/box2/box3/single> ####\nEXITING"
    quit()
else:
    if (args.bar == "box1" or args.bar == "box2" or args.bar == "box3" or args.bar == "single")==False:
        print "#### Need to bar to analyze using --bar <box1/box2/box3/single> ####\nEXITING"
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

# ** C. last run
if(args.lastRun is None):
    print "#### Need to specify last run to analyze --lastRun <run number###\nEXITING"
    quit()
else:
    if (args.lastRun).isdigit == False:
        print "#### Need to specify last run to analyze --lastRun <run number###\nEXITING"
        quit()
    else:
        print '-- Setting lastRun = {0}'.format(args.lastRun)

# ** D. time Algolast run
if(args.timeAlgo == "IL_50"):
    print '-- Default timeAlgo = {0}'.format(args.timeAlgo)
else:
    print '-- Setting lastRun = {0}'.format(args.timeAlgo)


## *** 1. Parse together output directory and create if does not exist
## ** A. Top level directory of which runs
outputDir = 'Runs_'+args.firstRun+'to'+args.lastRun
if ( not os.path.exists(outputDir) ):
    print "Specified run directory {0} DNE.\nCREATING NOW".format(outputDir)
    os.system("mkdir {0}".format(outputDir))
# ** B. Sub-level directory of which bar
outputDir = outputDir + '/' + args.bar
if ( not os.path.exists(outputDir) ):
    print "Specified bar sub-directory {0} DNE.\nCREATING NOW".format(outputDir)
    os.system("mkdir {0}".format(outputDir))
# ** C. Sub-level directory of which time algorithm
outputDir = outputDir + '/' + args.timeAlgo + '/'
if ( not os.path.exists(outputDir) ):
    print "Specified timeAlgo sub-directory {0} DNE.\nCREATING NOW".format(outputDir)
    os.system("mkdir {0}".format(outputDir))

# *** 2. Run code
if args.isCondor == "true" or args.isCondor == "True":
    os.system("""root -l -q -b 'analyze_FNAL.C("{0}", {1}, {2}, "{3}", "{4}", "True")'""".format(args.bar, args.firstRun, args.lastRun, args.timeAlgo, outputDir))
else:
    os.system("""root -l -q 'analyze_FNAL.C("{0}", {1}, {2}, "{3}", "{4}")'""".format(args.bar, args.firstRun, args.lastRun, args.timeAlgo, outputDir))

