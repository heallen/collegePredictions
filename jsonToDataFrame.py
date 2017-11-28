import pandas as pd
import re



def readJson():
	jsonFile = 'profiles.json'
	data = pd.read_json(jsonFile)
	return data

def quantifyACT(act):
	if act and type(act) != float:
		score = act.split()
		if any(i.isdigit() for i in score[0]):
			num = re.findall("\d+", score[0])
			return num[0]
		else:
			return None
	return None

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
	return None

#fix
def quantifySAT(sat):
	if sat and type(sat) != float:
		num = re.findall("\d+", sat)
		if num:
			if int(num[0]) > 1600:
				writing = {'writing', 'w', 'wr'}
			else:
				return num[0]
	return None

def quantifySAT2(sat2):
	if sat2 and type(sat2) != float:
		num = re.findall("\d+", sat2)
		results = filter(lambda x: x > 100, list(map(int, num)))
		return results
	return None

#Not done at all
def quantifyIncome(inc):
	if inc and type(inc) != float:
		return inc
	return None

def standardizeGender(gen):
	if gen and type(gen) != float:
		female = {'female', 'f'}
		male = {'male', 'm', 'bro', 'masculine', 'XY'}
		if any(word in gen.lower() for word in female):
			return 'F'
		elif any(word in gen.lower() for word in male):
			return 'M'
	return None

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
	data['act'] = data['act'].map(quantifyACT)
	data['gpa'] = data['gpa'].map(quantifyGPA)
	data['sat1'] = data['sat1'].map(quantifySAT)
	data['sat2'] = data['sat2'].map(quantifySAT2)
	data['income'] = data['income'].map(quantifyIncome)
	data['gender'] = data['gender'].map(standardizeGender)
	data['decision'] = data['decision'].map(standardizeDecision)
	for d in data['income']:
		print d

main()