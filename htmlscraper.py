import urllib2
import re
from bs4 import BeautifulSoup
import json

url = 'https://talk.collegeconfidential.com/harvard-university/1480236-official-harvard-university-2017-rd-results.html'
page = urllib2.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
messages = soup.find_all('div', attrs={'class': 'Message'})

profiles = []

for message in messages:
	lines = str(message).splitlines()
	profile = {}
	for line in lines:
		if 'Decision' in line:
			startIndex = line.find('Decision:') + len('Decision:')
			endIndex = line.find('</b>', startIndex)
			if endIndex != -1:
				profile['decision'] = line[startIndex: endIndex].strip()

		elif 'SAT I ' in line or 'SATI ' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['sat1'] = line[startIndex: endIndex].strip()

		elif 'ACT:' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['act'] = line[startIndex: endIndex].strip()

		elif 'SAT II:' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['sat2'] = line[startIndex: endIndex].strip()

		elif 'Unweighted GPA' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['gpa'] = line[startIndex: endIndex].strip()

		elif 'AP (place score' in line or 'AP:' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['ap'] = line[startIndex: endIndex].strip()

		elif 'IB (place score' in line or 'IB:' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['ib'] = line[startIndex: endIndex].strip()

		elif 'Senior Year Course Load' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['courseload'] = line[startIndex: endIndex].strip()

		elif 'Major Awards' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['awards'] = line[startIndex: endIndex].strip()

		elif 'Extracurriculars (place leadership' in line or 'Extracurriculars:' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['extracurriculars'] = line[startIndex: endIndex].strip()

		elif 'Job/Work Experience' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['jobexp'] = line[startIndex: endIndex].strip()
		
		elif 'Volunteer/Community' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['volunteer'] = line[startIndex: endIndex].strip()

		elif 'Summer Activities:' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['summer'] = line[startIndex: endIndex].strip()

		elif 'Essays (rating' in line or 'Essays:' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['essay'] = line[startIndex: endIndex].strip()

		### TODO: RECOMMENDATIONS

		elif 'Interview:' in line :
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['interview'] = line[startIndex: endIndex].strip()

		elif 'State (if domestic applicant):' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['state'] = line[startIndex: endIndex].strip()

		elif 'Country (if international applicant):' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['country'] = line[startIndex: endIndex].strip()

		elif 'School Type:' in line: 
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['schooltype'] = line[startIndex: endIndex].strip()

		elif 'Ethnicity:' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['ethnicity'] = line[startIndex: endIndex].strip()

		elif 'Gender:' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['gender'] = line[startIndex: endIndex].strip()

		elif 'Income Bracket:' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['income'] = line[startIndex: endIndex].strip()

		elif 'Hooks:' in line or 'Hooks (URM' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['hooks'] = line[startIndex: endIndex].strip()

		elif 'Strengths:' in line or 'Hooks (URM' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['strengths'] = line[startIndex: endIndex].strip()

		elif 'Weaknesses:' in line or 'Hooks (URM' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['weaknesses'] = line[startIndex: endIndex].strip()

		elif 'Why you think you were' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['whydecision'] = line[startIndex: endIndex].strip()

		elif 'Where else were you' in line:
			startIndex = line.find(':') + 1
			endIndex = line.find('</li>', startIndex)
			if endIndex != -1:
				profile['otherschools'] = line[startIndex: endIndex].strip()

		elif 'General Comments' in line:
			startIndex = line.find('</b>') + 4
			endIndex = line.find('</div>', startIndex)
			if endIndex != -1:
				profile['comments'] = line[startIndex: endIndex].strip()

	profiles.append(profile)

#use if just need valid JSON, save space
# output = json.dumps(profiles)

#prettifies JSON
output = json.dumps(profiles, indent=4, sort_keys=True)

f = open('profiles.txt', 'w')
f.write(output)
f.close()

