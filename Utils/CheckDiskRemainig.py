import argparse
import commands
import time

parser = argparse.ArgumentParser()
parser.add_argument ('-d', '--disk', type=str, default='/dev/sdb4', help='Disk or volume to check')
parser.add_argument ('-l', '--limit', type=str, default='10G', help='Limit disk space')
args = parser.parse_args()

size_dic = {'P': 1024**5, 'T': 1024**4, 'G':1024**3, 'M':1024**2, 'K': 1024}

Nlim =  float(args.limit[:-1])*size_dic[args.limit[-1]]

while(True):
	_, out = commands.getstatusoutput('df -h | grep \"' + args.disk + '\"')
	out = [x for x in out.split(' ') if x]

	sfree = out[3]
	Nfree = float(sfree[:-1])*size_dic[sfree[-1]]

	if Nfree <= Nlim:
		print time.ctime(time.time())
		print 'Limit memory reached!'
		print '[WARNING]: Only {} free left on disk {} ({})\n\n'.format(sfree, out[0], out[-1])
	
	time.sleep(5)
