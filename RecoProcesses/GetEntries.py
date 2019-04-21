import ROOT
import sys

def RunEntries(FileLocation):

	f = ROOT.TFile.Open(FileLocation)
	if hasattr(f, 'pulse'):
		##### Number of Entries with Tracks
		EntriesWithTracks = f.pulse.GetEntries("ntracks==1&&nplanes>=19")
		##### Number of Entries with Tracks and hit in one or more of the three channels
		EntriesWithTracksAndHit = f.pulse.GetEntries("ntracks==1&&nplanes>=19&&(amp[0]>20||amp[1]>20||amp[2]>20)")
		##### Number of Entries with Tracks and hit in the photek
		EntriesWithTracksAndPhotekHit = f.pulse.GetEntries("ntracks==1&&nplanes>=19&&amp[3]>30")
		return EntriesWithTracks, EntriesWithTracksAndHit, EntriesWithTracksAndPhotekHit
	else:
		return -1,-1,-1