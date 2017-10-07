import scrt
import json
import urllib.request
import urllib.parse
import timeit


"""
bingME!
Input: query generated
Output: JSON file (to be the image)


"""
def bingMe(query,callnum):
	k,v = scrt.getMSFTKey()

	args = urllib.parse.urlencode({'q': query.replace(' ','+'), k: v, 'mkt': 'en-us'})

	query = query.replace(' ','+')
	submission = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search?{0}'.format(args)
	#submission = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search?q={0}&{1}={2}&mkt=en-us'.format(query,k,v)
	response = urllib.request.urlopen(submission).read().decode('utf-8')
	#data = json.load(response) ##NEED STR NOT BYTE
	print(response)
	fin = open('{0}-{1}.json'.format(callnum,query),'w+')
	fin.write(response)
	print('Completed.')