import scrt
import json
import urllib.request
import urllib.parse
import time


"""
bingME
Input: query generated, call # (for json filename)
Output: JSON file (to be the image)


"""
def bingMe(query,callnum,count=35):
	start = time.time()
	k,v = scrt.getMSFTKey()

	args = urllib.parse.urlencode({'q': query.replace(' ','+'), k: v, 'mkt': 'en-us','count':count,'size':'large'})

	#backup
	#submission = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search?q={0}&{1}={2}&mkt=en-us'.format(query,k,v)
	
	submission = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search?{0}'.format(args)
	response = urllib.request.urlopen(submission).read().decode('utf-8')
	#data = json.loads(response)
	
	#print(json.dumps(data))

	#writing to file, this erases the file if it already existed
	fin = open('data/{0}-{1}.json'.format(callnum,query),'w+')
	fin.close()

	fin = open('data/{0}-{1}.json'.format(callnum,query),'w+')
	fin.write(response)
	end = time.time()
	fin.close()
	print('Completed in {0}s.'.format(end-start))



##need to get from JSON to image on GOOGLE then get name also