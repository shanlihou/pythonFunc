import urllib2

def getIsNeedStop():
	url = 'http://127.0.0.1:8000/control?isNeedClose=1'
	resp = urllib2.urlopen(url).read()
	print resp

getIsNeedStop()
