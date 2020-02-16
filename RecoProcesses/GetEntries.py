import ROOT
import sys

def RunEntries(FileLocation):

	# f = ROOT.TFile.Open(FileLocation)
	# f = ROOT.TFile.Open(FileLocation)
	chain = ROOT.TChain("pulse")
	chain.Add(FileLocation)
	# if hasattr(f, 'pulse'):
	##### Number of Entries with Tracks
	EntriesWithTrack = chain.GetEntries("ntracks==1&&npix>0&&nback>0")
	##### Number of tracks without nplanes condition
	EntriesWithTrackWithoutNplanes = chain.GetEntries("ntracks==1")


	##### Number of Entries with Tracks and hit in one or more of the three channels
	EntriesWithTrackAndHit = chain.GetEntries("ntracks==1&&npix>0&&nback>0&&(amp[0]>20||amp[1]>20||amp[2]>20)")
	##### Number of Entries with a hit 
	EntriesWithHit = chain.GetEntries("amp[0]>20||amp[1]>20||amp[2]>20")

	return EntriesWithTrack, EntriesWithTrackAndHit, EntriesWithHit, EntriesWithTrackWithoutNplanes
	# else:
	# 	return -1,-1,-1,-1