# Python 3
# Get the HTML version of the Earth article on English Wikipedia

import requests
page = "Earth"
url = 'https://api.wikimedia.org/core/v1/wikipedia/en/page/' + page + '/html'

response = requests.get(url)
responseText = response.text
content = False
i=0
while(i<len(responseText)-2):
	if(not content):
		if(responseText[i]=='>' and responseText[i+1]=='<'):
			content=True
		elif(responseText[i]=='<' and responseText[i+1]=='p'):
			content=True
			while(responseText[i]!='>'):
				i+=1				
	else:
		#print()
		#print(i)
		if(responseText[i]=='<'):
			content = False
		else:
			print(responseText[i],end="")
	i+=1
