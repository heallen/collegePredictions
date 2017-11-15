import urllib2
import re
from bs4 import BeautifulSoup

url = 'https://talk.collegeconfidential.com/harvard-university/1480236-official-harvard-university-2017-rd-results.html'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
messages = soup.find_all('div', attrs={'class': 'Message'})

for message in messages:
	lines = str(message).splitlines()
	profile = {}
	for line in lines:
		if 'SAT I ' in line or 'SATI ' in line:
			nums = [int(s) for s in re.split(',|\s|-|:|/', line) if s.isdigit() and int(s) > 800]
			if(nums):
				profile['SATI'] = max(nums)
		if 'ACT' in line:
			nums = [int(s) for s in re.split(',|\s|-|:|/', line) if s.isdigit()]
			if(nums):
				profile['ACT'] = nums[0] #assume composite score is the first to be listed
		if 'SAT II' in line:
			nums = [int(s) for s in re.split(',|\s|-|:|/', line) if s.isdigit()]
			if(nums):
				profile['SATII'] = sum(nums)/len(nums)
				profile['nSATII'] = len(nums)
			else:
				profile['nSATII'] = 0
		if 'Unweighted GPA' in line:

	print profile