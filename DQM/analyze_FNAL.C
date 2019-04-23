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

void analyze_FNAL(string bar, const int& firstRun, const int& lastRun, string timeAlgo="LP2_30", string outputDir="./", string isCondor="")
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
    centerY = 25.; // hodoscope Y coordinate of crystal center in mm
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
  
  
  float amp[36];
  float time[36];
  float gaus_mean[36];
  float x_dut[4];
  float y_dut[4];
  
  //myTree->SetBranchStatus("*",0);
  myTree -> SetBranchAddress("amp",       &amp);
  myTree -> SetBranchAddress(timeAlgo.c_str(),     &time);
  myTree -> SetBranchAddress("gaus_mean", &gaus_mean);
  myTree -> SetBranchAddress("x_dut",     x_dut);
  myTree -> SetBranchAddress("y_dut",     y_dut);
  
  std::map<int,TLatex*> latex;
  for(int iCh = 0; iCh < NCH; ++iCh)
  {
    latex[iCh] = new TLatex(0.16,0.96,Form("%s",namech[iCh].c_str()));
    latex[iCh] -> SetNDC();
    latex[iCh] -> SetTextFont(42);
    latex[iCh] -> SetTextSize(0.03);
  }
  
  
  
  
  
  
  //------------------------------------------------------------------------
  //                   (1) first event loop - to calculate mip peak position
  //------------------------------------------------------------------------
  
  // define histograms
  TH2F* h_beamXY = new TH2F("h_beamXY","h_beamXY",100,minX,maxX,100,minY,maxY);
  TH1F* h_beamX  = new TH1F("h_beamX", "h_beamX", 100,minX,maxX);
  TH1F* h_beamY  = new TH1F("h_beamY", "h_beamY", 100,minY,maxY);
  
  TH1F* h_amp[NCH];
  TH1F* h_amp_cut[NCH];
  
  TProfile2D* p2_amp_vs_XY[NCH];
  
  TH1F* h_time[NCH];
  
  for(int iCh = 0; iCh<NCH; ++iCh)
  {
    h_amp[iCh] = new TH1F(Form("h_amp_%s",namech[iCh].c_str()),"",nAmpBins,ampMin,ampMax);
    h_amp_cut[iCh] = new TH1F(Form("h_amp_cut_%s",namech[iCh].c_str()),"",nAmpBins,ampMin,ampMax);    
    
    p2_amp_vs_XY[iCh] = new TProfile2D(Form("p2_amp_vs_XY_%s",namech[iCh].c_str()),"",100,minX,maxX,100,minY,maxY);
    
    h_time[iCh] = new TH1F(Form("h_time_%s",namech[iCh].c_str()),"",nTimeBins,minTime,maxTime);
  }
  
  
  // event loop
  int nSelectedEntries = 0;
  for(int entry = 0; entry < nEntries; ++entry)
  {
    std::cout << ">>> 1st loop: reading entry " << entry << " / " << nEntries << "\r" << std::flush;
    myTree -> GetEntry(entry);
    
    float myX = x_dut[0];
    float myY = y_dut[0];
        
    if( myX == -999 || myY == -999 ) continue;
    
    h_beamX  -> Fill( myX );
    h_beamY  -> Fill( myY );
    h_beamXY -> Fill( myX,myY );

    for(int iCh = 0; iCh < NCH; ++iCh)
    {
      h_amp[iCh] -> Fill( amp[ampch_id[iCh]] );    
      p2_amp_vs_XY[iCh] -> Fill( myX,myY,amp[ampch_id[iCh]] );

      // cut on BS
      if( myX == -999 || myY == -999 ) continue;
      if( fabs(myX-centerX) > BSX || fabs(myY-centerY) > BSY ) continue;    
      
      h_time[iCh] -> Fill( time[timech_id[iCh]] );
      
      if( amp[ampch_id[iCh]] > ampmin_cut[iCh] && amp[ampch_id[iCh]] < ampmax_cut[iCh] )
      {                
        h_amp_cut[iCh] -> Fill( amp[ampch_id[iCh]] );
      }
    }
    
    ++nSelectedEntries;
  }
  std::cout << "\n>>> 1st loop: selected entries " << nSelectedEntries << std::endl;
  
  
  
  // ---------------------------- drawing beam histos ----------------------------
  TCanvas* c_beamXY = new TCanvas("c_beamXY","c_beamXY",500,500);
  c_beamXY->cd();
  h_beamXY->SetStats(0);
  h_beamXY->SetTitle(";X [mm]; Y[mm];entries");
  h_beamXY->Draw("COLZ");
  
  TLine * x_BS_min = new TLine(centerX-BSX, minY, centerX-BSX, maxY);
  TLine * x_BS_max = new TLine(centerX+BSX, minY, centerX+BSX, maxY);
  TLine * y_BS_min = new TLine(minX, centerY-BSY, maxX, centerY-BSY);
  TLine * y_BS_max = new TLine(minX, centerY+BSY, maxX, centerY+BSY);
  
  x_BS_min->SetLineColor(kRed);
  x_BS_min->SetLineWidth(2);
  x_BS_max->SetLineColor(kRed);
  x_BS_max->SetLineWidth(2);
  y_BS_min->SetLineColor(kRed);
  y_BS_min->SetLineWidth(2);
  y_BS_max->SetLineColor(kRed);
  y_BS_max->SetLineWidth(2);

  TCanvas* c_amp_vs_XY = new TCanvas("c_amp_vs_XY","c_amp_vs_XY",1000,500*((NCH-1))/2);
  c_amp_vs_XY -> Divide(2,(NCH-1)/2);
  for(int iCh = 1; iCh < NCH; ++iCh)
  {
    c_amp_vs_XY -> cd(iCh);
    p2_amp_vs_XY[iCh]->Draw("COLZ");
    p2_amp_vs_XY[iCh]->SetStats(0);
    p2_amp_vs_XY[iCh]->SetTitle(";X [mm];Y [mm];amplitude [mV]");
    gPad -> SetLogz();
    
    x_BS_min->Draw("same");
    x_BS_max->Draw("same");
    y_BS_min->Draw("same");
    y_BS_max->Draw("same");

    latex[iCh] -> Draw("same");
  }
  
  // ---------------------------- fitting and drawing mip peak ----------------------------
  float mip_peak[NCH];
  
  TCanvas* c_amp = new TCanvas("c_amp","c_amp",1000,500*(NCH+1)/2);
  c_amp -> Divide(2,(NCH+1)/2);
  TLatex *l_peakAmp = new TLatex();

  for (int iCh = 0; iCh < NCH; ++iCh)
  {
    c_amp -> cd(iCh+1);
    gPad->SetLogy();

    h_amp[iCh] -> SetStats(0);
    h_amp[iCh] -> SetLineColor(kBlack);
    h_amp[iCh] -> SetLineWidth(2);
    h_amp[iCh] -> Draw();
    h_amp[iCh] -> SetTitle(";max. amp [mV];entries");
    h_amp_cut[iCh] -> SetFillColor(kOrange-9);
    h_amp_cut[iCh] -> SetLineColor(kBlack);
    h_amp_cut[iCh] -> SetLineWidth(2);
    h_amp_cut[iCh] -> Draw("same");

    if( iCh > 0 )
    {
      TF1* fitMipPeak = new TF1 ("fitMipPeak","landau",ampmin_cut[iCh],ampmax_cut[iCh]);
      fitMipPeak -> SetParameter(1,h_amp_cut[iCh]->GetBinCenter(h_amp_cut[iCh]->GetMaximum()));
      fitMipPeak->SetNpx(10000);
      fitMipPeak->SetLineColor(kRed);
      fitMipPeak->SetLineWidth(2);
      h_amp_cut[iCh] -> Fit(fitMipPeak,"SQR");
      mip_peak[iCh] = fitMipPeak->GetParameter(1);
      std::cout << "peak[" << iCh << "] = " << mip_peak[iCh] << " mV" << std::endl;
      
      TLine* lowcut = new TLine(std::max(rel_amp_cut_low*mip_peak[iCh],ampmin_cut[iCh]),0.,std::max(rel_amp_cut_low*mip_peak[iCh],ampmin_cut[iCh]),h_amp[iCh]->GetMaximum());
      TLine* higcut = new TLine(std::min(rel_amp_cut_hig*mip_peak[iCh],ampmax_cut[iCh]),0.,std::min(rel_amp_cut_hig*mip_peak[iCh],ampmax_cut[iCh]),h_amp[iCh]->GetMaximum());
      lowcut->Draw("same");
      higcut->Draw("same");
      
      l_peakAmp = new TLatex(0.55, 0.8, Form("Fit Peak: %.2f mV", mip_peak[iCh]));
      l_peakAmp->SetNDC();
      l_peakAmp->SetTextFont(42);
      l_peakAmp->SetTextSize(0.03);
      l_peakAmp->Draw("same");
    }
    
    latex[iCh] -> Draw("same");
  }
  
  // ---------------------------- fitting and drawing time peak ----------------------------
  TF1* fitTimePeak = new TF1("fitTimePeak","gaus",lowerTimeCut,upperTimeCut);
  float time_peak[NCH];
  float time_sigma[NCH];
  
  TCanvas* c_time = new TCanvas("c_time","c_time",1000,500*(NCH+1)/2);
  c_time -> Divide(2,(NCH+1)/2);
  
  for(int iCh = 0; iCh < NCH; ++iCh)
  {
    c_time -> cd(iCh+1);
    gPad -> SetLogy();

    h_time[iCh] -> SetStats(0);
    h_time[iCh] -> SetFillColor(kOrange-9);
    h_time[iCh] -> SetLineColor(kBlack);
    h_time[iCh] -> Draw();
    h_time[iCh] -> SetTitle(";time [ns];entries");
    
    fitTimePeak->SetParameters(1.,20.,5.);
    fitTimePeak->SetNpx(10000);
    fitTimePeak->SetLineColor(kRed);
    fitTimePeak->SetLineWidth(2);
    h_time[iCh] -> Fit(fitTimePeak,"QRS");
    time_peak[iCh] = fitTimePeak->GetParameter(1);
    time_sigma[iCh] = fitTimePeak->GetParameter(2);
    std::cout << "time_peak[" << iCh << "] = " << time_peak[iCh] << " :: sigma_time_peak = " << time_sigma[iCh] << std::endl;            
    
    TLine* lowcut = new TLine(std::max(time_peak[iCh]-time_sigma[iCh]*nSigmaTimeCut,lowerTimeCut),0,std::max(time_peak[iCh]-time_sigma[iCh]*nSigmaTimeCut,lowerTimeCut),h_time[iCh]->GetMaximum());
    TLine* higcut = new TLine(std::min(time_peak[iCh]+time_sigma[iCh]*nSigmaTimeCut,upperTimeCut),0,std::min(time_peak[iCh]+time_sigma[iCh]*nSigmaTimeCut,upperTimeCut),h_time[iCh]->GetMaximum());
    
    lowcut->Draw("same");
    higcut->Draw("same");
    
    latex[iCh] -> Draw("same");
  }
  
  
  //-----------------------------------------------------------------------------
  //                   (2) second loop events -  to calculate amp-walk correction
  //-----------------------------------------------------------------------------
  
  // define histograms
  TH1F* h_deltat[NCH];
  TH2F* h2_deltat_vs_amp[NCH];
  TProfile* p_deltat_vs_amp[NCH];
  
  for(int iCh = 0; iCh<NCH; ++iCh)
  {
    h_deltat[iCh] = new TH1F(Form("h_deltat_%s",namech[iCh].c_str()),"",nDeltatBins,minDeltat,maxDeltat);
    
    h2_deltat_vs_amp[iCh] = new TH2F(Form("h2_deltat_vs_amp_%s",namech[iCh].c_str()),"",nAmpBins,ampMin,ampMax,nDeltatBins,minDeltat,maxDeltat);
    p_deltat_vs_amp[iCh] = new TProfile(Form("p_deltat_vs_amp_%s",namech[iCh].c_str()),"",nAmpBins,ampMin,ampMax);
  }

  
  // event loop
  nSelectedEntries = 0;
  double nCountedEntries = 0;
  for(int entry = 0; entry < nEntries; ++entry)
  {
    std::cout << ">>> 2nd loop: reading entry " << entry << " / " << nEntries << "\r" << std::flush;
    myTree -> GetEntry(entry);
    
    float myX = x_dut[0];
    float myY = y_dut[0];
    
    // cut on BS
    if( myX == -999 || myY == -999 ) continue;
    if( fabs(myX-centerX) > BSX || fabs(myY-centerY) > BSY ) continue;    
    
    
    float time_ref = gaus_mean[timech_id[0]];
    
    //cut on MCP amp
    if( amp[ampch_id[0]] < ampmin_cut[0] ||
        amp[ampch_id[0]] > ampmax_cut[0] )
      continue;
    //cut on MCP time
    if ( time_ref < std::max(time_peak[0]-time_sigma[0]*nSigmaTimeCut,lowerTimeCut) ||
         time_ref > std::min(time_peak[0]+time_sigma[0]*nSigmaTimeCut,upperTimeCut) )
      continue;
    
    for(int iCh = 0; iCh < NCH; ++iCh)
    {      
      if( amp[ampch_id[iCh]] > std::max(mip_peak[iCh]*rel_amp_cut_low,ampmin_cut[iCh]) &&
          amp[ampch_id[iCh]] < std::min(mip_peak[iCh]*rel_amp_cut_hig,ampmax_cut[iCh]) &&
          time[timech_id[iCh]] > std::max(time_peak[iCh]-time_sigma[iCh]*nSigmaTimeCut,lowerTimeCut) &&
          time[timech_id[iCh]] < std::min(time_peak[iCh]+time_sigma[iCh]*nSigmaTimeCut,upperTimeCut) )
      {
        h_deltat[iCh] -> Fill( time[timech_id[iCh]]-time_ref );
        
        h2_deltat_vs_amp[iCh] -> Fill( amp[ampch_id[iCh]],time[timech_id[iCh]]-time_ref );
        p_deltat_vs_amp[iCh]  -> Fill( amp[ampch_id[iCh]],time[timech_id[iCh]]-time_ref );
	++nCountedEntries;
      }
    }
    
    ++nSelectedEntries;
  }
  std::cout << "\n>>> 2nd loop: selected entries " << nSelectedEntries << std::endl;
  std::cout << "\n>>> 2nd loop: counted entries " << nCountedEntries << std::endl;
  
  
  
  // ---------------------------- fitting and drawing time walk correction ----------------------------
  TF1* fitAmpCorr[NCH];

  TCanvas* c_time_vs_amp = new TCanvas("c_time_vs_amp","c_time_vs_amp",1000.,500.*((NCH-1))/2);
  c_time_vs_amp -> Divide(2,(NCH-1)/2);
  
  for(int iCh = 1; iCh < NCH; ++iCh)
  {
    c_time_vs_amp -> cd(iCh);
    
    h2_deltat_vs_amp[iCh]->SetStats(0);
    h2_deltat_vs_amp[iCh]->GetYaxis()->SetRangeUser(h_deltat[iCh]->GetMean()-5.*h_deltat[iCh]->GetRMS(),h_deltat[iCh]->GetMean()+5.*h_deltat[iCh]->GetRMS());
    h2_deltat_vs_amp[iCh]->SetTitle(";#Deltat [ns]; max. amplitude [mV]");
    h2_deltat_vs_amp[iCh]->Draw("COLZ");
    p_deltat_vs_amp[iCh]->SetMarkerStyle(20);
    p_deltat_vs_amp[iCh]->SetMarkerSize(0.7);
    p_deltat_vs_amp[iCh]->SetMarkerColor(kMagenta);
    p_deltat_vs_amp[iCh]->Draw("same");
    
    // fitAmpCorr[iCh] = new TF1(Form("fitAmpCorr_%s", namech[iCh].c_str()),"[0]*log([1]*x)+[2]",0.,1000.);
    // fitAmpCorr[iCh]->SetParameters(-0.3,6e-13,-10.);
    fitAmpCorr[iCh] = new TF1(Form("fitAmpCorr_%s", namech[iCh].c_str()),"pol4",0.,1000.);
    //fitAmpCorr[iCh] = new TF1(Form("fitAmpCorr_%s", namech[iCh].c_str()),"pol4",0.,200.);

    p_deltat_vs_amp[iCh] -> Fit(fitAmpCorr[iCh],"QNRS+");
    fitAmpCorr[iCh] -> SetLineColor(kMagenta);
    fitAmpCorr[iCh] -> Draw("same");
    
    latex[iCh] -> Draw("same");
  }
  
  
  //--------------------------------------------------------------------------
  //                    (3) third loop events --> to apply amp-walk correction
  //--------------------------------------------------------------------------

  // define histograms
  TH1F* h_deltat_avg = new TH1F("h_deltat_avg","",6000, minDeltat, maxDeltat);
  TH1F* h_deltat_avg_ampCorr = new TH1F("h_deltat_avg_ampCorr","",6000, minDeltat, maxDeltat);
  
  TH1F* h_deltat_avg_ampCorr_comb = new TH1F("h_deltat_avg_ampCorr_comb","",6000, minDeltat, maxDeltat);
  
  TH1F* h_deltat_left  = new TH1F("h_deltat_left","",6000, minDeltat, maxDeltat);
  TH1F* h_deltat_right = new TH1F("h_deltat_right","",6000, minDeltat, maxDeltat);
  TH1F* h_deltat_diff  = new TH1F("h_deltat_diff","",6000, minDeltat, maxDeltat);
  
  TH1F* h_deltat_left_ampCorr  = new TH1F("h_deltat_left_ampCorr","",6000, minDeltat, maxDeltat);
  TH1F* h_deltat_right_ampCorr = new TH1F("h_deltat_right_ampCorr","",6000, minDeltat, maxDeltat);
  TH1F* h_deltat_diff_ampCorr  = new TH1F("h_deltat_diff_ampCorr","",6000, minDeltat, maxDeltat);
  
  TProfile* p_left_vs_X  = new TProfile("p_left_vs_X","",400,minX,maxX);
  TProfile* p_right_vs_X = new TProfile("p_right_vs_X","",400,minX,maxX);  
  TProfile* p_avg_vs_X   = new TProfile("p_avg_vs_X","",400,minX,maxX);
  TProfile* p_diff_vs_X  = new TProfile("p_diff_vs_X","",400,minX,maxX);
  
  TProfile* p_left_vs_diff  = new TProfile("p_left_vs_diff","",6000,-10,10);
  TProfile* p_right_vs_diff = new TProfile("p_right_vs_diff","",6000,-10,10);  
  TProfile* p_avg_vs_diff   = new TProfile("p_avg_vs_diff","",6000,-10,10);
  
  TH1F* h_deltat_avg_ampCorr_posCutX[NPOSCUTSX];
  TH1F* h_deltat_left_ampCorr_posCutX[NPOSCUTSX];
  TH1F* h_deltat_right_ampCorr_posCutX[NPOSCUTSX];

  TH1F* h_deltat_avg_ampCorr_posCutY[NPOSCUTSY]; 
  TH1F* h_deltat_left_ampCorr_posCutY[NPOSCUTSY]; 
  TH1F* h_deltat_right_ampCorr_posCutY[NPOSCUTSY];

  TH1F* h_deltat_avg_ampCorr_posCutXY[NPOSCUTSX][NPOSCUTSY];
  
  for(int iPosCut = 0; iPosCut < NPOSCUTSX; ++iPosCut)
  {
    h_deltat_avg_ampCorr_posCutX[iPosCut]   = new TH1F(Form("h_deltat_ampCorr_posCut_%d", iPosCut), "",3000,minDeltat, maxDeltat);
    h_deltat_left_ampCorr_posCutX[iPosCut]  = new TH1F(Form("h_deltat_left_ampCorr_posCut_%d",iPosCut), "",3000,minDeltat, maxDeltat);
    h_deltat_right_ampCorr_posCutX[iPosCut]  = new TH1F(Form("h_deltat_right_ampCorr_posCut_%d",iPosCut), "",3000,minDeltat, maxDeltat);
  }  
  
  for(int iPosCut = 0; iPosCut < NPOSCUTSY; ++iPosCut)
  {
    h_deltat_avg_ampCorr_posCutY[iPosCut]   = new TH1F(Form("h_deltat_ampCorr_posCutY_%d", iPosCut), "",3000,minDeltat, maxDeltat);
    h_deltat_left_ampCorr_posCutY[iPosCut]  = new TH1F(Form("h_deltat_left_ampCorr_posCutY_%d",iPosCut), "",3000,minDeltat, maxDeltat);
    h_deltat_right_ampCorr_posCutY[iPosCut]  = new TH1F(Form("h_deltat_right_ampCorr_posCutY_%d",iPosCut), "",3000,minDeltat, maxDeltat);
  }
  
  for(int iPosCutX = 0; iPosCutX < NPOSCUTSX; ++iPosCutX)
  {
    for(int iPosCutY = 0; iPosCutY < NPOSCUTSY; ++iPosCutY)
    {
      h_deltat_avg_ampCorr_posCutXY[iPosCutX][iPosCutY]  = new TH1F(Form("h_deltat_ampCorr_posCutXY_%d_%d", iPosCutX,iPosCutY), "",3000,minDeltat, maxDeltat);
    }
  }
  
  TH1F* h_deltat_avg_ampCorr_BSCut[NBSCUTS];
  TH1F* h_deltat_left_ampCorr_BSCut[NBSCUTS];
  TH1F* h_deltat_right_ampCorr_BSCut[NBSCUTS];
  for (int iBSCut = 0; iBSCut < NBSCUTS; iBSCut++)
  {
    h_deltat_avg_ampCorr_BSCut[iBSCut]  = new TH1F(Form("h_deltat_avg_ampCorr_BSCut_%d", iBSCut), "",nDeltatBins, minDeltat, maxDeltat);
    h_deltat_left_ampCorr_BSCut[iBSCut]  = new TH1F(Form("h_deltat_left_ampCorr_BSCut_%d", iBSCut), "",nDeltatBins, minDeltat, maxDeltat);
    h_deltat_right_ampCorr_BSCut[iBSCut]  = new TH1F(Form("h_deltat_right_ampCorr_BSCut_%d", iBSCut), "",nDeltatBins, minDeltat, maxDeltat);
  }
  
  
  // event loop
  nSelectedEntries = 0;
  for(int entry = 0; entry < nEntries; ++entry)
  {
    if( entry%100 == 0 ) std::cout << ">>> 3rd loop: reading entry " << entry << " / " << nEntries << "\r" << std::flush;
    myTree -> GetEntry(entry);
    
    float myX = x_dut[0];
    float myY = y_dut[0];
    
    // cut on BS
    if( myX == -999 || myY == -999 ) continue;
    if( fabs(myX-centerX) > BSX || fabs(myY-centerY) > BSY ) continue;    
    
    
    float time_ref = gaus_mean[timech_id[0]];
    
    //cut on MCP amp
    if( amp[ampch_id[0]] < ampmin_cut[0] ||
        amp[ampch_id[0]] > ampmax_cut[0] )
      continue;
    //cut on MCP time
    if ( time_ref < std::max(time_peak[0]-time_sigma[0]*nSigmaTimeCut,lowerTimeCut) ||
         time_ref > std::min(time_peak[0]+time_sigma[0]*nSigmaTimeCut,upperTimeCut) )
      continue;
    
    
    // selected bar
    if( amp[ampch_id[1]] < std::max(mip_peak[1]*rel_amp_cut_low,ampmin_cut[1]) ) continue;
    if( amp[ampch_id[1]] > std::min(mip_peak[1]*rel_amp_cut_hig,ampmax_cut[1]) ) continue;
    if( amp[ampch_id[2]] < std::max(mip_peak[2]*rel_amp_cut_low,ampmin_cut[2]) ) continue;
    if( amp[ampch_id[2]] > std::min(mip_peak[2]*rel_amp_cut_hig,ampmax_cut[2]) ) continue;
    if( time[timech_id[1]] < std::max(time_peak[1]-time_sigma[1]*nSigmaTimeCut,lowerTimeCut) ) continue;
    if( time[timech_id[1]] > std::min(time_peak[1]+time_sigma[1]*nSigmaTimeCut,upperTimeCut) ) continue;
    if( time[timech_id[2]] < std::max(time_peak[2]-time_sigma[2]*nSigmaTimeCut,lowerTimeCut) ) continue;
    if( time[timech_id[2]] > std::min(time_peak[2]+time_sigma[2]*nSigmaTimeCut,upperTimeCut) ) continue;
    
    float amp1 = amp[ampch_id[1]];
    float amp2 = amp[ampch_id[2]];
    float time1 = time[timech_id[1]];
    float time2 = time[timech_id[2]];
    float time1_ampCorr = time1 - fitAmpCorr[1]->Eval(amp1) + fitAmpCorr[1]->Eval(h_amp_cut[1]->GetMean());
    float time2_ampCorr = time2 - fitAmpCorr[2]->Eval(amp2) + fitAmpCorr[2]->Eval(h_amp_cut[2]->GetMean());
    
    float deltat_avg = 0.5*(time1+time2) - time_ref;
    float deltat_avg_ampCorr = 0.5*(time1_ampCorr+time2_ampCorr) - time_ref;
    
    h_deltat_left  -> Fill( time1 - time_ref );
    h_deltat_right -> Fill( time2 - time_ref );
    h_deltat_diff  -> Fill( time2 - time1 );
    h_deltat_avg   -> Fill( deltat_avg );
    
    h_deltat_left_ampCorr  -> Fill( time1_ampCorr - time_ref );
    h_deltat_right_ampCorr -> Fill( time2_ampCorr - time_ref );      
    h_deltat_diff_ampCorr  -> Fill( time2_ampCorr - time1_ampCorr );    
    h_deltat_avg_ampCorr   -> Fill( deltat_avg_ampCorr );

    /*
    // combining with another bar
    if(
      amp[ampch_id[3]] > mip_peak[3]*rel_amp_cut_low &&
      amp[ampch_id[3]] < mip_peak[3]*rel_amp_cut_hig &&
      amp[ampch_id[4]] > mip_peak[4]*rel_amp_cut_low &&
      amp[ampch_id[4]] < mip_peak[4]*rel_amp_cut_hig &&
      time[timech_id[3]] > std::max(time_peak[3]-time_sigma[3]*nSigmaTimeCut,lowerTimeCut) &&
      time[timech_id[3]] < std::min(time_peak[3]+time_sigma[3]*nSigmaTimeCut,upperTimeCut) &&
      time[timech_id[4]] > std::max(time_peak[4]-time_sigma[4]*nSigmaTimeCut,lowerTimeCut) &&
      time[timech_id[4]] < std::min(time_peak[4]+time_sigma[4]*nSigmaTimeCut,upperTimeCut)
      )
    {
      float amp3 = amp[ampch_id[3]];
      float amp4 = amp[ampch_id[4]];
      float time3 = time[timech_id[3]];
      float time4 = time[timech_id[4]];
      float time3_ampCorr = time3 - fitAmpCorr[3]->Eval(amp3) + fitAmpCorr[3]->Eval(h_amp_cut[3]->GetMean());
      float time4_ampCorr = time4 - fitAmpCorr[4]->Eval(amp4) + fitAmpCorr[4]->Eval(h_amp_cut[4]->GetMean());
      
      h_deltat_avg_ampCorr_comb -> Fill( 0.5*( 0.5*(time1_ampCorr+time2_ampCorr) + 0.5*(time3_ampCorr+time4_ampCorr) ) - time_ref );
    }
    */
    
    
    // filling plots vs position
    p_left_vs_X  -> Fill( myX,time1_ampCorr-time_ref );
    p_right_vs_X -> Fill( myX,time2_ampCorr-time_ref );
    p_avg_vs_X   -> Fill( myX,0.5*(time1_ampCorr+time2_ampCorr)-time_ref );
    p_diff_vs_X  -> Fill( myX,time2_ampCorr-time1_ampCorr );
    
    
    // filling plots vd t_diff
    p_left_vs_diff  -> Fill( time2_ampCorr-time1_ampCorr,time1_ampCorr-time_ref);
    p_right_vs_diff -> Fill( time2_ampCorr-time1_ampCorr,time2_ampCorr-time_ref);
    p_avg_vs_diff   -> Fill( time2_ampCorr-time1_ampCorr,0.5*(time1_ampCorr+time2_ampCorr)-time_ref);
    
    
    // X dependency  
    for(int iPosCut = 0; iPosCut < NPOSCUTSX; ++iPosCut)
    {
      float step = (upperPosCutX-lowerPosCutX) / NPOSCUTSX;
      if( myX > lowerPosCutX + iPosCut*step &&
          myX < lowerPosCutX + (iPosCut+1)*step )
      {
        h_deltat_avg_ampCorr_posCutX[iPosCut]  -> Fill( deltat_avg_ampCorr );
        h_deltat_left_ampCorr_posCutX[iPosCut] -> Fill( time1_ampCorr - time_ref );
        h_deltat_right_ampCorr_posCutX[iPosCut] -> Fill( time2_ampCorr - time_ref );
      }
    }
    
    // Y dependency
    for(int iPosCut = 0; iPosCut < NPOSCUTSY; ++iPosCut)
    {
      float step = (upperPosCutY-lowerPosCutY) / NPOSCUTSY;
      if( myY >lowerPosCutY + iPosCut*step &&
          myY < lowerPosCutY+(iPosCut+1)*step )
      {
        h_deltat_avg_ampCorr_posCutY[iPosCut]  -> Fill( deltat_avg_ampCorr );
        h_deltat_left_ampCorr_posCutY[iPosCut] -> Fill( time1_ampCorr - time_ref );
        h_deltat_right_ampCorr_posCutY[iPosCut] -> Fill( time2_ampCorr - time_ref );
      }
    }
    
    for (int iPosCutX = 0; iPosCutX < NPOSCUTSX; ++iPosCutX)
    {
      float stepX = (upperPosCutX-lowerPosCutX) / NPOSCUTSX;
      
      for(int iPosCutY = 0; iPosCutY < NPOSCUTSY; ++iPosCutY)
      {
        float stepY = (upperPosCutY-lowerPosCutY) / NPOSCUTSY;
        
        if( myX > lowerPosCutX + iPosCutX*stepX &&
            myX < lowerPosCutX + (iPosCutX+1)*stepX &&
            myY > lowerPosCutY + iPosCutY*stepY &&
            myY < lowerPosCutY + (iPosCutY+1)*stepY )
        {
          h_deltat_avg_ampCorr_posCutXY[iPosCutX][iPosCutY]  -> Fill( deltat_avg_ampCorr );
        }
      }
    }
    
    
    for(int iBSCut = 0; iBSCut< NBSCUTS; ++iBSCut)
    {
      if ( fabs(myX-centerX) < BScut[iBSCut] )
      {
        h_deltat_avg_ampCorr_BSCut[iBSCut] -> Fill( 0.5*(time1_ampCorr+time2_ampCorr) - time_ref );
        h_deltat_left_ampCorr_BSCut[iBSCut] -> Fill( time1_ampCorr - time_ref );
        h_deltat_right_ampCorr_BSCut[iBSCut] -> Fill( time2_ampCorr - time_ref );
      }
    }
    
    
    ++nSelectedEntries;
  }
  std::cout << "\n>>> 3rd loop: selected entries " << nSelectedEntries << std::endl;
  
  
  
  // ---------------------------- position plots ----------------------------
  TCanvas *c_time_vs_X = new TCanvas("c_time_vs_X","c_time_vs_X",1000,500);
  c_time_vs_X -> Divide(2,1);
  
  c_time_vs_X -> cd(1);
  gPad->SetGridy();
  
  TF1* fitFunc_corrX = new TF1("fitFunc_corrX","pol2",centerX-2.*BSX,centerX+2.*BSX);
  p_avg_vs_X -> Fit(fitFunc_corrX,"QNR");

  p_avg_vs_X->GetXaxis()->SetRangeUser(centerX-2.*BSX,centerX+2.*BSX);
  p_avg_vs_X->GetYaxis()->SetRangeUser(h_deltat_avg->GetMean()-15.*h_deltat_avg->GetRMS(),
                                       h_deltat_avg->GetMean()+15.*h_deltat_avg->GetRMS());
  p_avg_vs_X->Draw();
  p_avg_vs_X->SetStats(0);
  p_avg_vs_X ->SetTitle(";X [mm];#Deltat [ns]");
  fitFunc_corrX -> Draw("same");
  p_avg_vs_X-> SetMarkerStyle(21);
  p_left_vs_X-> SetLineColor(kRed+1);
  p_left_vs_X-> SetMarkerColor(kRed+1);
  p_left_vs_X-> SetMarkerStyle(20);
  p_left_vs_X->Draw("same");
  p_right_vs_X-> SetLineColor(kBlue+1);
  p_right_vs_X-> SetMarkerColor(kBlue+1);
  p_right_vs_X-> SetMarkerStyle(20);
  p_right_vs_X->Draw("same");
  p_diff_vs_X-> SetLineColor(kYellow+2);
  p_diff_vs_X-> SetMarkerColor(kYellow+2);
  p_diff_vs_X-> SetMarkerStyle(22);
  p_diff_vs_X-> SetLineStyle(7);
  p_diff_vs_X->Draw("same");
  
  leg = new TLegend(0.71,0.73,0.86,0.93,NULL,"brNDC");
  leg->SetBorderSize(0);
  leg->SetTextFont(42);
  leg->SetTextSize(0.03);
  leg->SetLineColor(1);
  leg->SetLineStyle(1);
  leg->SetLineWidth(1);
  leg->SetFillColor(0);  
  leg->AddEntry(p_left_vs_X,  "t_{left} - t_{MCP}", "lpe");     
  leg->AddEntry(p_right_vs_X, "t_{right} - t_{MCP}", "lpe");     
  leg->AddEntry(p_avg_vs_X,   "t_{avg} - t_{MCP}", "lpe");     
  leg->AddEntry(p_diff_vs_X,  "t_{left} - t_{right}", "lpe");     
  leg->Draw("same");
  
  c_time_vs_X->cd(2);
  gPad->SetGridy();
  
  TF1* fitFunc_corrDiff = new TF1("fitFunc_corrDiff","pol2",h_deltat_diff->GetMean()-5.*h_deltat_diff->GetRMS(),h_deltat_diff->GetMean()+5.*h_deltat_diff->GetRMS());
  p_avg_vs_diff -> Fit(fitFunc_corrDiff,"QNR");
  
  p_avg_vs_diff->GetXaxis()->SetRangeUser(h_deltat_diff->GetMean()-5.*h_deltat_diff->GetRMS(),
                                          h_deltat_diff->GetMean()+5.*h_deltat_diff->GetRMS());
  p_avg_vs_diff->GetYaxis()->SetRangeUser(h_deltat_avg->GetMean()-15.*h_deltat_avg->GetRMS(),
                                          h_deltat_avg->GetMean()+15.*h_deltat_avg->GetRMS());
  p_avg_vs_diff->Draw();
  p_avg_vs_diff->SetStats(0);
  p_avg_vs_diff -> SetTitle(";t_{left} - t_{right} [ns];#Deltat [ns]");
  fitFunc_corrDiff -> Draw("same");
  p_avg_vs_diff-> SetMarkerStyle(20);
  p_left_vs_diff-> SetLineColor(kRed+1);
  p_left_vs_diff-> SetMarkerColor(kRed+1);
  p_left_vs_diff-> SetMarkerStyle(20);
  p_left_vs_diff->Draw("same");
  p_right_vs_diff-> SetLineColor(kBlue+1);
  p_right_vs_diff-> SetMarkerColor(kBlue+1);
  p_right_vs_diff-> SetMarkerStyle(20);
  p_right_vs_diff->Draw("same");
  
  leg = new TLegend(0.71,0.78,0.86,0.93,NULL,"brNDC");
  leg->SetBorderSize(0);
  leg->SetTextFont(42);
  leg->SetTextSize(0.03);
  leg->SetLineColor(1);
  leg->SetLineStyle(1);
  leg->SetLineWidth(1);
  leg->SetFillColor(0);
  leg->AddEntry(p_left_vs_diff,  "t_{left} - t_{MCP}", "lpe");     
  leg->AddEntry(p_right_vs_diff, "t_{right} - t_{MCP}", "lpe");     
  leg->AddEntry(p_avg_vs_diff,   "t_{avg} - t_{MCP}", "lpe");     
  leg->Draw("same");
  
  // ---------------------------- compare left, right, sum time resolution ----------------------------
  TCanvas* c_timeRes_comp = new TCanvas("c_timeRes_comp","c_timeRes_comp",1000,500);
  c_timeRes_comp->Divide(2,1);
  
  c_timeRes_comp->cd(1);
  h_deltat_avg -> SetStats(0);
  h_deltat_avg -> SetTitle(";#Deltat (no amp-walk corr.) [ns];entries");
  h_deltat_avg -> SetLineColor(kBlack);
  h_deltat_avg -> SetLineWidth(2);
  h_deltat_avg -> GetXaxis() -> SetRangeUser(h_deltat_avg->GetMean()-15.*h_deltat_avg->GetRMS(),
                                             h_deltat_avg->GetMean()+15.*h_deltat_avg->GetRMS());
  h_deltat_avg -> Draw();
  h_deltat_left -> Draw("same");
  h_deltat_left -> SetLineColor(kRed+1);
  h_deltat_left -> SetLineWidth(2);
  h_deltat_right -> Draw("same");
  h_deltat_right -> SetLineColor(kBlue+1);
  h_deltat_right -> SetLineWidth(2);
  
  TF1* fitdeltat_left = new TF1("fitdeltat_left", "gaus", h_deltat_left->GetMean()-h_deltat_left->GetRMS()*2, h_deltat_left->GetMean()+h_deltat_left->GetRMS()*2);
  fitdeltat_left->SetLineColor(kRed+1);
  h_deltat_left->Fit(fitdeltat_left, "QR");
  TF1* fitdeltat_right = new TF1("fitdeltat_right", "gaus", h_deltat_right->GetMean()-h_deltat_right->GetRMS()*2, h_deltat_right->GetMean()+h_deltat_right->GetRMS()*2);
  fitdeltat_right->SetLineColor(kBlue+1);
  h_deltat_right->Fit(fitdeltat_right, "QR");
  TF1* fitdeltat_avg = new TF1("fitdeltat_avg", "gaus", h_deltat_avg->GetMean()-h_deltat_avg->GetRMS()*2, h_deltat_avg->GetMean()+h_deltat_avg->GetRMS()*2);
  fitdeltat_avg->SetLineColor(kBlack);
  h_deltat_avg->Fit(fitdeltat_avg, "QR");

  float sigmaLeft  = sqrt( pow(fitdeltat_left->GetParameter(2),2)  - pow(sigma_ref,2) );    
  float sigmaRight = sqrt( pow(fitdeltat_right->GetParameter(2),2) - pow(sigma_ref,2) );    
  float sigmaAvg   = sqrt( pow(fitdeltat_avg->GetParameter(2),2)   - pow(sigma_ref,2) );    

  leg = new TLegend(0.65,0.78,0.80,0.93,NULL,"brNDC");
  leg->SetBorderSize(0);
  leg->SetTextFont(42);
  leg->SetTextSize(0.03);
  leg->SetLineColor(1);
  leg->SetLineStyle(1);
  leg->SetLineWidth(1);
  leg->SetFillColor(0);
  leg->SetFillStyle(1000);
  leg->AddEntry(h_deltat_left,  Form("#sigma^{left}_{t} = %.1f ps", sigmaLeft*1000), "l");
  leg->AddEntry(h_deltat_right, Form("#sigma^{right}_{t} = %.1f ps", sigmaRight*1000), "l");
  leg->AddEntry(h_deltat_avg,   Form("#sigma^{avg}_{t} = %.1f ps", sigmaAvg*1000), "l");
  leg->Draw("same");
  
  c_timeRes_comp->cd(2);
  h_deltat_avg_ampCorr -> SetStats(0);
  h_deltat_avg_ampCorr -> SetTitle(";#Deltat (amp-walk corr.) [ns];entries");
  h_deltat_avg_ampCorr -> SetLineColor(kBlack);
  h_deltat_avg_ampCorr -> SetLineWidth(2);
  h_deltat_avg_ampCorr -> GetXaxis() -> SetRangeUser(h_deltat_avg->GetMean()-15.*h_deltat_avg->GetRMS(),
                                                     h_deltat_avg->GetMean()+15.*h_deltat_avg->GetRMS());
  h_deltat_avg_ampCorr -> Draw();
  h_deltat_left_ampCorr -> SetLineColor(kRed+1);
  h_deltat_left_ampCorr -> SetLineWidth(2);
  h_deltat_left_ampCorr -> Draw("same");
  h_deltat_right_ampCorr -> SetLineColor(kBlue+1);
  h_deltat_right_ampCorr -> SetLineWidth(2);
  h_deltat_right_ampCorr -> Draw("same");
  
  TF1* fitdeltat_left_ampCorr = new TF1("fitdeltat_left_ampCorr", "gaus", h_deltat_left_ampCorr->GetMean()-h_deltat_left_ampCorr->GetRMS()*2, h_deltat_left_ampCorr->GetMean()+h_deltat_left_ampCorr->GetRMS()*2);
  fitdeltat_left_ampCorr->SetLineColor(kRed+1);
  h_deltat_left_ampCorr->Fit(fitdeltat_left_ampCorr, "QR");
  TF1* fitdeltat_right_ampCorr = new TF1("fitdeltat_right_ampCorr", "gaus", h_deltat_right_ampCorr->GetMean()-h_deltat_right_ampCorr->GetRMS()*2, h_deltat_right_ampCorr->GetMean()+h_deltat_right_ampCorr->GetRMS()*2);
  fitdeltat_right_ampCorr->SetLineColor(kBlue+1);
  h_deltat_right_ampCorr->Fit(fitdeltat_right_ampCorr, "QR");
  TF1* fitdeltat_avg_ampCorr = new TF1("fitdeltat_avg_ampCorr", "gaus", h_deltat_avg_ampCorr->GetMean()-h_deltat_avg_ampCorr->GetRMS()*2, h_deltat_avg_ampCorr->GetMean()+h_deltat_avg_ampCorr->GetRMS()*2);
  fitdeltat_avg_ampCorr->SetLineColor(kBlack);
  h_deltat_avg_ampCorr->Fit(fitdeltat_avg_ampCorr, "QR");
  
  float sigmaLeftCorr  = sqrt(pow(fitdeltat_left_ampCorr->GetParameter(2),2)  - pow(sigma_ref,2) );    
  float sigmaRightCorr = sqrt(pow(fitdeltat_right_ampCorr->GetParameter(2),2) - pow(sigma_ref,2) );    
  float sigmaAvgCorr   = sqrt(pow(fitdeltat_avg_ampCorr->GetParameter(2),2)   - pow(sigma_ref,2) );    
  
  // ---------------------------- BS cut plots ----------------------------
  TF1* fitdeltat_ampCorr_BSCut_L = new TF1("fitdeltat_ampCorr_BSCut_L", "gaus", h_deltat_left_ampCorr->GetMean() -h_deltat_left_ampCorr->GetRMS()*2,  h_deltat_left_ampCorr->GetMean() +h_deltat_left_ampCorr->GetRMS()*2);
  TF1* fitdeltat_ampCorr_BSCut_R = new TF1("fitdeltat_ampCorr_BSCut_R", "gaus", h_deltat_right_ampCorr->GetMean()-h_deltat_right_ampCorr->GetRMS()*2, h_deltat_right_ampCorr->GetMean()+h_deltat_right_ampCorr->GetRMS()*2);
  TF1* fitdeltat_ampCorr_BSCut   = new TF1("fitdeltat_ampCorr_BSCut",   "gaus", h_deltat_avg_ampCorr->GetMean()  -h_deltat_avg_ampCorr->GetRMS()*2,   h_deltat_avg_ampCorr->GetMean()  +h_deltat_avg_ampCorr->GetRMS()*2);
  
  TGraphErrors * gdeltat_vs_BS_L = new TGraphErrors ();
  TGraphErrors * gdeltat_vs_BS_R = new TGraphErrors ();
  TGraphErrors * gdeltat_vs_BS   = new TGraphErrors ();
  
  int myPoint = 0;
  for (int iBSCut = 0; iBSCut< NBSCUTS; iBSCut++)
  {
    //left
    h_deltat_left_ampCorr_BSCut[iBSCut]->Fit(fitdeltat_ampCorr_BSCut_L, "QNR");
    float tempSigma_L =  sqrt(pow(fitdeltat_ampCorr_BSCut_L->GetParameter(2),2) - pow(sigma_ref, 2));  
    float sigmaErr_L = fitdeltat_ampCorr_BSCut_L->GetParError(2);
    
    //right
    h_deltat_right_ampCorr_BSCut[iBSCut]->Fit(fitdeltat_ampCorr_BSCut_R, "QNR");      
    float tempSigma_R =  sqrt(pow(fitdeltat_ampCorr_BSCut_R->GetParameter(2),2) - pow(sigma_ref, 2));  
    float sigmaErr_R = fitdeltat_ampCorr_BSCut_R->GetParError(2);
    
    //avg
    h_deltat_avg_ampCorr_BSCut[iBSCut]->Fit(fitdeltat_ampCorr_BSCut, "QNR");
    float tempSigma =  sqrt(pow(fitdeltat_ampCorr_BSCut->GetParameter(2),2) - pow(sigma_ref, 2));  
    float sigmaErr = fitdeltat_ampCorr_BSCut->GetParError(2);
    
    if (tempSigma>0 && tempSigma<0.5 &&  h_deltat_avg_ampCorr_BSCut[iBSCut]->GetEntries()>30) 
    {
      gdeltat_vs_BS_L->SetPoint(myPoint, BScut[iBSCut]*2, tempSigma_L);            
      gdeltat_vs_BS_L->SetPointError(myPoint,0, sigmaErr_L);    
      
      gdeltat_vs_BS_R->SetPoint(myPoint, BScut[iBSCut]*2, tempSigma_R);            
      gdeltat_vs_BS_R->SetPointError(myPoint,0, sigmaErr_R);    
      
      gdeltat_vs_BS->SetPoint(myPoint, BScut[iBSCut]*2, tempSigma);            
      gdeltat_vs_BS->SetPointError(myPoint,0, sigmaErr);    
      
      ++myPoint;
    }
  }
  

  TCanvas* c_timeRes_vs_BS = new TCanvas("c_timeRes_vs_BS","c_timeRes_vs_BS",500,500);
  c_timeRes_vs_BS->cd();
  gPad->SetGridy();
  gPad->SetLogx();
  hPad = (TH1F*)( gPad->DrawFrame(BScut[NBSCUTS-1],0.02,3.*BScut[0],0.1) );
  hPad -> SetTitle(";beam spot width [mm];#sigma_{t} [ns]");
  hPad -> Draw();
  gdeltat_vs_BS->Draw("PLE,same");
  gdeltat_vs_BS->SetMarkerStyle(20);
  gdeltat_vs_BS_L->SetLineColor(kRed+1);
  gdeltat_vs_BS_L->SetMarkerColor(kRed+1);
  gdeltat_vs_BS_L->SetMarkerStyle(21);
  gdeltat_vs_BS_L->Draw("same LPE");
  gdeltat_vs_BS_R->SetLineColor(kBlue+1);
  gdeltat_vs_BS_R->SetMarkerColor(kBlue+1);
  gdeltat_vs_BS_R->SetMarkerStyle(21);
  gdeltat_vs_BS_R->Draw("same LPE");
  
  leg = new TLegend(0.71,0.78,0.86,0.93,NULL,"brNDC");
  leg->SetBorderSize(0);
  leg->SetTextFont(42);
  leg->SetTextSize(0.03);
  leg->SetLineColor(1);
  leg->SetLineStyle(1);
  leg->SetLineWidth(1);
  leg->SetFillColor(0);  
  leg->AddEntry(gdeltat_vs_BS_L, Form("left only"), "lpe");     
  leg->AddEntry(gdeltat_vs_BS_R, Form("right only"), "lpe");     
  leg->AddEntry(gdeltat_vs_BS,   Form("avgrage"), "lpe");     
  leg->Draw("same");
  
  // ---------------------------- plots in position bins ----------------------------
  TGraphErrors* g_timeRes_left_vs_X = new TGraphErrors ();
  TGraphErrors* g_timeRes_right_vs_X = new TGraphErrors ();
  TGraphErrors* g_timeRes_avg_vs_X = new TGraphErrors ();
  
  TGraphErrors* g_timeRes_left_vs_Y = new TGraphErrors ();
  TGraphErrors* g_timeRes_right_vs_Y = new TGraphErrors ();
  TGraphErrors* g_timeRes_avg_vs_Y   = new TGraphErrors ();
  
  TH2F* h2_timeRes_avg_vs_XY = new TH2F("h2_timeRes_avg_vs_XY","",NPOSCUTSX,lowerPosCutX,upperPosCutX,NPOSCUTSY,lowerPosCutY,upperPosCutY);
  
  // X position
  // avgrage
  myPoint = 0;
  for(int iPosCut = 0; iPosCut < NPOSCUTSX; ++iPosCut)
  {
    float step = ( upperPosCutX - lowerPosCutX ) / NPOSCUTSX;

    TF1* fitdeltat_ampCorr_posCut = new TF1("fitdeltat_avg_ampCorr_posCut","gaus",
                                            h_deltat_avg_ampCorr_posCutX[iPosCut]->GetMean()-h_deltat_avg_ampCorr_posCutX[iPosCut]->GetRMS()*2.,
                                            h_deltat_avg_ampCorr_posCutX[iPosCut]->GetMean()+h_deltat_avg_ampCorr_posCutX[iPosCut]->GetRMS()*2.);
    h_deltat_avg_ampCorr_posCutX[iPosCut]->Fit(fitdeltat_ampCorr_posCut, "QNR");
    float selPos = lowerPosCutX+(step*iPosCut);
    float tempSigma =  sqrt( pow(fitdeltat_ampCorr_posCut->GetParameter(2),2) - pow(sigma_ref,2) );  
    float sigmaErr = fitdeltat_ampCorr_posCut->GetParError(2);      
    if( tempSigma > 0. && tempSigma < 0.5 && h_deltat_avg_ampCorr_posCutX[iPosCut]->GetEntries() > 20 ) 
    {
      g_timeRes_avg_vs_X->SetPoint(myPoint,selPos,tempSigma);            
      g_timeRes_avg_vs_X->SetPointError(myPoint,step/2/sqrt(12),sigmaErr);    
      ++myPoint;
    }

    delete fitdeltat_ampCorr_posCut;
  }

  // left only
  myPoint = 0;
  for(int iPosCut = 0; iPosCut < NPOSCUTSX; ++iPosCut)
    {
      float step = ( upperPosCutX - lowerPosCutX ) / NPOSCUTSX;

      TF1* fitdeltat_ampCorr_posCut = new TF1("fitdeltat_left_ampCorr_posCut","gaus",
                                              h_deltat_left_ampCorr->GetMean()-h_deltat_left_ampCorr->GetRMS()*2.,
                                              h_deltat_left_ampCorr->GetMean()+h_deltat_left_ampCorr->GetRMS()*2.);
      h_deltat_left_ampCorr_posCutX[iPosCut]->Fit(fitdeltat_ampCorr_posCut, "QNR");
      float selPos = lowerPosCutX+(step*iPosCut);
      float tempSigma =  sqrt(pow(fitdeltat_ampCorr_posCut->GetParameter(2),2) - pow(sigma_ref, 2));
      float sigmaErr = fitdeltat_ampCorr_posCut->GetParError(2);
      if( tempSigma > 0. && tempSigma < 0.5 && h_deltat_left_ampCorr_posCutX[iPosCut]->GetEntries() > 20 )
      {
        g_timeRes_left_vs_X->SetPoint(myPoint, selPos, tempSigma);
        g_timeRes_left_vs_X->SetPointError(myPoint,step/2, sigmaErr);
        ++myPoint;
      }
      delete fitdeltat_ampCorr_posCut;
    }

  // right only
  myPoint = 0;
  for(int iPosCut = 0; iPosCut < NPOSCUTSX; ++iPosCut)
  {
    float step = ( upperPosCutX - lowerPosCutX ) / NPOSCUTSX;

    TF1* fitdeltat_ampCorr_posCut = new TF1("fitdeltat_right_ampCorr_posCut","gaus",
                                            h_deltat_right_ampCorr->GetMean()-h_deltat_right_ampCorr->GetRMS()*2.,
                                            h_deltat_right_ampCorr->GetMean()+h_deltat_right_ampCorr->GetRMS()*2.);
    h_deltat_right_ampCorr_posCutX[iPosCut]->Fit(fitdeltat_ampCorr_posCut, "QNR");
    float selPos = lowerPosCutX+(step*iPosCut);
    float tempSigma =  sqrt(pow(fitdeltat_ampCorr_posCut->GetParameter(2),2) - pow(sigma_ref, 2));
    float sigmaErr = fitdeltat_ampCorr_posCut->GetParError(2);
    if (tempSigma > 0. && tempSigma < 0.5 &&  h_deltat_right_ampCorr_posCutX[iPosCut]->GetEntries() > 20 )
    {
      g_timeRes_right_vs_X->SetPoint(myPoint,selPos,tempSigma);
      g_timeRes_right_vs_X->SetPointError(myPoint,step/2,sigmaErr);
      ++myPoint;
    }
    
    delete fitdeltat_ampCorr_posCut;
  }


  TCanvas* c_timeRes_vs_X_Y = new TCanvas("c_timeRes_vs_X_Y","c_timeRes_vs_X_Y",1000,500);
  c_timeRes_vs_X_Y -> Divide(2,1);
  c_timeRes_vs_X_Y->cd(1);
  gPad->SetGridy();
  g_timeRes_avg_vs_X->GetYaxis()->SetRangeUser(0, 0.2);
  g_timeRes_avg_vs_X->SetTitle(";X [mm];#sigma_{t} [ns]");
  g_timeRes_avg_vs_X->SetMarkerStyle(20);
  g_timeRes_avg_vs_X->Draw("ALPE");
  g_timeRes_left_vs_X->SetLineColor(kRed+1);
  g_timeRes_left_vs_X->SetMarkerColor(kRed+1);
  g_timeRes_right_vs_X->SetLineColor(kBlue+1);
  g_timeRes_right_vs_X->SetMarkerColor(kBlue+1);
  g_timeRes_left_vs_X->Draw("same LPE");
  g_timeRes_right_vs_X->Draw("same LPE");
  
  leg = new TLegend(0.70,0.78,0.85,0.93,NULL,"brNDC");
  leg->SetBorderSize(0);
  leg->SetTextFont(42);
  leg->SetTextSize(0.03);
  leg->SetLineColor(1);
  leg->SetLineStyle(1);
  leg->SetLineWidth(1);
  leg->SetFillColor(0);
  leg->SetFillStyle(1000);
  leg->AddEntry(g_timeRes_left_vs_X,  Form("#sigma^{left}_{t}"), "el");
  leg->AddEntry(g_timeRes_right_vs_X, Form("#sigma^{right}_{t}"),"el");
  leg->AddEntry(g_timeRes_avg_vs_X,   Form("#sigma^{avg}_{t}"),  "pl");
  leg->Draw("same");
  
  // Y position
  // average
  myPoint = 0;
  for(int iPosCut = 0; iPosCut < NPOSCUTSY; ++iPosCut)
  {
    float step = ( upperPosCutY - lowerPosCutY ) / NPOSCUTSY;

    TF1* fitdeltat_ampCorr_posCut = new TF1("fitdeltat_avg_ampCorr_posCut","gaus",
                                            h_deltat_avg_ampCorr_posCutY[iPosCut]->GetMean()-h_deltat_avg_ampCorr_posCutY[iPosCut]->GetRMS()*2.,
                                            h_deltat_avg_ampCorr_posCutY[iPosCut]->GetMean()+h_deltat_avg_ampCorr_posCutY[iPosCut]->GetRMS()*2.);
    h_deltat_avg_ampCorr_posCutY[iPosCut]->Fit(fitdeltat_ampCorr_posCut, "QNR");
    float selPos = lowerPosCutY+(step*iPosCut);
    float tempSigma =  sqrt( pow(fitdeltat_ampCorr_posCut->GetParameter(2),2) - pow(sigma_ref,2) );  
    float sigmaErr = fitdeltat_ampCorr_posCut->GetParError(2);      
    if( tempSigma > 0. && tempSigma < 0.5 && h_deltat_avg_ampCorr_posCutY[iPosCut]->GetEntries() > 20 ) 
    {
      g_timeRes_avg_vs_Y->SetPoint(myPoint,selPos,tempSigma);            
      g_timeRes_avg_vs_Y->SetPointError(myPoint,step/2/sqrt(12),sigmaErr);    
      ++myPoint;
    }

    delete fitdeltat_ampCorr_posCut;
  }

  // left only
  myPoint = 0;
  for(int iPosCut = 0; iPosCut < NPOSCUTSY; ++iPosCut)
    {
      float step = ( upperPosCutY - lowerPosCutY ) / NPOSCUTSY;

      TF1* fitdeltat_ampCorr_posCut = new TF1("fitdeltat_left_ampCorr_posCut","gaus",
                                              h_deltat_left_ampCorr->GetMean()-h_deltat_left_ampCorr->GetRMS()*2.,
                                              h_deltat_left_ampCorr->GetMean()+h_deltat_left_ampCorr->GetRMS()*2.);
      h_deltat_left_ampCorr_posCutY[iPosCut]->Fit(fitdeltat_ampCorr_posCut, "QNR");
      float selPos = lowerPosCutY+(step*iPosCut);
      float tempSigma =  sqrt(pow(fitdeltat_ampCorr_posCut->GetParameter(2),2) - pow(sigma_ref, 2));
      float sigmaErr = fitdeltat_ampCorr_posCut->GetParError(2);
      if( tempSigma > 0. && tempSigma < 0.5 && h_deltat_left_ampCorr_posCutY[iPosCut]->GetEntries() > 20 )
      {
        g_timeRes_left_vs_Y->SetPoint(myPoint, selPos, tempSigma);
        g_timeRes_left_vs_Y->SetPointError(myPoint,step/2, sigmaErr);
        ++myPoint;
      }
      delete fitdeltat_ampCorr_posCut;
    }

  // right only
  myPoint = 0;
  for(int iPosCut = 0; iPosCut < NPOSCUTSY; ++iPosCut)
  {
    float step = ( upperPosCutY - lowerPosCutY ) / NPOSCUTSY;

    TF1* fitdeltat_ampCorr_posCut = new TF1("fitdeltat_right_ampCorr_posCut","gaus",
                                            h_deltat_right_ampCorr->GetMean()-h_deltat_right_ampCorr->GetRMS()*2.,
                                            h_deltat_right_ampCorr->GetMean()+h_deltat_right_ampCorr->GetRMS()*2.);
    h_deltat_right_ampCorr_posCutY[iPosCut]->Fit(fitdeltat_ampCorr_posCut, "QNR");
    float selPos = lowerPosCutY+(step*iPosCut);
    float tempSigma =  sqrt(pow(fitdeltat_ampCorr_posCut->GetParameter(2),2) - pow(sigma_ref, 2));
    float sigmaErr = fitdeltat_ampCorr_posCut->GetParError(2);
    if (tempSigma > 0. && tempSigma < 0.5 &&  h_deltat_right_ampCorr_posCutY[iPosCut]->GetEntries() > 20 )
    {
      g_timeRes_right_vs_Y->SetPoint(myPoint,selPos,tempSigma);
      g_timeRes_right_vs_Y->SetPointError(myPoint,step/2,sigmaErr);
      ++myPoint;
    }
    
    delete fitdeltat_ampCorr_posCut;
  }
  
  c_timeRes_vs_X_Y->cd(2);
  gPad->SetGridy();
  g_timeRes_avg_vs_Y->GetYaxis()->SetRangeUser(0, 0.2);
  g_timeRes_avg_vs_Y->SetTitle(";Y [mm];#sigma_{t} [ns]");
  g_timeRes_avg_vs_Y->SetMarkerStyle(20);
  g_timeRes_avg_vs_Y->Draw("ALPE");
  g_timeRes_left_vs_Y->SetLineColor(kRed+1);
  g_timeRes_left_vs_Y->SetMarkerColor(kRed+1);
  g_timeRes_right_vs_Y->SetLineColor(kBlue+1);
  g_timeRes_right_vs_Y->SetMarkerColor(kBlue+1);
  g_timeRes_left_vs_Y->Draw("same LPE");
  g_timeRes_right_vs_Y->Draw("same LPE");
  
  leg = new TLegend(0.70,0.78,0.85,0.93,NULL,"brNDC");
  leg->SetBorderSize(0);
  leg->SetTextFont(42);
  leg->SetTextSize(0.03);
  leg->SetLineColor(1);
  leg->SetLineStyle(1);
  leg->SetLineWidth(1);
  leg->SetFillColor(0);
  leg->SetFillStyle(1000);
  leg->AddEntry(g_timeRes_left_vs_Y,  Form("#sigma^{left}_{t}"), "el");
  leg->AddEntry(g_timeRes_right_vs_Y, Form("#sigma^{right}_{t}"),"el");
  leg->AddEntry(g_timeRes_avg_vs_Y,   Form("#sigma^{avg}_{t}"),  "pl");
  leg->Draw("same");
  
  
  // XY position
  //right only
  for(int iPosCutX = 0; iPosCutX < NPOSCUTSX; ++iPosCutX)
  {
    float stepX = (upperPosCutX - lowerPosCutX) / NPOSCUTSX;
    
    for(int iPosCutY = 0; iPosCutY < NPOSCUTSY; ++iPosCutY)
    {
      float stepY = (upperPosCutY - lowerPosCutY) / NPOSCUTSY;
      
      if( h_deltat_avg_ampCorr_posCutXY[iPosCutX][iPosCutY]->GetEntries() < 20 ) continue;

      TF1* fitdeltat_ampCorr_posCut = new TF1("fitdeltat_right_ampCorr_posCut","gaus",
                                              h_deltat_avg_ampCorr_posCutXY[iPosCutX][iPosCutY]->GetMean()-h_deltat_avg_ampCorr_posCutXY[iPosCutX][iPosCutY]->GetRMS()*2.,
                                              h_deltat_avg_ampCorr_posCutXY[iPosCutX][iPosCutY]->GetMean()+h_deltat_avg_ampCorr_posCutXY[iPosCutX][iPosCutY]->GetRMS()*2.);
      h_deltat_avg_ampCorr_posCutXY[iPosCutX][iPosCutY]->Fit("fitdeltat_right_ampCorr_posCut","QNR");
      float selPosX = lowerPosCutX+(stepX*iPosCutX);
      float selPosY = lowerPosCutY+(stepY*iPosCutY);
      float tempSigma = sqrt( pow(fitdeltat_ampCorr_posCut->GetParameter(2),2) - pow(sigma_ref,2) );
      float sigmaErr = fitdeltat_ampCorr_posCut->GetParError(2);
      
      if (tempSigma > 0. && tempSigma < 0.5 && h_deltat_avg_ampCorr_posCutXY[iPosCutX][iPosCutY]->GetEntries() > 20 )
      {
        h2_timeRes_avg_vs_XY -> Fill(selPosX,selPosY,tempSigma);
      }

      delete fitdeltat_ampCorr_posCut;
    }
  }


  TCanvas* c_timeRes_vs_XY = new TCanvas ("c_timeRes_vs_XY","c_timeRes_vs_XY",500,500);
  gStyle -> SetPaintTextFormat(".3f");
  h2_timeRes_avg_vs_XY->SetStats(0);
  h2_timeRes_avg_vs_XY->Draw("COLZ,text");
  h2_timeRes_avg_vs_XY->GetZaxis()->SetRangeUser(0, 0.08);
  h2_timeRes_avg_vs_XY->SetTitle(";x [mm];y [mm];#sigma_{t} [ns]");
  
    
  
  //----------------------------------------------------------------------
  //                    (4) fourth loop events --> to apply pos correction
  //----------------------------------------------------------------------

  // define histograms
  TH1F* h_deltat_wei_ampCorr = new TH1F("h_deltat_wei_ampCorr","",6000, minDeltat, maxDeltat);

  TH1F* h_deltat_avg_ampCorr_diffCorr = new TH1F("h_deltat_avg_ampCorr_diffCorr","",6000, minDeltat, maxDeltat);
  TH1F* h_deltat_avg_ampCorr_posCorr = new TH1F("h_deltat_avg_ampCorr_posCorr","",6000, minDeltat, maxDeltat);

  // event loop
  nSelectedEntries = 0;
  for(int entry = 0; entry < nEntries; ++entry)
  {
    if( entry%100 == 0 ) std::cout << ">>> 4th loop: reading entry " << entry << " / " << nEntries << "\r" << std::flush;
    myTree -> GetEntry(entry);
    
    float myX = x_dut[0];
    float myY = y_dut[0];
    
    // cut on BS
    if( myX == -999 || myY == -999 ) continue;
    if( fabs(myX-centerX) > BSX || fabs(myY-centerY) > BSY ) continue;    
    
    
    float time_ref = gaus_mean[timech_id[0]];
    
    //cut on MCP amp
    if( amp[ampch_id[0]] < ampmin_cut[0] ||
        amp[ampch_id[0]] > ampmax_cut[0] )
      continue;
    //cut on MCP time
    if ( time_ref < std::max(time_peak[0]-time_sigma[0]*nSigmaTimeCut,lowerTimeCut) ||
         time_ref > std::min(time_peak[0]+time_sigma[0]*nSigmaTimeCut,upperTimeCut) )
      continue;
    
    
    // selected bar
    if( amp[ampch_id[1]] < std::max(mip_peak[1]*rel_amp_cut_low,ampmin_cut[1]) ) continue;
    if( amp[ampch_id[1]] > std::min(mip_peak[1]*rel_amp_cut_hig,ampmax_cut[1]) ) continue;
    if( amp[ampch_id[2]] < std::max(mip_peak[2]*rel_amp_cut_low,ampmin_cut[2]) ) continue;
    if( amp[ampch_id[2]] > std::min(mip_peak[2]*rel_amp_cut_hig,ampmax_cut[2]) ) continue;
    if( time[timech_id[1]] < std::max(time_peak[1]-time_sigma[1]*nSigmaTimeCut,lowerTimeCut) ) continue;
    if( time[timech_id[1]] > std::min(time_peak[1]+time_sigma[1]*nSigmaTimeCut,upperTimeCut) ) continue;
    if( time[timech_id[2]] < std::max(time_peak[2]-time_sigma[2]*nSigmaTimeCut,lowerTimeCut) ) continue;
    if( time[timech_id[2]] > std::min(time_peak[2]+time_sigma[2]*nSigmaTimeCut,upperTimeCut) ) continue;
    
    float amp1 = amp[ampch_id[1]];
    float amp2 = amp[ampch_id[2]];
    float time1 = time[timech_id[1]];
    float time2 = time[timech_id[2]];
    float time1_ampCorr = time1 - fitAmpCorr[1]->Eval(amp1) + fitAmpCorr[1]->Eval(h_amp_cut[1]->GetMean());
    float time2_ampCorr = time2 - fitAmpCorr[2]->Eval(amp2) + fitAmpCorr[2]->Eval(h_amp_cut[2]->GetMean());
    
    float deltat_avg = 0.5*(time1+time2) - time_ref;
    float deltat_avg_ampCorr = 0.5*(time1_ampCorr+time2_ampCorr) - time_ref;
    float deltat_wei_ampCorr = ( time1_ampCorr/pow(sigmaLeft,2) + time2_ampCorr/pow(sigmaRight,2) ) / ( 1/pow(sigmaLeft,2) + 1/pow(sigmaRight,2) ) - time_ref;

    float posCorr = -1.*fitFunc_corrX->Eval(myX) + fitFunc_corrX->Eval(centerX);
    float diffCorr = -1.*fitFunc_corrDiff->Eval(time2_ampCorr-time1_ampCorr) + fitFunc_corrDiff->Eval(h_deltat_diff->GetMean());

    h_deltat_wei_ampCorr -> Fill( deltat_wei_ampCorr );
    h_deltat_avg_ampCorr_posCorr -> Fill( deltat_avg_ampCorr + posCorr );
    h_deltat_avg_ampCorr_diffCorr-> Fill( deltat_avg_ampCorr + diffCorr );
    
      
    ++nSelectedEntries;
  }
  std::cout << "\n>>> 4th loop: selected entries " << nSelectedEntries << std::endl;
  
  
  c_timeRes_comp->cd(2);
  h_deltat_wei_ampCorr -> SetLineColor(kOrange+1);
  h_deltat_wei_ampCorr -> SetLineWidth(2);
  h_deltat_wei_ampCorr -> Draw("same");
  h_deltat_avg_ampCorr_posCorr -> SetLineColor(kViolet+1);
  h_deltat_avg_ampCorr_posCorr -> SetLineWidth(2);
  h_deltat_avg_ampCorr_posCorr -> Draw("same");  
  
  TF1* fitdeltat_wei_ampCorr = new TF1("fitdeltat_wei_ampCorr", "gaus", h_deltat_wei_ampCorr->GetMean()-h_deltat_wei_ampCorr->GetRMS()*2, h_deltat_wei_ampCorr->GetMean()+h_deltat_wei_ampCorr->GetRMS()*2);
  fitdeltat_wei_ampCorr->SetLineColor(kOrange+1);
  h_deltat_wei_ampCorr->Fit(fitdeltat_wei_ampCorr, "QR");
  
  TF1* fitdeltat_avg_ampCorr_posCorr = new TF1("fitdeltat_avg_ampCorr_posCorr", "gaus", h_deltat_avg_ampCorr_posCorr->GetMean()-h_deltat_avg_ampCorr_posCorr->GetRMS()*2, h_deltat_avg_ampCorr_posCorr->GetMean()+h_deltat_avg_ampCorr_posCorr->GetRMS()*2);
  fitdeltat_avg_ampCorr_posCorr->SetLineColor(kViolet+1);
  h_deltat_avg_ampCorr_posCorr->Fit(fitdeltat_avg_ampCorr_posCorr, "QR");
  
  float sigmaWeiCorr    = sqrt(pow(fitdeltat_wei_ampCorr->GetParameter(2),2)         - pow(sigma_ref,2) );
  float sigmaAvgCorrPos = sqrt(pow(fitdeltat_avg_ampCorr_posCorr->GetParameter(2),2) - pow(sigma_ref,2) );
  
  leg = new TLegend(0.65,0.68,0.80,0.93,NULL,"brNDC");
  leg->SetBorderSize(0);
  leg->SetTextFont(42);
  leg->SetTextSize(0.03);
  leg->SetLineColor(1);
  leg->SetLineStyle(1);
  leg->SetLineWidth(1);
  leg->SetFillColor(0);  
  leg->AddEntry(h_deltat_left_ampCorr,       Form("#sigma^{left}_{t} = %.1f ps", sigmaLeftCorr*1000), "l");     
  leg->AddEntry(h_deltat_right_ampCorr,      Form("#sigma^{right}_{t} = %.1f ps", sigmaRightCorr*1000), "l");
  leg->AddEntry(h_deltat_avg_ampCorr,        Form("#sigma^{avg}_{t} = %.1f ps", sigmaAvgCorr*1000), "l");
  leg->AddEntry(h_deltat_wei_ampCorr,        Form("#sigma^{wei}_{t} = %.1f ps", sigmaWeiCorr*1000), "l");
  leg->AddEntry(h_deltat_avg_ampCorr_posCorr,Form("#sigma^{avg+pos}_{t} = %.1f ps", sigmaAvgCorrPos*1000), "l");
  leg->Draw("same");


  // print canvasses
  printCanvas(c_timeRes_vs_XY, outputDir, timeAlgo);    
  printCanvas(c_timeRes_vs_X_Y, outputDir, timeAlgo);    
  printCanvas(c_beamXY, outputDir, timeAlgo);
  printCanvas(c_amp_vs_XY, outputDir, timeAlgo);
  printCanvas(c_amp, outputDir, timeAlgo);  
  printCanvas(c_time, outputDir, timeAlgo);
  printCanvas(c_time_vs_amp, outputDir, timeAlgo);  
  printCanvas(c_time_vs_X, outputDir, timeAlgo);  
  printCanvas(c_timeRes_comp, outputDir, timeAlgo);  
  printCanvas(c_timeRes_vs_BS, outputDir, timeAlgo);    

 
}
