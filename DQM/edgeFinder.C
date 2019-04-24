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

int returnNumberOfBinsAboveAmpThreshold(TProfile* _tp0, double _threshold = 0.35)
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

void edgeFinder(const int& firstRun, const int& lastRun, string outputDir="./", string isCondor="")
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
  std::string dataFolder = "/data2/2019_04_April_CMSTiming/VME/RecoData/RecoWithTracks/v3/"; // BBT, 4-18-19, local
  //std::string dataFolder = "/eos/uscms/store/group/cmstestbeam/2019_04_April_CMSTiming/VME/RecoData/RecoWithTracks/v3/"; // BBT, 4-18-19, LPC EOS
  if (isCondor=="True")
    dataFolder = "root://cmseos.fnal.gov//store/group/cmstestbeam/2019_04_April_CMSTiming/VME/RecoData/RecoWithTracks/v3/"; // BBT, 4-18-19, LPC EOS
  //std::string dataFolder = "/data2/2019_04_April_CMSTiming/VME/RecoData/RecoWithTracks/v3/";
  
  //----------------
  // define channels
  
  
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

  TProfile2D* h_box1   = new TProfile2D("h_box1", "Top Bar", 200, -10, 40, 160, 0, 40);
  TProfile2D* h_box2   = new TProfile2D("h_box2", "Middle Bar", 200, -10, 40, 160, 0, 40);  
  TProfile2D* h_box3   = new TProfile2D("h_box3", "Bottom Bar", 200, -10, 40, 160, 0, 40);
  TProfile2D* h_single = new TProfile2D("h_single", "h_single", 200, -10, 40, 160, 0, 40);
  TCanvas* c_box1 = new TCanvas("c_box1", "c_box1", 800, 800);
  TCanvas* c_box2 = new TCanvas("c_box2", "c_box2", 800, 800);
  TCanvas* c_box3 = new TCanvas("c_box3", "c_box3", 800, 800);
  TCanvas* c_single = new TCanvas("c_single", "c_single", 800, 800);



  c_box1->cd();
  myTree->Draw("amp[1] > 400 :  y_dut[0]:x_dut[0]>>+h_box1", "ntracks==1", "profcolz");

  c_box2->cd();
  myTree->Draw("amp[2] > 400 :  y_dut[0]:x_dut[0]>>+h_box2", "ntracks==1", "profcolz");

  c_box3->cd();
  myTree->Draw("amp[3] > 400 :  y_dut[0]:x_dut[0]>>+h_box3", "ntracks==1", "profcolz");

  c_single->cd();
  myTree->Draw("amp[20] > 200 :  y_dut[0]:x_dut[0]>>+h_single", "ntracks==1", "profcolz");

  return;

}
