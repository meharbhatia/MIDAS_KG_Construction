#sudo pip3 install flair
from flair.models import SequenceTagger
from flair.data import Sentence
import spacy
import en_core_web_sm
import csv
import nltk
import re
from nltk import sent_tokenize


ex = 'The company also showcased it\'s latest Dynasty series of marvellous vehicles, which were recently unveiled at the company\'s spring product launch in Beijing'
ex = 'BYD quickly debuted it\'s E-SEED GT concept car and Song Pro SUV alongside it\'s all-new e-series models at the Shanghai International Automobile Industry Exhibition'
# ex = 'Ritwik Mishra\'s lawyer appealed to Reserve Bank of India to hear the case of Nirav Modi, Mehul Choksy, Rahul Gandhi, Arvind Keriwal and Ramanujam'
# ex = "John Sowa from India exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework"
# ex = "An Indian resident, John Sowa, exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework"
# ex = "A total of 23 new car models were exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework"
# ex = "John Sowa from India exhibited amazing dancing skills and performed Salsa at the event"
# ex = "\"What is your name?\", asked John"
# ex = "That is the place where John died"
# ex = "The Akash eagerly wanted Mehar Sharma's blue coloured jacket, green umbrella of John Sowa and Ritwik Mishra's red jeans"
# ex = "John went to the market by car, and Mary went to the school"
ex = "John was walking near the ocean and bought sea-shells"

tagger = SequenceTagger.load('chunk')

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
		# print("here"*10)
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

	elif (sentence[k][1] == "CC" and k+2 < len(sentence) and sentence[k+1][1] == "VP" and len(triplets) >= 1):
		# n1 = triplets[0][0]

		k2 = k
		while (k2 >= 0 and sentence[k2][1] != "VP"):
			k2-=1

		if k2 != 0:
			n1 = sentence[k2-1][0]
		else:
			n1 = triplets[0][0]

		# print("here")
		k+=1
		r = sentence[k][0]
		if ( k+1 < len(sentence) and sentence[k+1][1] == "PP"):
			r = r + " " + sentence[k][0]
			k+=1
		n2 = sentence[k+1][0]
		nouns.append(n2)
		triplets.append([n1,r,n2])



	k+=1

print("\n\n\tGENERATED TRIPLETS")
for x in triplets:
	print(x)




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

