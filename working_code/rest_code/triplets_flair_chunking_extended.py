from flair.models import SequenceTagger
from flair.data import Sentence
import spacy
import en_core_web_sm
import csv
import nltk
import re
from nltk import sent_tokenize, word_tokenize


# ex = 'The company also showcased it\'s latest Dynasty series of marvellous vehicles, which were recently unveiled at the company\'s spring product launch in Beijing'
# ex = 'BYD quickly debuted it\'s E-SEED GT concept car and Song Pro SUV alongside it\'s all-new e-series models at the Shanghai International Automobile Industry Exhibition'
# ex = 'Ritwik Mishra\'s lawyer appealed to Reserve Bank of India to hear the case of Nirav Modi, Mehul Choksy, Rahul Gandhi, Arvind Keriwal and Ramanujam'
# ex = "John Sowa from India exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework"
# ex = "An Indian resident, John Sowa, exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework"
# ex = "A total of 23 new car models were exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework"
# ex = "John Sowa from India exhibited amazing dancing skills and performed Salsa at the event"
# ex = "\"What is your name?\", asked John"
# ex = "That is the place where John died"
ex = "The Akash eagerly wanted Mehar Bhatia's black jackets, green umbrella of John Sowa and Ritwik Mishra's red jeans"
# ex = "John went to the market by car, and Mary went to the school"
# ex = "Akash Kumar Sharma's friend bought four new cars"
ex = "John caught the running horse"

tagger = SequenceTagger.load('chunk')

# sentence = Sentence('BYD quickly debuted it\'s E-SEED GT concept car and Song Pro SUV alongside it\'s all-new e-series models at the Shanghai International Automobile Industry Exhibition .')
sentence = Sentence(ex)

tagger.predict(sentence)
strchunked = sentence.to_tagged_string()
print("\n")
print(sentence)
print("\nChunked sentence")
print(strchunked)

nlp = en_core_web_sm.load()
doc = nlp(ex)
# pos_tags = [(i, i.tag_) for i in doc]
pos_tags = nltk.pos_tag(nltk.word_tokenize(ex))
print("\nPOS tags")
print(pos_tags)


listchunked = strchunked.split()
# print(len(listchunked))
# print(len(pos_tags))
print("\n\n")
ph = ""
sentence = []


k = 0
while k < len(listchunked):
	if listchunked[k+1] == '<S-NP>' or listchunked[k+1] == '<S-VP>' or listchunked[k+1] == '<S-PP>':
		ph = listchunked[k]
		sentence.append([(ph), (listchunked[k+1][-3:-1])])
		ph = ""
		k+=2
		# print("S")
	elif listchunked[k+1] == '<B-NP>':
		# ph = ph + listchunked[k]
		while listchunked[k+1] != '<E-NP>':
			ph = ph.strip() + " " + listchunked[k]
			k+=2
		ph = ph.strip() + " " + listchunked[k]
		sentence.append([(ph), (listchunked[k+1][-3:-1])])
		ph = ""
		k+=2
		# print("BNP")
	elif listchunked[k+1] == '<B-VP>':
		while listchunked[k+1] != '<E-VP>':
			ph = ph.strip() + " " + listchunked[k]
			k+=2
		ph = ph.strip() + " " + listchunked[k]
		sentence.append([(ph), (listchunked[k+1][-3:-1])])
		ph = ""
		k+=2
		# print(BVP)
	elif not ( listchunked[k+1][0] == '<' and listchunked[k+1][-1] == '>' ): #happens with 'CC'
		sentence.append([ listchunked[k] , 'CC'])
		k+=1
	else:
		k+=2
		# print("here")
print("CHUNKS from spacy")
for x in sentence:
	print(x)
	

print("\n\n")
k=m=0
sentence2 = []
while k < len(sentence):
	ph = ""
	for x in nltk.word_tokenize(sentence[k][0]):
		while m < len(pos_tags):
			if (x == pos_tags[m][0]):
				if(pos_tags[m][1]=="RB" or pos_tags[m][1]=="DT" or pos_tags[m][1]=="." or pos_tags[m][1]=="``"):
					break
				if (pos_tags[m][1]==","):
					sentence2.append([ ph.strip() , sentence[k][1] ])
					ph = ""
				else:
					ph = ph.strip() + " " +x+"^"+pos_tags[m][1]
				m+=1
				break
			m+=1
	if (len(ph) > 0):
		sentence2.append([ ph.strip() , sentence[k][1] ])
	elif (sentence[k][0][-1] != ','):
		sentence2.append( [sentence[k][0]+"^NN", sentence[k][1]])
	k+=1

print("CHUNKS with POS tags")
for x in sentence2:
	print(x)

sentence = sentence2

k = 0
while k < len(sentence):
	ph = sentence[k][0].split()
	p = 0
	vbfound = False
	s = ""
	while p < len(ph):
		if ( (re.search(r'.*\^',ph[p]).group()[:-1] == "'s" or re.search(r'.*\^',ph[p]).group()[:-1] == "'") and len(re.search(r'.*\^',ph[p]).group()[:-1]) <= 2 ):
			if (p-2 >= 0):
				s = ' '.join(ph[:p-1])
			s = s + " " + re.search(r'.*\^',ph[p-1]).group()[:-1] + "'s^POS " + ' '.join(ph[p+1:])
			# print(s)
			# input('ENTER')
			sentence[k] = (s.strip(), sentence[k][1])
			ph = sentence[k][0].split()
			p-=1
			s = ""
		if ("VB" in re.search(r'\^.*',ph[p]).group()[1:]):
			if not(vbfound):
				vbfound = True
			else:
				s = ' '.join(ph[p:])
				sentence[k] = (s.strip(), sentence[k][1])
		if (re.search(r'\^.*',ph[p]).group()[1:][0] == 'W'):
			sentence = sentence[:k] + (sentence[k+1:] if k+1 < len(sentence) else [])
			k-=1
			break
		# if ("NN" in re.search(r'\^.*',ph[p]).group()[1:]):


		p+=1
	k+=1

print("\n\n\tCHUNKS WITH possession TAG and removing question tags starting with 'W'")
for x in sentence:
	print(x)
	
k=0
while k < len(sentence):
	ph = sentence[k][0].split()
	p=0
	s = ""
	while p < len(ph):
		s = s + re.search(r'.*\^',ph[p]).group()[:-1] + " "
		p+=1
	sentence[k] = (s.strip(), sentence[k][1])
	s = ""
	k+=1

print("\n\n\tCHUNKS WITHOUT POS TAGS")
for x in sentence:
	print(x)

# k=1
# ph = sentence[0][1]
# while k < len(sentence):
# 	if (ph == sentence[k][1]):
# 		s = sentence[k-1][0] + " , " + sentence[k][0]
# 		sentence[k] = (s, sentence[k][1])
# 		sentence = sentence[:k-1] + sentence[k:]
# 	else:
# 		ph = sentence[k][1]
# 	k+=1
# print("\n\n\tCHUNKS WITH merging consecutive phrases")
# for x in sentence:
# 	print(x)

k = 0
nouns = []
triplets = []
while k < len(sentence):
	if (sentence[k][1] == "NP"):
		nouns.append(sentence[k][0])
	if (sentence[k][1] == "VP"):
		r = sentence[k][0]
		if (k == 0): # not possible generally 
			k+=1
			continue
		if (k == len(sentence)-1):
			if (len(nouns) < 2): # John died
				k+=1
				continue
			n1 = nouns[-2]
			n2 = nouns[-1]
			triplets.append( [n1, r, n2] )
			# print("jere"*10)
			k+=1
			continue
		if (len(nouns) > 0):
			# print("\t\there")
			n1 = nouns[-1]
			k+=1
			if (sentence[k][1] == "PP"):
				r = r + " " + sentence[k][0]
				k+=1
			k2 = k
			while (k2 < len(sentence) and sentence[k2][1] == "NP"):
				n2 = sentence[k2][0]
				nouns.append(n2)
				triplets.append([n1, r, n2])
				k2+=1
				if (k2 < len(sentence) and sentence[k2][1] == "PP"):
					k2+=2
			k+=1
			continue


	if (sentence[k][1] == "PP"):
		# print("HERE"*10)
		if (k+1 < len(sentence) and sentence[k+1][1] == "NP"):
			n1 = nouns[-1]
			r = sentence[k][0]
			n2 = sentence[k+1][0]
			# print(nouns, k+1)
			triplets.append([n1, r, n2])
			k+=2
			continue

	if (sentence[k][1] == "CC" and k < len(sentence) and sentence[k+1][1] == "NP"):
		k2 = k 
		verbFound = False
		while (k2 < len(sentence)):
			if (sentence[k2][1] == 'VP'):
				verbFound = True
				break
			k2+=1
		if not (verbFound):
			k+=1
			# print("\n\n")
			# print(sentence[k])
			nouns.append(sentence[k][0])
			k2 = k
			while (k2 >= 0 and sentence[k2][1] != "VP"):
				k2-=1
			if k2 != 0:
				triplets.append([sentence[k2-1][0], sentence[k2][0], nouns[-1]])
	k+=1

# print(triplets)
print("\n\n\tGENERATED TRIPLETS")
# print(triplets)
for x in triplets:
	print(x)

input('ENTER')
	
def preprocess(sent):
	sent = nltk.word_tokenize(sent)
	sent = nltk.pos_tag(sent)
	return sent

#Function to break the triplets with POS/JJ/CD
def getBrokenTriplets(ex):
	#tag each word in the triplet like 
	sent = preprocess(ex)
	# print("NORMAL POS TAGGING")
	# print(sent)
	# print("NER DEFAULT")
	# print(nltk.ne_chunk(sent))


	# tripletsADDON = []
	nn = ()
	ml = []
	nstr = ""
	k=0
	# All the consecutive NN pos tags are merged in this loop
	while k<len(sent):
		if ("NN" in sent[k][1]):
			if (k+1 >= len(sent)) or not (
				("\'s" in sent[k][0] or "’s" in sent[k][0] or sent[k+1][0] == '’' ) #if the noun is containing a possesion like John’s, Mary’s, Teachers’
				and
				(len(sent[k][0]) > 1 ) ): #so that it doesn't filter the names like O’Reily and not John’s
				nstr = nstr + sent[k][0] + " "
			else:
				if ("\'s" in sent[k][0] or "’s" in sent[k][0]):
					sent[k] = (sent[k][0], 'POSS')
				elif (sent[k+1][0] == "\'s" or sent[k+1][0] == "’s"):
					sent[k] = (sent[k][0], 'POSS')
					sent[k+1] = (sent[k+1][0], 'POSS')
				else:
					sent[k] = (sent[k][0], 'POSS')
					sent[k+1] = (sent[k+1][0], 'POSS')
					if (k+2 < len(sent)): #adding if condition just to be on safe side
						sent[k+2] = (sent[k+2][0], 'POSS') # so this doesn't go out of range
						#when the sentence ends with NN's like John’s. Mary’s. Teachers’.
				k-=1

		elif (k!=0 and k!=len(sent)-1 # so that it doesn't raise an error in the coming lines
			and
			(sent[k-1][0][0] >= 'A' and sent[k-1][0][0] <= 'Z' and "NN" in sent[k-1][1]) #if the word before it, is a proper noun
			and
			("and" in sent[k][0] or "of" in sent[k][0]) # if it is a conjuction word in the name of a proper noun, like "Reserve Bank 'of' India"
			and
			(sent[k+1][0][0] >= 'A' and sent[k+1][0][0] <= 'Z' and "NN" in sent[k+1][1]) # if the next word is also a proper noun
			):
			nstr = nstr + sent[k][0] + " "

		else: #something other than NN encountered 
			if (len(nstr)>0): # if there is a NN to write 
				nstr = nstr.strip()
				nn = (nstr,) + ("NN",)
				ml.append(nn) #write the NN
				nstr = "" # clear the string
				ml.append(sent[k]) # add the other-than-NN word
			else:
				ml.append(sent[k]) #just add it
		k+=1
		if (k == len(sent)): #in case the last word was a noun in a sentence
			nstr = nstr.strip()
			nn = (nstr,) + ("NN",)
			ml.append(nn)
			nstr = ""


	print(ml)
	input('enter here')
	# DONE PERFECTLY 

	# print("==========QUALITY==========")
	k=0
	entities = []
	# triplets_NEW = []
	# here we select the adjectives 
	while k<len(ml):
		if ("JJ" in ml[k][1]):
			n1 = ml[k][0]
			# print("N1", n1)
			r = "quality"
			k2 = k
			while k<len(ml): #find the NN coming just next to JJ
				if ("NN" in ml[k][1]):
					# print("YESS")
					break
				k+=1
			if (k<len(ml) and k==k2+1): # if NN found
				n2 = ml[k][0]
				# print("N2", n2)
			elif (len(entities)>0): # if no NN found after JJ and stack is not empty
				n2 = entities[-1][0] # assume that the adjective is associated with last NN in stack
				# print("New case", n2)
				entities = []
			# print("triplet taken is:", ex.split())
			a = ex.split()
			# print(a)
			# print(a[0])
			# print(a[2])
			i = 1
			# print(k, len(ml))
			while(i <(len(ml))):
				# print(i, a[i])
				if (n2 in a[0] or n2 in a[i]):
					# print("YESSS N2", n2)
					qual_triplets = [n1, r, n2]
					if qual_triplets not in tripletsADDON:
						tripletsADDON.append(qual_triplets)
						print("NEW TRIPLETS", tripletsADDON)
					# print("Quality JJ triplets:", (n1), (r), (n2))
					# qual_triplets = [n1, r, n2]
					# print(qual_triplets)
					break
				i+=1

		elif "NN" in ml[k][1]: 
			entities.append(ml[k]) # stack of nouns NN
			# print("NO JJ found")
		k+=1
	#DONE

	# print("==========NUMBER==========")
	k=0
	entities = []
	# here we select the cardinal numbers 
	while k<len(ml):
		if ("CD" in ml[k][1]):
			# print(k)
			n1 = ml[k][0]
			# print(n1)
			r = "number"
			while k<len(ml): #find the NN coming just next to CD
				# print(ml[k][1], k)
				if ("NN" in ml[k][1]):
					break
				k+=1
			
			if (k<len(ml)): # if NN found
				# print("K fin", k)
				n2 = ml[k][0]
				# print(n2)
				# rint("Quality JJ triplets:", (n1), (r), (n2))
				num_triplets = [n1, r, n2]
				# print(num_triplets)
				tripletsADDON.append(num_triplets)
				print("NEW TRIPLETS", tripletsADDON)
				# triplets.append((n1,)+(r,)+(n2,))
			
			elif (len(entities)>0): # if no NN found after CD and stack is not empty
				n2 = entities[-1][0] # assume that the number is associated with last NN in stack
				entities = []
				num_triplets = [n1, r, n2]
				# print(num_triplets)
				tripletsADDON.append(num_triplets)
				

		elif "NN" in ml[k][1]: 
			entities.append(ml[k]) # stack of nouns NN
		k+=1

	# print("==========POCESSION==========")
	k2 = 0
	entities = []
	# here we select the possessions 
	while k2<len(ml):
		if ("POS" in ml[k2][1]):
			# print(k2)
			# print(ml[k2][1])
			
			# if (k+3 >= len(ml)):
			# 	print(ml[k-2],ml[k-1], ml[k], ml[k+1], ml[k+2])
			# 	print(ex, len(ml), k)
			# 	print(sent)
			# 	print(ml)
			# 	input()

			n1 = ml[k2-1][0].replace('\'s','').replace('’s','')
			# print(ml[k2][0])
			# print("N1", n1)
			if ("POS" in ml[k2+1][1]):
				print("YEs1")
				# n1 = n1+ml[k+1][0]
				k+=1
			if ("POS" in ml[k2+1][1]):
				print('YEs2')
				# n1 = n1+ml[k+1][0]
				k+=1
			r = "belongs-to"
			# print(k2+1)
			i = 1
			# print(k2, ml)
			while i<(len(ml)-k2):
				if ("NN" in ml[k2+i][1]):
					n2 = ml[k2+i][0]
					# print("K2", k2)
					# print("N2", n2)
					# print("Quality JJ triplets:", (n1), (r), (n2))
					
					pos_triplets = [n2, r, n1]
					# print(pos_triplets)
					tripletsADDON.append(pos_triplets)
					print("NEW TRIPLETS", tripletsADDON)
					# triplets.append((n2,)+(r,)+(n1,)) #order of n1 and n2 changed intentionally
				i+=1
		k2+=1


print("\n\n\tBREAKING TRIPLETS using POS/JJ/CD")
tripletsADDON = []
for x in triplets:
	for trip in x:
		# print(trip.split())
		if (len(trip.split())>1):
			print("USING:", trip.split())
			# print(trip.split())
			# tripletsADDON = []
			getBrokenTriplets(trip)

print(tripletsADDON)
input('enter')


print("\n\n\tFINAL TRIPLETS")
# triplets.append(tripletsADDON)
triplets = triplets + tripletsADDON
for final in triplets:
	print(final)

# for trip in triplets:
# 	print(trip.split())
	# if (len(trip.split())>1):
	# 	print(trip)
		# print(getTriplets(trip))

# print(len(listchunked)/2, len(pos_tags))

# print('='*200)

# csvFile = open('../../datasets/g055_Coref_Dataset.csv', 'r')
# reader = csv.reader(csvFile)
# next(reader)
# for row in reader:
# 	for x in sent_tokenize(row[1]):
# 		sentence = Sentence(x.strip().strip('.'))
# 		tagger.predict(sentence)
# 		print("Actual sentence\n"+x)
# 		print("Chunked sentence\n"+sentence.to_tagged_string())
# 		input('\nEnter for next line')

# csvFile.close()
# print(listchunked)