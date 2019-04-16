from AllModules import *
CMD = 'tail ' 
CMD += '$(find . -type f -printf "%T@ %p\n" | sort -n | tail -1 | cut -f2- -d" " )' 
while True:
	os.system(CMD)
	time.sleep(4)