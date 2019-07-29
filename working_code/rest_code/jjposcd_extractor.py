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
			p = k-1
			p2 = p
			while p >= 0 and "NN" in tags[p]:
				pos = pos + " " + mylist[p2-p]
				p-=1
			# pos = ' '.join(mylist[:k+1])
			if(p==-1):
				mylist = mylist[k+1:]
				tags = tags[k+1:]
			else:
				# print(mylist, tags, p)
				mylist = mylist[:p+1]+mylist[k+1:]
				tags = tags[:p+1]+tags[k+1:]
			k=-1

		elif (tags[k] == "JJ" and len(tags)==1 and (mylist[0][0] >='a' and mylist[0][0]<='z')): #cut it from the list, if the adjective is the only thing present in the phrase AND it begins with a small letter (a-z)
			jj = jj + " " + mylist[k]
			mylist = mylist[:k] + (mylist[k+1:] if k+1 < len(mylist) else [])
			tags = tags[:k] + (tags[k+1:] if k+1 < len(tags) else [])
			k=-1

		elif (tags[k] == "CD" and len(tags) > 1):
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
	if (pos != "" and len(mylist) > 0 and len(pos.strip("'s").strip()) > 0):
		reducedTriplets.append([' '.join(mylist), 'belongs-to', pos.strip("'s").strip()])
	# if (jj != "" and len(mylist) > 0):
		# for x in jj.strip().split():
		# 	reducedTriplets.append([x, 'quality', ' '.join(mylist)])
	if (cd != "" and len(mylist) > 0):
		reducedTriplets.append([cd, 'number', ' '.join(mylist)])
	return reducedTriplets

if __name__ == "__main__":
	tupple = ("many^JJ", 'NP')
	print(tupple)
	for x in extractor(tupple):
		print(x)