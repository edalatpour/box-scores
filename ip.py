import socket

def getAddress():
	testIP = "8.8.8.8"
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect((testIP, 0))
	ipaddr = s.getsockname()[0]
	host = socket.gethostname()
	return(ipaddr)

