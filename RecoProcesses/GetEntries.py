import ROOT
import sys

def RunEntries(FileLocation):

	f = ROOT.TFile.Open(FileLocation)
	if hasattr(f, 'pulse'):
		##### Number of Entries with Tracks
		EntriesWithTrack = f.pulse.GetEntries("ntracks==1&&nplanes>=19")
		##### Number of Entries with Tracks and hit in one or more of the three channels
		EntriesWithTrackAndHit = f.pulse.GetEntries("ntracks==1&&nplanes>=19&&(amp[0]>20||amp[1]>20||amp[2]>20)")
		##### Number of Entries with a hit 
		EntriesWithHit = f.pulse.GetEntries("amp[0]>20||amp[1]>20||amp[2]>20")
		##### Number of tracks without nplanes condition
		EntriesWithTrackWithoutNplanes = f.pulse.GetEntries("ntracks==1")
		return EntriesWithTrack, EntriesWithTrackAndHit, EntriesWithHit, EntriesWithTrackWithoutNplanes
	else:
		return -1,-1,-1,-1