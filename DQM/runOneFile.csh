#!/bin/bash
source /cvmfs/sft.cern.ch/lcg/views/LCG_89/x86_64-slc6-gcc62-opt/setup.sh
cd ${_CONDOR_SCRATCH_DIR}
#xrdcp -s root://cmseos.fnal.gov//store/user/benjtann/$2/$7 .
tar -xf $5
rm $5

python analyzeBarForTiming.py --bar ${1} --firstRun ${2} --lastRun ${3} --timeAlgo ${4} --isCondor True

### Now that the run is over, there is one or more root files created
echo "List all produced .png files = "
ls $6/*.png
echo "List all files"
ls 
echo "*******************************************"
OUTDIR=root://cmseos.fnal.gov//store/user/benjtann/
echo "xrdcp output for condor"
for FILE in $6/*.png
do
  echo "xrdcp -f ${FILE} ${OUTDIR}/${FILE}"
  xrdcp -f ${FILE} ${OUTDIR}/${FILE} 2>&1
  XRDEXIT=$?
  if [[ $XRDEXIT -ne 0 ]]; then
    rm *.png
    echo "exit code $XRDEXIT, failure in xrdcp"
    exit $XRDEXIT
  fi
  rm ${FILE}
done
