import urllib2 
import re
import sys
def getUrlList(urlPath):
	response = urllib2.urlopen(urlPath)
	html = response.read()
	pattern = re.compile(r'http://www\.btspread\.com/magnet/detail/hash/[A-F0-9]+')
	patFind = pattern.search(html)
	if (patFind):
		matchList = pattern.findall(html)
		return matchList
	return None

def getMagnet(urlPath):
	response = urllib2.urlopen(urlPath)
	html = response.read()
	pattern = re.compile(r'(magnet:\?xt=urn:btih:[^"\']+)" class=')
	patFind = pattern.search(html)
	if (patFind):
		print patFind.group(1)
		print '\n'

def getAllMagnet(code):
	List = getUrlList('http://www.btspread.com/search/' + code)
	if (List != None):
		for url in List:
			getMagnet(url)

if (len(sys.argv) == 2):
	getAllMagnet(sys.argv[1])
