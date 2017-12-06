import pandas as pd
import re

def readJson(fileName):
	jsonFile = fileName
	data = pd.read_json(jsonFile)
	return data

#DONE
def quantifyACT(act):
	if act and type(act) != float:
		score = act.split()
		if any(i.isdigit() for i in score[0]):
			num = re.findall("\d+", score[0])
			return num[0]
	return 0

#DONE
def quantifyAP(ap):
	if ap and type(ap) != float:
		num = re.findall("\d+", ap)
		if num:
			return list(map(int, num))
	return 0

#DONE
# assumed ib that wasn't 1-7 already was out of 45 points
def quantifyIB(ib):
	if ib and type(ib) != float:
		num = re.findall("\d+", ib)
		num = list(map(int, num))
		if num:
			if any(n > 10 for n in num):
				num = [min(int(round(float(n)/6)),7) if n > 10 else int(n) for n in num]
			return num
	return 0

#could try to make more accurate
def quantifyGPA(gpa):
	if gpa and type(gpa) != float:
		num = re.findall(r"[-+]?\d*\.\d+|[-+]?\d+", gpa)
		if num:
			if float(num[0]) <= 4.0:
				return float(num[0])
			elif float(num[0]) < 10:
				return float(num[0]) - 1
			elif float(num[0]) > 60:
				grade = float(num[0])/20 - 1
				return grade
	return 0

# DONE - if 2400 is chill
# ALL OUT OF 2400
# 26 scores out of 1600
def quantifySAT(sat):
	if sat and type(sat) != float:
		num = re.findall("\d+", sat)
		num = list(map(int, num))
		if num:
			for n in num:
				# if n > 800 and n <1600:
				# 	print n
				if n > 1600:
					return n
			if len(num) == 3:
				if all(n > 400 and n <=800 for n in num):
					return int(sum(num))
	return 0

#DONE
def quantifySAT2(sat2):
	if sat2 and type(sat2) != float:
		num = re.findall("\d+", sat2)
		results = filter(lambda x: x > 100, list(map(int, num)))
		return results
	return 0

#DONE
def quantifyIncome(inc):
	if inc and type(inc) != float:
		num = re.findall("\d+[,,k]\d*", inc)
		if num:
			income = 0
			if len(num) == 1:
				if 'k' in num[0]:
					n = re.findall("\d+", num[0])
					income =  int(n[0]) * 1000
				elif ',' in num[0]:
					n = num[0].replace(',','')
					income = int(n)
			elif len(num) == 2:
				if 'k' in num[0] or 'k' in num[1]:
					n1 = int(re.findall("\d+", num[0])[0]) * 1000
					n2 = int(re.findall("\d+", num[1])[0]) * 1000
				elif ',' in num[0] or ',' in num[1]:
					n1 = int(num[0].replace(',',''))
					n2 = int(num[1].replace(',',''))
				income = (n1 + n2)/ 2
			if income < 50000:
				return 'lower'
			elif income < 100000:
				return 'lower-middle'
			elif income < 200000:
				return 'middle'
			elif income < 400000:
				return 'upper-middle'
			elif income >= 400000:
				return 'upper'
		else:
			lower = {'lower', 'lowest'}
			lower_middle = {'lower-middle', 'lower middle'}
			middle = {'middle'}
			upper_middle= {'upper-middle', 'upper middle'}
			upper = {'high', 'highest', 'upper'}
			if any(word in inc.lower() for word in lower_middle):
				return 'lower-middle'
			elif any(word in inc.lower() for word in upper_middle):
				return 'upper-middle'
			elif any(word in inc.lower() for word in middle):
				return 'middle'
			elif any(word in inc.lower() for word in lower):
				return 'lower'
			elif any(word in inc.lower() for word in upper):
				return 'upper'
	return 'N/A'

# DONE
#floats
def quantifyRank(rank):
	if rank and type(rank) != float:
		percent = re.findall("\d+%", rank)
		fraction = re.findall("\d+/\d+", rank)
		if percent:
			p = float(re.findall("\d+", percent[0])[0])/100
			if p > .5:
				return 1 - p
			else:
				return p
		elif fraction:
			f = float(fraction[0].split('/')[0])/int(fraction[0].split('/')[1])
			return f
	return 0

# Grouping can be changed
def standardizeEthnicity(eth):
	if eth and type(eth) != float:
		#how to handle 'mixed' with listed ethnicities
		white = {'white', 'caucasian', 'w', 'croatian'}
		hispanic = {'hispanic', 'puerto rican', 'mexican', 'latino'}
		african = {'black', 'nigerian', 'african'}
		asian = {'chinese', 'asian', 'thai', 'vietnamese', 'korean', 'filipino',  'nepali'}
		indian = {'indian'}
		#Also african american and hispanic are considered urm
		urm = {'urm', 'native american'}
		if any(word in eth.lower() for word in white):
			return 'caucasian'
		elif any(word in eth.lower() for word in hispanic):
			return 'hispanic'
		elif any(word in eth.lower() for word in asian):
			return 'asian'
		elif any(word in eth.lower() for word in african):
			return 'african'
		# urm before indian so native american is check before indian
		elif any(word in eth.lower() for word in urm):
			return 'urm'
		elif any(word in eth.lower() for word in indian):
			return 'indian'
	return None

#DONE
def standardizeState(state, states):
	if state and type(state) != float:
		states_abbrev = states['abbreviation']
		states_full = states['name']
		if any(len(s) == 2 for s in state.split()):
			for s in state.split():
				if len(s) == 2:
					state = s
			for word in states_abbrev:
				if word in state.lower():
					return word
		for word in states_full:
			if word in state.lower():
				abbrev = states.loc[(states['name'] == word), ['abbreviation']]
				return abbrev.values[0][0]
	return None

#update country to US if state found
def updateCountryByState(row):
	if row['state'] != None:
		row['country'] = 'US'
	return row

#DONE
def standardizeCountry(country, states):
	if country and type(country) != float:
		states_abbrev = states['abbreviation']
		states_full = states['name']
		us = {'us', 'usa', 'united states', 'america', 'u.s.a', 'u.s.', 'u!s!a!', 'u.s.a.'}
		# uk = {'england', 'britain', 'uk'}
		# countries = {'us', 'uk', 'canada', 'chile', 'netherlands'}
		if any(word in country.lower() for word in us) or \
		   any(word in country.lower() for word in states_abbrev) or \
		   any(word in country.lower() for word in states_full):
			return 'US'
		else:
			if 'n/a' in country.lower():
				return None
			else:
				return 'international'
	return None


#DONE
def standardizeGender(gen):
	if gen and type(gen) != float:
		female = {'female', 'f'}
		male = {'male', 'm', 'bro', 'masculine', 'XY', 'man'}
		if any(word in gen.lower() for word in female):
			return 'F'
		elif any(word in gen.lower() for word in male):
			return 'M'
	return None

#DONE
def standardizeDecision(dec):
	if dec and type(dec) != float:
		accepted = {'accepted'}
		rejected = {'rejected'}
		waitlisted = {'waitlisted', 'waitlist'}
		deferred = {'deferred'}
		if any(word in dec.lower() for word in accepted):
			return 'A'
		elif any(word in dec.lower() for word in rejected):
			return 'R'
		elif any(word in dec.lower() for word in waitlisted):
			return 'W'
		elif any(word in dec.lower() for word in deferred):
			return 'D'
	return None

def updateKeywords(row):
	if row['hooks'] and type(row['hooks']) != float:
		hooks = row['hooks'].lower()
 		if 'urm' in hooks:
 			row['urm'] = True
 		if 'first generation' in hooks:
 			row['first_generation'] = True

 	if row['extracurriculars'] and type(row['extracurriculars']) != float:
		leadership = row['extracurriculars'].lower()
		editor = {'editor in chief', 'editor-in-chief'}
		if any(word in leadership for word in editor):
			row['editor-in-chief'] = True 
		if 'founder' in leadership:
 			row['founder'] = True
 		if 'president' in leadership:
 			row['president'] = True
 		if 'captain' in leadership:
 			row['captain'] = True
 	
 	if row['awards'] and type(row['awards']) != float:
		awards = row['awards'].lower()
		siemens = {'siemens competition semifinalist', 'siemens competition finalist'}
		presidential = {'presidential scholar', 'presidential scholars'}
		national_merit = {'national merit', 'nm', 'nmf'}
		if any(word in awards for word in siemens):
			row['siemens'] = True 
		if 'intel' in awards:
 			row['intel'] = True
		if any(word in awards for word in presidential):
			row['presidential_scholar'] = True 
		if any(word in awards for word in national_merit):
			row['national_merit'] = True
		if 'ap scholar' in awards:
 			row['ap_scholar'] = True
 		if 'aime' in awards:
 			row['aime'] = True
 		if 'imo' in awards:
 			row['imo'] = True
 		if 'national achievement' in awards:
 			row['national_achievement'] = True
 		if 'olympiad' in awards:
 			row['olymdpiad'] = True

	return row

def main():
	data = readJson('profiles.json')
	states = readJson('states.json')

	# QUANTITIES
	data['act'] = data['act'].map(quantifyACT)
	data['gpa'] = data['gpa'].map(quantifyGPA)
	data['ap'] = data['ap'].map(quantifyAP)
	data['ib'] = data['ib'].map(quantifyIB)
	data['sat1'] = data['sat1'].map(quantifySAT)
	data['sat2'] = data['sat2'].map(quantifySAT2)
	data['income'] = data['income'].map(quantifyIncome)
	data['rank'] = data['rank'].map(quantifyRank)
	
	# BINARY
	data['gender'] = data['gender'].map(standardizeGender)

	# SET OF LABELS
	data['ethnicity'] = data['ethnicity'].map(standardizeEthnicity)
	data['decision'] = data['decision'].map(standardizeDecision)
	data['state'] = data['state'].apply(lambda x: standardizeState(x, states))
	data = data.apply(updateCountryByState, axis=1)
	# binary
	data['country'] = data['country'].apply(lambda x: standardizeCountry(x, states))

	# KEYWORDS - BINARY
	data = data.apply(updateKeywords, axis=1)

	categories = ['act', 'gpa', 'ap', 'ib', 'sat1', 'sat2', 'income', 'rank', 'gender', 'ethnicity', \
	'decision', 'state', 'country', 'urm', 'first_generation', 'editor-in-chief', 'founder', 'president', \
	'captain', 'siemens', 'intel', 'presidential_scholar', 'national_merit', 'ap_scholar', 'aime', 'imo', \
	'national_achievement', 'olympaid']
	updated_data = data.filter(categories, axis=1)
	updated_data.to_csv('updatedProfiles.csv')
	updated_data.to_pickle('updatedProfiles.pkl')

	data.to_csv('full_updatedProfiles.csv', encoding='utf-8')

main()