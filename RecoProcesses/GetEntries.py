import ROOT
import sys

def RunEntries(FileLocation):

	# f = ROOT.TFile.Open(FileLocation)
	# f = ROOT.TFile.Open(FileLocation)
	chain = ROOT.TChain("pulse")
	chain.Add(FileLocation)
	# if hasattr(f, 'pulse'):
	##### Number of Entries with Tracks
	EntriesWithTrack = chain.GetEntries("ntracks==1&&npix>0&&nplanes>10")
	##### Number of tracks without nplanes condition
	EntriesWithTrackWithoutNplanes = chain.GetEntries("ntracks==1&&nplanes>10")


	##### Number of Entries with Tracks and hit in one or more of the three channels
	str_channels = "amp[1]>70"

	EntriesWithTrackAndHit = chain.GetEntries("ntracks==1&&npix>0&&nplanes>10&&({})".format(str_channels))
	# EntriesWithTrackAndHit = chain.GetEntries("ntracks==1&&npix>0&&nback>1&&(amp[0]>20||amp[1]>20||amp[2]>20)")
	##### Number of Entries with a hit 
	EntriesWithHit = chain.GetEntries(str_channels)
	# EntriesWithHit = chain.GetEntries("amp[0]>20||amp[1]>20||amp[2]>20")

	hits_ch1 = chain.GetEntries("amp[0]>20")
	hits_ch2 = chain.GetEntries("amp[1]>20")
	hits_ch3 = chain.GetEntries("amp[2]>20")
	hits_ch4 = chain.GetEntries("amp[3]>20")

	return EntriesWithTrack, EntriesWithTrackAndHit, EntriesWithHit, EntriesWithTrackWithoutNplanes,hits_ch1,hits_ch2,hits_ch3,hits_ch4
	# else:
	# 	return -1,-1,-1,-1
