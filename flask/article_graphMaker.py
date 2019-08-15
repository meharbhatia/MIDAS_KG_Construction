from triplets_using_flair import clearBrackets
from reduce_triplets import *
from jjposcd_extractor import extractor
from flairChunking import getPhrases
from flair.models import SequenceTagger
from flair.data import Sentence
from nltk import sent_tokenize
from graphviz import *
from datetime import datetime
import spacy
import nltk
import re
import pandas as pd
import en_core_web_sm




def getTriplets(ex, Ngrams, show, nlp, tagger):
	ex = ex.strip('.').strip('!').replace('‘','\'').replace('’','\'').replace('“','"').replace('”','"')
	# ex = clearBrackets(ex)
	sentence = Sentence(ex)
	triplets = []


	tagger.predict(sentence)
	strchunked = sentence.to_tagged_string()
	if(show):
		print("\n")
		print(sentence)
		print("\nChunked sentence")
		print(strchunked)
	sentence = getPhrases(ex, tagger)


	
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
					ph = ph.strip() + " " +x+"^"+pos_tags[m][1]
					m+=1
					break
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
			if (re.search(r'\^.*',ph[p]).group()[1:][0] == 'W'):
				ph = ph[:p] + (ph[p+1:] if p+1 < len(ph) else [])
			p+=1
		if (len(ph)==0):
			sentence = sentence[:k] + (sentence[k+1:] if k+1 < len(sentence) else [])
		else:
			sentence[k][0] = ' '.join(ph)
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

				if(k<len(sentence) and (sentence[k][1]=="NP" or sentence[k][0] == "era")):
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

				if (sentence[k][0] == "of" or sentence[k][0]=="on" or "than" in sentence[k][0]):
					r = sentence[k][0]
					n1 = sentence[k-1][0]
				else:
					k2 = k
					# print(k2)
					while k2>=0:
						if(sentence[k2][1]=="VP"):
							break
						k2-=1
					if(k2<=0):
						r = sentence[k][0]
						n1 = sentence[k-1][0]
					else:
						# print(k2)
						r = sentence[k2][0]+" "+sentence[k][0]
						n1 = sentence[k2-1][0]
						for x in list(reversed(triplets)):
							if (x[1] == sentence[k2][0]):
								n1 = x[0]
								break
				n2 = sentence[k+1][0]
				# print(nouns, k+1)
				triplets.append([n1, r, n2])
				k+=2
				continue

			elif (k == 0 and len(sentence) > 1 and sentence[k+1][1] == "NP"):
				prepInStart = True
				k+=2
				continue


		if (sentence[k][1] == "CC" and k+1 < len(sentence) and sentence[k+1][1] == "NP" and sentence[k][0]!="era"):
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

		elif (sentence[k][1] == "CC" and k+2 < len(sentence) and sentence[k+1][1] == "VP" and len(triplets) >= 1 and sentence[k][0]!="era"):
			# n1 = triplets[0][0]

			k2 = k
			while (k2 >= 1 and not(sentence[k2][1] == "VP" and sentence[k2-1][1] == "NP")):
				k2-=1

			if k2 != 0:
				n1 = sentence[k2-1][0]
				for x in list(reversed(triplets)):
					if (sentence[k2][0] in x[1]):
						n1 = x[0]					#x[0] good for "us; to experience; EQC" --> "x[0]; to normalize; EQC"
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
		elif (sentence[k][1] == "CC" and k+1 < len(sentence) and sentence[k+1][1] == "PP" and sentence[k][0]!="era"):
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
		elif (triplets[k][1]=="number"):
			yearflag = False
			for x in getNERs(ex, nlp):
				if(triplets[k][0] == x[0] and x[1] == "DATE"):
					yearflag = True
					break 
			if(yearflag):
				triplets[k][1] = "year"
		k+=1


	if(show):
		print("\n\n\tGENERATED TRIPLETS")
		for x in triplets:
			print(x)

	return triplets

def articleToGraph(article, tagger):
	
	# article = "Norway has a lot of electric cars, so many that it can make anyone driving a new vehicle with an internal combustion engine look like a Luddite. Mercedes-Benz brought us there to experience the EQC, and possibly to normalize it in a sea of EVs that makes California look like a land of late adopters. Outside Oslo, where cars were larger and more upscale than in other parts of Europe, and Tesla vehicles (S and X) are a more common sight than around Los Angeles or the Bay Area, the EQC fit right in. DON'T MISS: Mercedes-Benz EQC Edition 1886 electric SUV kicks off a new era. After a couple of rain-soaked days driving the EQC there last week, we can say that it will be a great addition in the U.S. when it arrives sometime in 2020. At about 187 inches long, the EQC400 4Matic crossover splices into the American mid-sizers."
	triplets = []
	show = False
	article = clearBrackets(article)
	article = article.strip('\n').strip('.').strip()
	sents = sent_tokenize(article)
	Ngrams = getNgrams(article)
	nlp = en_core_web_sm.load()

	s = 0
	while s < len(sents):
		ml = getTriplets(sents[s], Ngrams, show, nlp, tagger) #getting triplets for each sentence
		triplets+=ml
		if(show):
			input("\n\t\t\tPress ENTER to see next sentence...") #to pause execution
		s+=1
		print(str(s)+" / "+str(len(sents)))



	sdata = pd.DataFrame(triplets)
	sdata.columns = ["s1", "r", "s2"]

	if(show):
		for x in triplets:
			print(x)
		print(sdata)

	nset = list(set(sdata["s1"]).union(set(sdata["s2"])))
	dot = Graph()

	for x in nset:
		dot.node(re.sub(r'\W+', ' ', x), x)
	i = 0
	while i < len(sdata):
		dot.edge(re.sub(r'\W+', ' ', sdata.iloc[i]["s1"]), re.sub(r'\W+', ' ', sdata.iloc[i]["s2"]), label=sdata.iloc[i]["r"])
		i+=1
	dtstring = str((datetime.now()- datetime(1970, 1, 1)).seconds)
	# pathstr = "static/images/"+dtstring
	pathstr = "static/images/graph"

	article = '\n\n== ARTICLE ==\n'+'\n'.join(sents)

	dot.attr(label=article)
	dot.attr(fontsize='25')

	dot.render(pathstr, format='png')
	return pathstr
