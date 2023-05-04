import socket

def getAddress():
	try:
		testIP = "192.0.0.1"
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.connect((testIP, 0))
		ipaddr = s.getsockname()[0]
		host = socket.gethostname()
		return(ipaddr)
	except:
		return("0.0.0.0")
