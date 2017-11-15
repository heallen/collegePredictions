import urllib2
import re
from bs4 import BeautifulSoup

url = 'https://talk.collegeconfidential.com/harvard-university/1480236-official-harvard-university-2017-rd-results.html'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
messages = soup.find_all('div', attrs={'class': 'Message'})

## TODO: normalize inputs (at least lowercase all terms, extract keywords)

for message in messages:
	lines = str(message).splitlines()
	profile = {}
	for line in lines:
		if 'Decision' in line:
			if 'Rejected' in line or 'rejected' in line:
				profile['decision'] = 'r'
			elif 'Accepted' in line or 'accepted' in line:
				profile['decision'] = 'a'
			elif 'Waitlisted' in line or 'waitlisted' in line or 'waitlist' in line:
				profile['decision'] = 'w'
		elif 'SAT I ' in line or 'SATI ' in line:
			nums = [int(s) for s in re.split(',|\s|-|:|/', line) if s.isdigit() and int(s) > 800]
			if(nums):
				profile['SATI'] = max(nums)
		elif 'ACT' in line:
			nums = [int(s) for s in re.split(',|\s|-|:|/', line) if s.isdigit()]
			if(nums):
				profile['ACT'] = nums[0] #assume composite score is the first to be listed
		elif 'SAT II' in line:
			nums = [int(s) for s in re.split(',|\s|-|:|/', line) if s.isdigit()]
			if(nums):
				profile['SATII'] = sum(nums)/len(nums) #average score of SATII tests
				profile['nSATII'] = len(nums) #number of SATII's taken
			else:
				profile['nSATII'] = 0
		elif 'State (if domestic applicant):' in line:
			# Line format: <li>State (if domestic applicant): NJ</li>
			state = line.split(':')[1].split('<')[0].strip()
			if state:
				profile['state'] = state
		elif 'Country (if international applicant):' in line:
			country = line.split(':')[1].split('<')[0].strip()
			if country:
				profile['country'] = country
		elif 'School Type:' in line: 
			# need to normalize this data, search for 'public', 'private', 'magnet', etc?
			schoolType = line.split(':')[1].split('<')[0].strip() 
			if schoolType:
				profile['schoolType'] = schoolType
		elif 'Ethnicity:' in line:
			ethnicity = line.split(':')[1].split('<')[0].strip()
			if ethnicity:
				profile['ethnicity'] = ethnicity
		elif 'Gender:' in line:
			# TODO: normalize to just 'F' or 'M'
			gender = line.split(':')[1].split('<')[0].strip()
			if gender:
				profile['gender'] = gender
				
		## TODO: figure out how to extract AP scores and GPA reliably
		# if 'AP' in line:
		# 	nums = [int(s) for s in re.split(',|\s|-|:|/', line) if s.isdigit()]
		# 	if(nums):
		# 		profile['AP'] = sum(nums)/len(nums)
		# 		profile['nAP'] = len(nums)
		# 	else:
		# 		profile['nAP'] = 0
		# if 'Unweighted GPA' in line:
		# 	# print line
		# 	print
		# 	nums = [float(s) for s in re.split(':', line)[1].split('\s|:|,|)|]') if re.match('\d', s)]
		# 	print nums
		# 	if(nums):
		# 		profile['GPA'] = nums[0]

	print profile