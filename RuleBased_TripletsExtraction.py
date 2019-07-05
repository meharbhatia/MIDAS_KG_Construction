# -*- coding: utf-8 -*-
import unicodedata
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk import sent_tokenize
import csv

ex = 'BYD debuted its E-SEED GT concept car and Song Pro SUV alongside its all-new e-series models at the Shanghai International Automobile Industry Exhibition.'
# ex = "John was very fast"
# ex = "Running is the favourite hobby of John."
# ex = "John ran away with his sister."
# ex = "John eats Apple, Orange and Coconut."
# ex = "The company also showcased its latest Dynasty series of vehicles, which were recently unveiled at the company’s spring product launch in Beijing."
# ex = "A total of 23 new car models were exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework."
# ex = "John is doing excercise."
# ex = "John is a good boy."
# ex = "Father of John taught him dancing."

def getTriplets(ex):
	# print(ex)

	def preprocess(sent):
		sent = nltk.word_tokenize(sent)
		sent = nltk.pos_tag(sent)
		return sent

	sent = preprocess(ex)
	# print("NORMAL POS TAGGING")
	# print(sent)
	# print("NER DEFAULT")
	# print(nltk.ne_chunk(sent))


	triplets = []
	nn = ()
	ml = []
	nstr = ""
	k=0
	# All the consecutive NN pos tags are merged in this loop
	while k<len(sent):
		if ("NN" in sent[k][1]):
			nstr = nstr + sent[k][0] + " "
		else:
			if (len(nstr)>0):
				nstr = nstr.strip()
				nn = (nstr,) + ("NN",)
				ml.append(nn)
				nstr = ""
				ml.append(sent[k])
			else:
				ml.append(sent[k])
		k+=1

	# print("NER MODIFIED")
	# print(nltk.ne_chunk(ml))

	ignore_verbs = ["is","was","were","will","shall","must","should","would","can","could","may","might"] #verbs which are often modal verbs
	entities = []
	k=0
	# Here, all nouns NN are catched by their verb VB to form a triplet
	while k<len(ml):
		if ("NN" in ml[k][1] or "VBG" in ml[k][1]): # VBG are verbs acting as nouns
			entities.append(ml[k]) # unless you encounter a VB or CC or IN tag, keep a stack of all nouns
		elif ("VB" in ml[k][1]): # verb found
			ismodal = False
			for x in ignore_verbs:
				if (ml[k][0] == x):
					ismodal = True
					break

			k2 = k # remember the verb
			k+=1
			while k < len(ml): #find the noun coming after the verb
				if ("NN" in ml[k][1] or "VBG" in ml[k][1]):
					break
				if (ismodal and "VB" in ml[k][1]):
					k2 = k
					ismodal = False
				k+=1
			if (k < len(ml)): # if there exists a noun after the verb
				if(len(entities) > 0): # if there exists a noun before the verb (in the stack)
					n1 = entities[-1][0]
					# entities = entities[:-1] # remove that noun from the stack
					if (k2+1 < len(ml) and "IN" in ml[k2+1][1]):
						r = ml[k2][0] + " " + ml[k2+1][0]
					else:	
						r = ml[k2][0]
					n2 = ml[k][0]
					triplets.append((n1,)+(r,)+(n2,))
		elif ("CC" in ml[k][1]): #conjuction like AND OR found
			if (len(triplets)>0): # if there already exists a triplet before
				while k < len(ml):
					if ("NN" in ml[k][1] or "VBG" in ml[k][1]): #find the NN coming just after CC
						break
					k+=1
				if (k<len(ml)): # if there exists such a NN
					n1 = triplets[-1][0] # extract node 1 from last triplet
					r = triplets[-1][1] # extract relation from last triplet
					n2 = ml[k][0] # select this NN you just got
					triplets.append((n1,)+(r,)+(n2,))
			elif (len(entities)>0): #list of nouns (@maher not completed yet)
				while (k<len(ml)): 
					if ("NN" in ml[k][1] or "VBG" in ml[k][1]):
						break # final entry in the list found
					k+=1
				# if (k<len(ml)):
		elif ("IN" in ml[k][1]): # a preposition found
			if (len(triplets)>0):
				k2 = k
				while k < len(ml): # find a noun NN after the preposition
					if ("NN" in ml[k][1] or "VBG" in ml[k][1]):
						entities.append(ml[k]) # put the noun in entities stack 
						break
					k+=1
				if (k<len(ml)): #if at least one noun is found
					if(ml[k2][0] == "of" or ml[k2][0] == "alongside"): #these two prepositions are more often associated with object rather than subject (of last triplet)
						n1 = triplets[-1][2] # node 2 of last triplet
						r = ml[k2][0]
						n2 = n2 = ml[k][0]
					else:
						n1 = triplets[0][0] # node 1 of first triplet
						r = triplets[0][1]+" "+ml[k2][0] # relation of first triplet + preposition of this
						n2 = ml[k][0]
					triplets.append((n1,)+(r,)+(n2,))
			elif (len(entities) > 0):
				k2 = k
				while k < len(ml): # find a noun NN after the preposition
					if ("NN" in ml[k][1] or "VBG" in ml[k][1]):
						entities.append(ml[k]) # put the noun in entities stack 
						break
					k+=1
				if (k<len(ml)):
					n1 = entities[-2][0]
					r = ml[k2][0]
					n2 = entities[-1][0]
					triplets.append((n1,)+(r,)+(n2,))
		k+=1
	k=0
	entities = []
	# here we select the adjectives 
	while k<len(ml):
		if ("JJ" in ml[k][1]):
			n1 = ml[k][0]
			r = "quality"
			k2 = k
			while k<len(ml): #find the NN coming just next to JJ
				if ("NN" in ml[k][1]):
					break
				k+=1
			if (k<len(ml) and k==k2+1): # if NN found
				n2 = ml[k][0]
				triplets.append((n1,)+(r,)+(n2,))
			elif (len(entities)>0): # if no NN found after JJ and stack is not empty
				n2 = entities[-1][0] # assume that the adjective is associated with last NN in stack
				entities = []
				triplets.append((n1,)+(r,)+(n2,))

		elif "NN" in ml[k][1]: 
			entities.append(ml[k]) # stack of nouns NN
		k+=1

	k=0
	entities = []
	# here we select the cardinal numbers 
	while k<len(ml):
		if ("CD" in ml[k][1]):
			n1 = ml[k][0]
			r = "number"
			while k<len(ml): #find the NN coming just next to CD
				if ("NN" in ml[k][1]):
					break
				k+=1
			if (k<len(ml)): # if NN found
				n2 = ml[k][0]
				triplets.append((n1,)+(r,)+(n2,))
			elif (len(entities)>0): # if no NN found after CD and stack is not empty
				n2 = entities[-1][0] # assume that the number is associated with last NN in stack
				entities = []
				triplets.append((n1,)+(r,)+(n2,))

		elif "NN" in ml[k][1]: 
			entities.append(ml[k]) # stack of nouns NN
		k+=1
	return triplets





output = [['industry', 'index', 's1', 'r', 's2']]
#change path
with open('/home/ritwik/Downloads/icdm_contest_data.csv', 'r') as csvFile:
    reader = csv.reader(csvFile)
    next(reader) #so that first line is ignored
    k=0
    tlen = 300
    for row in reader:
        article = row[1] #picking article
        triplets = []
        for x in sent_tokenize(article):
        	ml = getTriplets(x) #getting triplets for each sentence
        	triplets+=ml
        #at this point triplets variable contains all the triples from the article
        tl = []
        for x in triplets:
        	ttl = []
        	ttl.append(row[2])
        	ttl.append(row[0])
        	ttl.append(x[0])
        	ttl.append(x[1])
        	ttl.append(x[2])
        	tl.append(ttl)
        output+=tl

        k+=1
        print(str(k)+" / "+str(tlen))
        # if k>2:
        # 	break
        
file = open('tempcsv.csv','w')
for x in output:
	for y in x:
		file.write(y.replace(',','').replace('‘','\'').replace('’','\'').replace('“','\'').replace('”','\'')+', ')
	file.write("\n")
file.close()
csvFile.close()
