IncludeTelescope=1


python AutoPilot.py -it $IncludeTelescope -conf $1 -nrun $2

while [ $n -le 100 ]
do
	echo "Meraj sucks $n times."
	n=$(( n+1 ))	 # increments $n
done

