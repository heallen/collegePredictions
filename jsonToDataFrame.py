import pandas as pd
import re



def readJson():
	jsonFile = 'profiles.json'
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
			return num
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
		if len(num) == 1:
			if 'k' in num[0]:
				n = re.findall("\d+", num[0])
				return int(n[0]) * 1000
			elif ',' in num[0]:
				n = num[0].replace(',','')
				return int(n)
		if len(num) == 2:
			if 'k' in num[0] or 'k' in num[1]:
				n1 = int(re.findall("\d+", num[0])[0]) * 1000
				n2 = int(re.findall("\d+", num[1])[0]) * 1000
			elif ',' in num[0] or ',' in num[1]:
				n1 = int(num[0].replace(',',''))
				n2 = int(num[1].replace(',',''))
			average = (n1 + n2)/ 2
			return average
	return 0

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
		hispanic = {'hispanic', 'puerto rican', 'mexican'}
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

#NEED TO EDIT
def standardizeCountry(country):
	if country and type(country) != float:
		us = {'us', 'usa', 'united states', 'america'}
		uk = {'england', 'britain', 'uk'}
		countries = {'us', 'uk', 'canada', 'chile', 'netherlands'}
		if any(word in country.lower() for word in countries):
			return 'country'
	return None

#NEED TO EDIT
def standardizeState(state):
	if state and type(state) != float:
		#map abbreviations to names in another file and return abrev.
		return state
	return None

#DONE
def standardizeGender(gen):
	if gen and type(gen) != float:
		female = {'female', 'f'}
		male = {'male', 'm', 'bro', 'masculine', 'XY'}
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


def main():
	data = readJson()

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

	#need to make json map of all posibilities (find online)
	# data['country'] = data['country'].map(standardizeCountry)
	# data['state'] = data['state'].map(standardizeState)


	# to edit states.json to all lowercase - not needed for more than one run
	# jsonFile = 'states.json'
	# states = pd.read_json(jsonFile)
	# states = states.apply(lambda x: x.astype(str).str.lower())
	# states.to_json(jsonFile)

	categories = ['act', 'gpa', 'ap', 'ib', 'sat1', 'sat2', 'income', 'rank', 'gender', 'ethnicity', 'decision']
	final_data = data.filter(categories, axis=1)
	final_data.to_csv('updatedProfiles.csv')

main()