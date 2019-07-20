import re

def extractor(tupple):
	reducedTriplets= []
	secondtuple = tupple
	mylist = tupple[0].split()
	tags = []

	k=0
	while k<len(mylist):
		tags.append(re.search(r'\^.*',mylist[k]).group()[1:])
		mylist[k] = re.search(r'.*\^',mylist[k]).group()[:-1]
		k+=1

	k=0
	pos = ""
	jj = ""
	cd = ""
	while k < len(tags):
		if (tags[k] == "POS" and k+1 < len(tags)):
			pos = ' '.join(mylist[:k+1])
			mylist = mylist[k+1:]
			tags = tags[k+1:]
			k=-1

		elif (tags[k] == "JJ"):
			jj = jj + " " + mylist[k]
			mylist = mylist[:k] + (mylist[k+1:] if k+1 < len(mylist) else [])
			tags = tags[:k] + (tags[k+1:] if k+1 < len(tags) else [])
			k=-1

		elif (tags[k] == "CD"):
			cd = mylist[k]
			mylist = mylist[:k] + (mylist[k+1:] if k+1 < len(mylist) else [])
			tags = tags[:k] + (tags[k+1:] if k+1 < len(tags) else [])
			k=-1
		k+=1

	k=0
	while k<len(tags):
		tags[k] = mylist[k]+"^"+tags[k]
		k+=1

	reducedTriplets.append([' '.join(tags), tupple[1]])
	if (pos != ""):
		reducedTriplets.append([' '.join(mylist), 'belongs-to', pos.strip("'s")])
	if (jj != ""):
		for x in jj.strip().split():
			reducedTriplets.append([x, 'quality', ' '.join(mylist)])
	if (cd != ""):
		reducedTriplets.append([cd, 'number', ' '.join(mylist)])
	return reducedTriplets

tupple = ("Mehar^NNP Sharma^NNP 's^POS blue^NN coloured^VBD jacket^NN", 'NP')
for x in extractor(tupple):
	print(x)