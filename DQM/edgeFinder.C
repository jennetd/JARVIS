void printCanvas(TCanvas* _c0, string _outputDir, string _timeAlgo)
{
  _c0->Draw();
  TLatex* _algoLabel = new TLatex(0.74, 0.96, Form("%s", _timeAlgo.c_str()));
  _algoLabel->SetNDC(kTRUE);
  _algoLabel->SetTextFont(42);
  _algoLabel->SetTextSize(0.03);
  _algoLabel->Draw("same");
  _c0->Print( ( _outputDir + "/" + _c0->GetTitle() + "_" + _timeAlgo + ".png").c_str() );

  return;
}

int returnNumberOfBinsAboveAmpThreshold(TProfile* _tp0, double _threshold = 0.5)
{
  int _binsAboveThreshold = 0 ;

  for(int iBin=1; iBin < _tp0->GetNbinsX(); iBin++){
    if ( _tp0->GetBinContent(iBin) > _threshold ) 
      _binsAboveThreshold++;
  }

  return _binsAboveThreshold;

}

bool checkTrackingSynchronization(const char* _fileName)
{

  //TFile* _fileToCheck = new TFile( _fileName, "READ");
  TFile* _fileToCheck = TFile::Open( _fileName );
  if (_fileToCheck->GetListOfKeys()->Contains("pulse")==false)
    return false;

  TTree* _pulse = (TTree*)_fileToCheck->Get("pulse");
  
  TProfile* h_box1_L = new TProfile("h_box1_L", "h_box1_L", 30, 10, 35);
  TProfile* h_box1_R = new TProfile("h_box1_R", "h_box1_R", 30, 10, 35);
  TProfile* h_box2_L = new TProfile("h_box2_L", "h_box2_L", 30, 10, 35);
  TProfile* h_box2_R = new TProfile("h_box2_R", "h_box2_R", 30, 10, 35);
  TProfile* h_box3_L = new TProfile("h_box3_L", "h_box3_L", 30, 10, 35);
  TProfile* h_box3_R = new TProfile("h_box3_R", "h_box3_R", 30, 10, 35);
  TProfile* h_single_L = new TProfile("h_single_L", "h_single_L", 30, 10, 35);
  TProfile* h_single_R = new TProfile("h_single_R", "h_single_R", 30, 10, 35);
  
  _pulse->Draw("amp[1] > 400 :  y_dut[0]>>+h_box1_L", "ntracks==1");
  _pulse->Draw("amp[2] > 400 :  y_dut[0]>>+h_box2_L", "ntracks==1");
  _pulse->Draw("amp[3] > 400 :  y_dut[0]>>+h_box3_L", "ntracks==1");
  _pulse->Draw("amp[4] > 400 :  y_dut[0]>>+h_box1_R", "ntracks==1");
  _pulse->Draw("amp[5] > 400 :  y_dut[0]>>+h_box2_R", "ntracks==1");
  _pulse->Draw("amp[6] > 400 :  y_dut[0]>>+h_box3_R", "ntracks==1");
  _pulse->Draw("amp[19] > 200 : y_dut[0]>>+h_single_L", "ntracks==1");
  _pulse->Draw("amp[20] > 200 : y_dut[0]>>+h_single_R", "ntracks==1");

  int _nBinsForSyncedFlag = 2;
  bool found_box1_L = returnNumberOfBinsAboveAmpThreshold(h_box1_L) >= _nBinsForSyncedFlag ? true : false;
  bool found_box2_L = returnNumberOfBinsAboveAmpThreshold(h_box2_L) >= _nBinsForSyncedFlag ? true : false;
  bool found_box3_L = returnNumberOfBinsAboveAmpThreshold(h_box3_L) >= _nBinsForSyncedFlag ? true : false;
  bool found_box1_R = returnNumberOfBinsAboveAmpThreshold(h_box1_R) >= _nBinsForSyncedFlag ? true : false;
  bool found_box2_R = returnNumberOfBinsAboveAmpThreshold(h_box2_R) >= _nBinsForSyncedFlag ? true : false;
  bool found_box3_R = returnNumberOfBinsAboveAmpThreshold(h_box3_R) >= _nBinsForSyncedFlag ? true : false;
  bool found_single_L = returnNumberOfBinsAboveAmpThreshold(h_single_L) >= _nBinsForSyncedFlag ? true : false;
  bool found_single_R = returnNumberOfBinsAboveAmpThreshold(h_single_R) >= _nBinsForSyncedFlag ? true : false;

  // ** A. This is the tightest "goodness" condition possible. looser is potentially an option
  //if (found_box1_L == true && found_box2_L == true && found_box3_L == true && found_box1_R == true && found_box2_R == true && found_box3_R == true && found_single_L == true && found_single_R == true)
  // ** B. This checks tracking using box2+box3+single but skipping box1 (top bar in box)
  if (found_box2_L == true && found_box3_L == true && found_box2_R == true && found_box3_R == true && found_single_L == true && found_single_R == true)
    return true;
  
  return false;
}

void edgeFinder(string bar, const int& firstRun, const int& lastRun, string timeAlgo="LP2_30", string outputDir="./", string isCondor="")
{
  gStyle->SetPadTopMargin(0.05);
  gStyle->SetPadBottomMargin(0.13);
  gStyle->SetPadLeftMargin(0.13);
  gStyle->SetPadRightMargin(0.17);

  gStyle->SetTitleOffset(1.20, "X");
  gStyle->SetTitleOffset(1.80, "Y");
  gStyle->SetTitleOffset(1.60, "Z");
  
  
  //----------------
  // ntuple location
  //std::string dataFolder = "/eos/cms/store/group/dpg_mtd/comm_mtd/TB/MTDTB_FNAL_Nov2018/reco/v6/";
  //std::string dataFolder = "/data2/2019_04_April_CMSTiming/VME/RecoData/RecoWithTracks/v3/"; // BBT, 4-18-19, local
  std::string dataFolder = "/eos/uscms/store/group/cmstestbeam/2019_04_April_CMSTiming/VME/RecoData/RecoWithTracks/v3/"; // BBT, 4-18-19, LPC EOS
  if (isCondor=="True")
    dataFolder = "root://cmseos.fnal.gov//store/group/cmstestbeam/2019_04_April_CMSTiming/VME/RecoData/RecoWithTracks/v3/"; // BBT, 4-18-19, LPC EOS
  //std::string dataFolder = "/data2/2019_04_April_CMSTiming/VME/RecoData/RecoWithTracks/v3/";
  
  //----------------
  // define channels
  const int NCH = 3;
  
  int ampch_id [NCH];
  int timech_id[NCH];
  std::string namech[NCH];
  float ampmin_cut[NCH];
  float ampmax_cut[NCH];
  
  if (bar == "box1"){
    cout << bar << endl;
    ampch_id[0]  = 0; // digitizer index of reference channel (MCP)
    timech_id[0] = 0; // digitizer index of reference channel (MCP)
    namech[0] = "photek";
    ampmin_cut[0] = 50.;  //  low amp cut in mV (can be loose, dynamic selection on MIP peak below)
    ampmax_cut[0] = 850.; // high amp cut in mV (can be loose, dynamic selection on MIP peak below)
    
    ampch_id[1]  = 10; // digitizer index of 1st bar, left SiPM
    timech_id[1] = 1;  // digitizer index of 1st bar, left SiPM
    namech[1] = "top left";
    ampmin_cut[1] = 100.; //  low amp cut in mV (can be loose, dynamic selection on MIP peak below)
    ampmax_cut[1] = 500.; // high amp cut in mV (can be loose, dynamic selection on MIP peak below)
    
    ampch_id[2]  = 13; // digitizer index of 1st bar, right SiPM
    timech_id[2] = 4;  // digitizer index of 1st bar, right SiPM
    namech[2] = "top right";
    ampmin_cut[2] = 100.; //  low amp cut in mV (can be loose, dynamic selection on MIP peak below)
    ampmax_cut[2] = 500.; // high amp cut in mV (can be loose, dynamic selection on MIP peak below)
  }
  else if (bar == "box2"){
    cout << bar << endl;
    ampch_id[0]  = 0; // digitizer index of reference channel (MCP)
    timech_id[0] = 0; // digitizer index of reference channel (MCP)
    namech[0] = "photek";
    ampmin_cut[0] = 50.;  //  low amp cut in mV (can be loose, dynamic selection on MIP peak below)
    ampmax_cut[0] = 850.; // high amp cut in mV (can be loose, dynamic selection on MIP peak below)
    
    ampch_id[1]  = 11; // digitizer index of 1st bar, left SiPM
    timech_id[1] = 2;  // digitizer index of 1st bar, left SiPM
    namech[1] = "middle left";
    ampmin_cut[1] = 100.; //  low amp cut in mV (can be loose, dynamic selection on MIP peak below)
    ampmax_cut[1] = 500.; // high amp cut in mV (can be loose, dynamic selection on MIP peak below)
    
    ampch_id[2]  = 14; // digitizer index of 1st bar, right SiPM
    timech_id[2] = 5;  // digitizer index of 1st bar, right SiPM
    namech[2] = "middle right";
    ampmin_cut[2] = 100.; //  low amp cut in mV (can be loose, dynamic selection on MIP peak below)
    ampmax_cut[2] = 500.; // high amp cut in mV (can be loose, dynamic selection on MIP peak below)
  }
  else if (bar == "box3"){
    cout << bar << endl;
    ampch_id[0]  = 0; // digitizer index of reference channel (MCP)
    timech_id[0] = 0; // digitizer index of reference channel (MCP)
    namech[0] = "photek";
    ampmin_cut[0] = 50.;  //  low amp cut in mV (can be loose, dynamic selection on MIP peak below)
    ampmax_cut[0] = 850.; // high amp cut in mV (can be loose, dynamic selection on MIP peak below)
    
    ampch_id[1]  = 12; // digitizer index of 1st bar, left SiPM
    timech_id[1] = 3;  // digitizer index of 1st bar, left SiPM
    namech[1] = "bottom left";
    ampmin_cut[1] = 100.; //  low amp cut in mV (can be loose, dynamic selection on MIP peak below)
    ampmax_cut[1] = 500.; // high amp cut in mV (can be loose, dynamic selection on MIP peak below)
    
    ampch_id[2]  = 15; // digitizer index of 1st bar, right SiPM
    timech_id[2] = 6;  // digitizer index of 1st bar, right SiPM
    namech[2] = "bottom right";
    ampmin_cut[2] = 100.; //  low amp cut in mV (can be loose, dynamic selection on MIP peak below)
    ampmax_cut[2] = 500.; // high amp cut in mV (can be loose, dynamic selection on MIP peak below)
  }
  else if (bar == "single"){
    cout << bar << endl;
    ampch_id[0]  = 18; // digitizer index of reference channel (MCP)
    timech_id[0] = 18; // digitizer index of reference channel (MCP)
    namech[0] = "photek";
    ampmin_cut[0] = 50.;  //  low amp cut in mV (can be loose, dynamic selection on MIP peak below)
    ampmax_cut[0] = 450.; // high amp cut in mV (can be loose, dynamic selection on MIP peak below)
    
    ampch_id[1]  = 21; // digitizer index of 2nd bar, left SiPM
    timech_id[1] = 19;  // digitizer index of 2nd bar, left SiPM
    namech[1] = "FBK left";
    ampmin_cut[1] = 20.;  //  low amp cut in mV (can be loose, dynamic selection on MIP peak below)
    ampmax_cut[1] = 400.; // high amp cut in mV (can be loose, dynamic selection on MIP peak below)
    
    ampch_id[2]  = 22; // digitizer index of 2nd bar, right SiPM 
    timech_id[2] = 20;  // digitizer index of 2nd bar, right SiPM
    namech[2] = "FBK right";
    ampmin_cut[2] = 20.;  //  low amp cut in mV (can be loose, dynamic selection on MIP peak below)
    ampmax_cut[2] = 400.; // high amp cut in mV (can be loose, dynamic selection on MIP peak below)
  }
  
  //------------------
  // define selections
  float rel_amp_cut_low = 0.85; //  low amp cut in fraction of MIP peak
  float rel_amp_cut_hig = 4.;   // high amp cut in fraction of MIP peak

  float lowerTimeCut = 20.; //  low time cut in ns
  float upperTimeCut = 60.; // high time cut in ns
  float nSigmaTimeCut = 2.; // n of sigma on time cut
  
  float minX = -99.;   // range of X in mm
  float maxX = -99.;   // range of X in mm
  float centerX = -99.; // hodoscope X coordinate of crystal center in mm
  float BSX = -99.;     // half-size of beam spot selection around the center in mm
  float minY = -99.;    // range of Y in mm
  float maxY = -99.;    // range of Y in mm
  float centerY = -99.; // hodoscope Y coordinate of crystal center in mm
  float BSY = -99;      // half-size of beam spot selection around the center in mm

  if( bar == "box1"){
    minX = -10.;   // range of X in mm
    maxX = +30.;   // range of X in mm
    centerX = 13.; // hodoscope X coordinate of crystal center in mm
    BSX = 15.;     // half-size of beam spot selection around the center in mm
    minY = 0.;    // range of Y in mm
    maxY = +40.;    // range of Y in mm
    centerY = 28.25; // hodoscope Y coordinate of crystal center in mm
    BSY = 1.25;      // half-size of beam spot selection around the center in mm
  }
  else if( bar == "box2"){
    minX = -10.;   // range of X in mm
    maxX = +30.;   // range of X in mm
    centerX = 13.; // hodoscope X coordinate of crystal center in mm
    BSX = 15.;     // half-size of beam spot selection around the center in mm
    minY = 0.;    // range of Y in mm
    maxY = +40.;    // range of Y in mm
    //centerY = 25.; // hodoscope Y coordinate of crystal center in mm
    centerY = 20.; // hodoscope Y coordinate of crystal center in mm
    BSY = 1.5;      // half-size of beam spot selection around the center in mm
  }
  else if( bar == "box3"){
    minX = -10.;   // range of X in mm
    maxX = +30.;   // range of X in mm
    centerX = 13.; // hodoscope X coordinate of crystal center in mm
    BSX = 15.;     // half-size of beam spot selection around the center in mm
    minY = 0.;    // range of Y in mm
    maxY = +40.;    // range of Y in mm
    centerY = 21.5; // hodoscope Y coordinate of crystal center in mm
    BSY = 1.5;      // half-size of beam spot selection around the center in mm
  }
  else if( bar == "single"){
    minX = -10.;   // range of X in mm
    maxX = +30.;   // range of X in mm
    centerX = 9.5; // hodoscope X coordinate of crystal center in mm
    BSX = 13.5;     // half-size of beam spot selection around the center in mm
    minY = 0.;    // range of Y in mm
    maxY = +40.;    // range of Y in mm
    centerY = 26.; // hodoscope Y coordinate of crystal center in mm
    BSY = 1.5;      // half-size of beam spot selection around the center in mm
  }

  const int NPOSCUTSX = 8; // number of bins along X for binned time resolution
  float lowerPosCutX = centerX-BSX;
  float upperPosCutX = centerX+BSX;  
  const int NPOSCUTSY = 6; // number of bins along Y for binned time resolution
  float lowerPosCutY = centerY-BSY;
  float upperPosCutY = centerY+BSY;
  
  const int NBSCUTS = 6; // number of beam spot bins
  float BScut[NBSCUTS];
  BScut[0] = 10; // in mm around the center
  BScut[1] = 7;
  BScut[2] = 5;
  BScut[3] = 3;
  BScut[4] = 2;
  BScut[5] = 1;
  
  float sigma_ref = 0.015; // MCP time resolution
  
  
  TH1F* hPad;
  TLegend* leg;
  
  int nAmpBins = 250;
  float ampMin = 0.;
  float ampMax = 1000.;

  int nTimeBins = 500;
  float minTime = 0.;
  float maxTime = 200.;
  
  int nDeltatBins = 500;
  float minDeltat = -20.;
  float maxDeltat = +20.;
  
  
  //------------
  // define tree  
  TChain* myTree = new TChain("pulse", "pulse");
  TFile *f0 = new TFile();
  bool trackingIsSynced = false;
  for (int iRun = firstRun; iRun <= lastRun; iRun++)
  {   
  f0 = TFile::Open( Form("%s/RawDataSaver0CMSVMETiming_Run%d_0_Raw.root",dataFolder.c_str(),iRun) );
    if ( f0 == NULL ) {
      std::cout << " !! FILE NOT FOUND " << Form("%s/RawDataSaver0CMSVMETiming_Run%d_0_Raw.root",dataFolder.c_str(),iRun) << std::endl;
      continue;
    }

    trackingIsSynced = checkTrackingSynchronization( Form("%s/RawDataSaver0CMSVMETiming_Run%d_0_Raw.root",dataFolder.c_str(),iRun) );

    if (trackingIsSynced == true) {
      //myTree->Add( Form("%s/DataVMETiming_Run%d.root",dataFolder.c_str(),iRun) );
      myTree->Add( Form("%s/RawDataSaver0CMSVMETiming_Run%d_0_Raw.root",dataFolder.c_str(),iRun) ); // BBT, 4-18-19 
      std::cout << "adding run: " << iRun << " " <<  Form("%s/RawDataSaver0CMSVMETiming_Run%d_0_Raw.root",dataFolder.c_str(),iRun) << std::endl;
    }
    else
      std::cout << "!! TRACKING DE-SYNCED, skiping run: " << iRun << " " <<  Form("%s/RawDataSaver0CMSVMETiming_Run%d_0_Raw.root",dataFolder.c_str(),iRun) << std::endl;
    
  }
  
  int nEntries = myTree->GetEntries();
  std::cout << ">>> Events read: " << nEntries << std::endl;

  TProfile2D* h_box1   = new TProfile2D("h_box1", "h_box1", 100, -10, 40, 80, 0, 40);
  TProfile2D* h_box2   = new TProfile2D("h_box2", "h_box2", 100, -10, 40, 80, 0, 40);  
  TProfile2D* h_box3   = new TProfile2D("h_box3", "h_box3", 100, -10, 40, 80, 0, 40);
  TProfile2D* h_single = new TProfile2D("h_single", "h_single", 100, -10, 40, 80, 0, 40);
  TCanvas* c_box1 = new TCanvas("c_box1", "c_box1", 800, 800);
  TCanvas* c_box2 = new TCanvas("c_box2", "c_box2", 800, 800);
  TCanvas* c_box3 = new TCanvas("c_box3", "c_box3", 800, 800);
  TCanvas* c_single = new TCanvas("c_single", "c_single", 800, 800);



  c_box1->cd();
  myTree->Draw("amp[2] > 400 :  y_dut[0]:x_dut[0]>>+h_box1", "ntracks==1", "profcolz");

  c_box2->cd();
  myTree->Draw("amp[4] > 400 :  y_dut[0]:x_dut[0]>>+h_box2", "ntracks==1", "profcolz");

  c_box3->cd();
  myTree->Draw("amp[6] > 400 :  y_dut[0]:x_dut[0]>>+h_box3", "ntracks==1", "profcolz");

  c_single->cd();
  myTree->Draw("amp[20] > 200 :  y_dut[0]:x_dut[0]>>+h_single", "ntracks==1", "profcolz");

  return;

}
