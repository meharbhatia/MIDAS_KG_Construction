#sudo pip3 install flair
from jjposcd_extractor import extractor
from spacyNER import getNERs
from flairChunking import getPhrasesfromfile
from flair.models import SequenceTagger
from flair.data import Sentence
from flairChunking import getPhrases
from reduce_triplets import *
import spacy
import en_core_web_sm
import csv
import nltk
import re
from nltk import sent_tokenize



# ex = 'The company also showcased it\'s latest Dynasty series of marvellous vehicles, which were recently unveiled at the company\'s spring product launch in Beijing'
# ex = 'BYD quickly debuted it\'s E-SEED GT concept car and Song Pro SUV alongside it\'s all-new e-series models at the Shanghai International Automobile Industry Exhibition'
# ex = 'Ritwik Mishra\'s lawyer appealed to International Association of Trade and Commerce to hear the case of Nirav Modi, Mehul Choksy, Rahul Gandhi, Arvind Keriwal and Ramanujam'
# ex = "John Sowa from India exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework"
# ex = "An Indian resident, John Sowa exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework"
ex = "Ford says shifter cables can snap off and render the gear selector broken or useless on 2013–2016 Ford Fusion sedans."
ex = "\"The SUV has really expanded from a consumer standpoint,\" said Jeff Schuster, president of global forecasting at LMC. \"That's where the volume is; that's where the future is"
ex = "Celebrity chef Jamie Oliver's British restaurant chain has become insolvent, putting 1,300 jobs at risk"
ex = "Oliver began his restaurant empire in 2013–2014 when he opened Fifteen in London"
# ex = "A resident on Palomino Court, off Soledad Mountain Road, called 9-1-1 about 9:45 a.m. to report the house next door on fire, with black smoke coming out of the roof, police said"
# ex = "DON'T MISS: Mercedes-Benz EQC Edition 1886 electric SUV kicks off a new era"
# ex = "Norway has a lot of electric cars, so many that it can make anyone driving a new vehicle with an internal combustion engine look like a Luddite"
# ex = "A total of 23 new car models were exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture design, the 3rd generation of Dual Mode technology, plus the e-platform framework"
# ex = "John Sowa from India exhibited amazing dancing skills and performed Salsa at the event"
# ex = "\"What is your name?\", asked John"
# ex = "That is the place where John died"
# ex = "In 2019, Akash eagerly wanted Mehar Sharma's blue coloured jacket, broken umbrella of John Sowa and Ritwik Mishra's big black red jeans"
# ex = "Outside Oslo, where cars were larger and more upscale than in other parts of Europe, and Tesla vehicles are a more common sight than around Los Angeles or the Bay Area, the EQC fit right in."
# ex = "John went to the market by car, and Mary went to the school"
# ex = "John was walking near the vast ocean and bought sea-shells"
# ex = "In New York, the buildings were tall and beautiful"

def clearBrackets(article): # to clear the text written inside brackets 
	k=0
	p1 = 0
	p2 = 0
	while k<len(article) and '(' in article:
		if (article[k]=='('):
			p1 = k
		if (article[k]==')'):
			p2 = k
		if(p1!=0 and p2!=0):
			article = article[:p1]+article[p2+1:].strip()
			p1 = 0
			p2 = 0
			k=0
		k+=1
	article = article.replace('(','').replace('(','')
	return article


def getTriplets(iname, aindex, sindex, ex, Ngrams, show, nlp):
	# ex = "RX also gets a brake-based torque vectoring system the subtly applies the brakes on the inner wheels for better handling and stability through turns. F Sport models get an updated Active Variable Suspension system that's said to be more responsive than before"
	# ex = "The Akash eagerly wanted Mehar Sharma's blue coloured jacket, green umbrella of John Sowa, and Ritwik Mishra's big black red jeans"
	# ex = "John had good dancing skills"
	ex = ex.strip('.').strip('!').replace('‘','\'').replace('’','\'').replace('“','"').replace('”','"')
	# ex = clearBrackets(ex)
	sentence = Sentence(ex)
	triplets = []

	if(iname == '0'):
		tagger = SequenceTagger.load('chunk')
		tagger.predict(sentence)
		strchunked = sentence.to_tagged_string()
		if(show):
			print("\n")
			print(sentence)
			print("\nChunked sentence")
			print(strchunked)
		sentence = getPhrases(ex, tagger)
	else:
		sentence = getPhrasesfromfile(iname, aindex, sindex)

	
	doc = nlp(ex)
	# pos_tags = [(i, i.tag_) for i in doc]
	pos_tags = nltk.pos_tag(nltk.word_tokenize(ex))
	if(show):
		print(ex)
		print("\nPOS tags")
		print(pos_tags)


	if(show):
		print("\n\n")
		print("CHUNKS from Flair")
		for x in sentence:
			print(x)

	if(show):
		print("\n\n")
		print("NER from Spacy")
		for x in getNERs(ex, nlp):
			print(x)

	
	tf = False
	k=m=0
	sentence2 = []
	while k < len(sentence):
		ph = ""
		for x in nltk.word_tokenize(sentence[k][0]):
			m2 = m #old value of m
			while m < len(pos_tags): #find the pos tag of x
				if (x.strip('.') == pos_tags[m][0].strip('.')): #found the pos tag of x
					if(pos_tags[m][1]=="RB" or pos_tags[m][1]=="." or pos_tags[m][1]=="``"):
						break
					if (pos_tags[m][1]=="DT" and sentence[k][0].find(x) == 0):
						break
					# if (pos_tags[m][1]==","):
					# 	if (len(ph) > 0):
					# 		sentence2.append([ ph.strip() , sentence[k][1] ])
					# 		ph = ""
					# else:
					# 	ph = ph.strip() + " " +x+"^"+pos_tags[m][1]
					ph = ph.strip() + " " +x+"^"+pos_tags[m][1]
					m+=1
					break
				# elif (x == "have"):
				# 	print(pos_tags[m], m)
				m+=1
			if (m == len(pos_tags) and m2 != len(pos_tags)):
				m = m2
		if (len(ph) > 0):
			sentence2.append([ ph.strip() , sentence[k][1] ])
		elif (sentence[k][0][-1] != ',' and ' ' not in sentence[k][0]):
			sentence2.append( [sentence[k][0]+"^NN", sentence[k][1]])
		k+=1

	if(show):
		print("\n\n")
		print("CHUNKS with POS tags")
		for x in sentence2:
			print(x)


	sentence = sentence2

	k=0
	while k<len(sentence):
		temptriplets = extractor(sentence[k])
		if (len(temptriplets[0][0]) == 0 and sentence[k-1][1] != "VP"):
			sentence[k] = temptriplets[0]
			sentence = sentence[:k] + (sentence[k+1:] if k+1 < len(sentence) else [])
			k-=1
		elif (len(temptriplets[0][0]) != 0):
			sentence[k] = temptriplets[0]
		triplets = triplets + temptriplets[1:]
		k+=1

	if(show):
		print("\n\n")
		print("CHUNKS with removed POS-CD")
		for x in sentence:
			print(x)

	k = 0
	while k < len(sentence):
		ph = sentence[k][0].split()
		p = 0
		vbfound = False
		s = ""
		while p < len(ph):
			# try:
			# 	fflag = ((re.search(r'.*\^',ph[p]).group()[:-1] == "'s" or re.search(r'.*\^',ph[p]).group()[:-1] == "'") and len(re.search(r'.*\^',ph[p]).group()[:-1]) <= 2)
			# except:
			# 	print(sentence)
			# 	input('ERROR')
			# if ( (re.search(r'.*\^',ph[p]).group()[:-1] == "'s" or re.search(r'.*\^',ph[p]).group()[:-1] == "'") and len(re.search(r'.*\^',ph[p]).group()[:-1]) <= 2 ):
			# 	if (p-2 >= 0):
			# 		s = ' '.join(ph[:p-1])
			# 	s = s + " " + re.search(r'.*\^',ph[p-1]).group()[:-1] + "'s^POS " + ' '.join(ph[p+1:])
			# 	# print(s)
			# 	# input('ENTER')
			# 	sentence[k] = (s.strip(), sentence[k][1])
			# 	ph = sentence[k][0].split()
			# 	p-=1
			# 	s = ""
			# if ("VB" in re.search(r'\^.*',ph[p]).group()[1:]):
			# 	if not(vbfound):
			# 		vbfound = True
			# 	else:
			# 		s = ' '.join(ph[p:])
			# 		sentence[k] = (s.strip(), sentence[k][1])
			if (re.search(r'\^.*',ph[p]).group()[1:][0] == 'W'):
				sentence = sentence[:k] + (sentence[k+1:] if k+1 < len(sentence) else [])
				k-=1
				break
			# if ("NN" in re.search(r'\^.*',ph[p]).group()[1:]):


			p+=1
		k+=1
	if(show):
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

	if(show):
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
	prepInStart = False
	nounAtLast = (True if (len(sentence)>0 and sentence[-1][1] == "NP") else False)
	########################### Rules for TRIPLETS FORMATION ###########################
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

				if(k<len(sentence) and sentence[k][1]=="NP"):
					n2 = sentence[k][0]
					nouns.append(n2)
				elif (nounAtLast==False and prepInStart==True):
					r = r + " " + sentence[0][0].lower()
					n2 = sentence[1][0]
					prepInStart = False
				else:
					n2 = "<UNKNOWN>"
				triplets.append([n1, r, n2])

				k+=1
				continue


		if (sentence[k][1] == "PP"):
			# print("HERE"*10)
			if (k+1 < len(sentence) and (sentence[k+1][1] == "NP") and len(nouns) > 0):
				
				r = sentence[k][0]

				n1 = nouns[-1]					#this
				if(sentence[k][0] == "of"):		#and this
					n1 = sentence[k-1][0]		#i think both are same <nervous_smiley_emoji>
				
				n2 = sentence[k+1][0]
				# print(nouns, k+1)
				triplets.append([n1, r, n2])
				k+=2
				continue
			elif (k == 0 and len(sentence) > 1 and sentence[k+1][1] == "NP"):
				prepInStart = True
				k+=2
				continue


		if (sentence[k][1] == "CC" and k+1 < len(sentence) and sentence[k+1][1] == "NP"):
			k2 = k+1 
			verbFound = False
			ppfound = False
			while (k2 < len(sentence) and sentence[k2][1]!="CC"):
				if (sentence[k2][1] == 'VP'):
					verbFound = True
					break
				elif (sentence[k2][1] == "PP"):
					ppfound = True
					break #zarurat nhi hai break ki, fir bhi for the sake of symmetry :) 
				k2+=1
			
			k2 = 0
			while k2<len(triplets):
				if(triplets[k2][0] == sentence[k+1][0] and triplets[k2][1] == "belongs-to"):
					ppfound = True
				k2+=1
			if sentence[k-1][1] == "CC":
				ppfound = True
			if not (verbFound):
				k+=1
				# print("\n\n")
				# print(sentence[k])
				nouns.append(sentence[k][0])
				n2 = sentence[k][0]
				k2 = k
				while (k2 >= 0 and (sentence[k2][1] not in (["VP"] if ppfound else ["VP","PP"]) )):
					k2-=1
				if k2 != 0:
					if (sentence[k2-1][1] == "VP"):
						k2-=1
					r = sentence[k2][0]
					if (k2+1 < len(sentence) and sentence[k2+1][1] == "PP"):
						r = r + " " + sentence[k2+1][0]

					while (k2 >= 1 and not(sentence[k2-1][1] == "NP")): #no need of loop waise to, just right before there will be the NP
						k2-=1
					n1 = sentence[k2-1][0]

					for x in list(reversed(triplets)):
						if (r in x[1]):
							n1 = x[0]
							break

					triplets.append([n1, r, n2])

		elif (sentence[k][1] == "CC" and k+2 < len(sentence) and sentence[k+1][1] == "VP" and len(triplets) >= 1):
			# n1 = triplets[0][0]

			k2 = k
			while (k2 >= 1 and not(sentence[k2][1] == "VP" and sentence[k2-1][1] == "NP")):
				k2-=1

			if k2 != 0:
				n1 = sentence[k2-1][0]
				for x in list(reversed(triplets)):
					if (sentence[k2][0] in x[1]):
						n1 = x[2]
						break
				
			elif (len(nouns)>0):
				n1 = nouns[-1]

			else:
				break

			# print("here")
			k+=1
			r = sentence[k][0]
			if ( k+1 < len(sentence)-1 and sentence[k+1][1] == "PP"):
				r = r + " " + sentence[k+1][0]
				k+=1
			if(sentence[k+1][1]=="NP"):
				n2 = sentence[k+1][0]
			else:
				continue
			nouns.append(n2)
			triplets.append([n1,r,n2])
			k+=1
		elif (sentence[k][1] == "CC" and k+1 < len(sentence) and sentence[k+1][1] == "PP"):
			k+=1
			if(k+1<len(sentence) and sentence[k+1][1]=="NP"):
				k+=1
		k+=1

	if (prepInStart):
		k = len(sentence)-1
		while k >=0:
			if (k-1 >=0 and sentence[k][1] == "VP" and sentence[k-1][1] == "NP" and sentence[k-1][0] in nouns):
				break
			k-=1
		if(k-1 >=0 and sentence[k][1] == "VP" and sentence[k-1][1] == "NP"):
			n1 = sentence[k-1][0]
			r = sentence[0][0]
			n2 = sentence[1][0]
			triplets.append([n1, r, n2])

	k=0
	while k <len(triplets):
		if( len(triplets[k][0])<2 or len(triplets[k][2])<2 or triplets[k][2] == "<UNKNOWN>" or triplets[k][0] == "<UNKNOWN>"):
			triplets = triplets[:k] + (triplets[k+1:] if k+1<len(triplets) else [])
		k+=1


	### to remove isolated nodes
	# k=0
	# while k<len(triplets):
	# 	f = True
	# 	p=0
	# 	while p<len(triplets):
	# 		if(p!=k):
	# 			if ((len(triplets[k][0]) > 1 and len(triplets[k][2]) > 1) and (triplets[k][0]==triplets[p][0] or triplets[k][0]==triplets[p][2]
	# 				or
	# 				triplets[k][2]==triplets[p][0] or triplets[k][2]==triplets[p][2])):
	# 				f = False
	# 				break
	# 		p+=1
	# 	if(f):
	# 		triplets = triplets[:k]+triplets[k+1:]
	# 		k-=1
	# 	k+=1

	if(show):
		print("\n\n\tGENERATED TRIPLETS")
		for x in triplets:
			print(x)

	return triplets

if __name__ == "__main__":
	# tagger = SequenceTagger.load('chunk')
	nlp = en_core_web_sm.load()
	Ngrams = getNgrams(ex)
	print(Ngrams)
	getTriplets('0',22,2,ex, Ngrams ,True, nlp)