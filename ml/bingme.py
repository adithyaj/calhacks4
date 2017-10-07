import scrt
import json
import urllib.request


"""
bingME!
Input: query generated
Output: JSON file (to be the image)


"""
def bingMe(query):
	k,v = scrt.getMSFTKey()
	query = query.replace(' ','+')
	submission = 'https://api.cognitive.microsoft.com/bing/v5.0/images/search?q={0}&{1}={2}&mkt=en-us'.format(query,k,v)
	response = urllib.request.urlopen(submission)
	#data = json.load(response)
	print(response.read())