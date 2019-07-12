# -*- coding: utf-8 -*-
import unicodedata
import nltk
import re
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk import sent_tokenize
import csv
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

nlp = en_core_web_sm.load()

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

def preprocess(sent):
	sent = nltk.word_tokenize(sent)
	sent = nltk.pos_tag(sent)
	return sent

def getTriplets(ex):
	print(ex)
	ex = ex.replace('‘','\'').replace('’','\'').replace('“','\'').replace('”','\'')

	sent = preprocess(ex)
	print("NORMAL POS TAGGING")
	print(sent)
	print("NER DEFAULT")
	print(nltk.ne_chunk(sent))


	triplets = []
	nn = ()
	ml = []

	## NER is being performed here
	doc = nlp(ex)
	spacyml = [(X, X.ent_iob_, X.ent_type_) for X in doc]
	print(len(sent), len(spacyml))
	newml = []
	pos_tags = [(i, i.tag_) for i in doc]
	sent = pos_tags
	print("Spacy POS tagging")
	print(sent)
	print(spacyml)
	nstr = ""
	k=0
	while k<len(spacyml):
		# print(spacyml[k], end='')
		# print("\t\t", end='')
		# if (k<len(sent)):
		# 	print(sent[k])


		if (spacyml[k][1]=='O' or str(spacyml[k][0]) == "'s"):
			if (len(nstr)>0):
				nn = (nstr.strip(),) + ("NN",)
				newml.append(nn)
				nstr = ""
			newml.append((str(sent[k][0]),) + (str(sent[k][1]),))
		else:
			nstr = nstr + str(sent[k][0]) + " "



		k+=1

	ml = newml
	newml = []
	nstr= ""
	k=0
	while k<len(ml):
		if ( re.search(r'\d', ml[k][0]) ):
			ml[k] = (ml[k][0], "CD")
			if (len(nstr)>0):
				nn = (nstr.strip(),) + ("NN",)
				newml.append(nn)
				nstr = ""
			newml.append(ml[k])
		elif (k+1 < len(ml) and ml[k+1][1] == "POS"):
			ml[k] = (ml[k][0], "POS")
			if (len(nstr)>0):
				nn = (nstr.strip(),) + ("NN",)
				newml.append(nn)
				nstr = ""
			newml.append(ml[k])
		elif ("NN" in ml[k][1]):
			nstr = nstr + ml[k][0] + " "
		else:
			if (len(nstr)>0):
				nn = (nstr.strip(),) + ("NN",)
				newml.append(nn)
				nstr = ""
			newml.append(ml[k])
		k+=1

	ml = newml
	newml = []


	print("NER MODIFIED")
	print(nltk.ne_chunk(ml))
	for y in ml:
		print(y)


	input()

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
			elif (len(entities)>0): # if no NN found after JJ and stack is not empty
				n2 = entities[-1][0] # assume that the adjective is associated with last NN in stack
				entities = []
			for x in triplets:
				if (n2 in x[0] or n2 in x[2]):
					triplets.append((n1,)+(r,)+(n2,))
					break

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

	k=0
	entities = []
	# here we select the possessions 
	while k<len(ml):
		if ("POS" in ml[k][1]):

			# if (k+3 >= len(ml)):
			# 	print(ml[k-2], ml[k-1], ml[k], ml[k+1], ml[k+2])
			# 	print(ex, len(ml), k)
			# 	print(sent)
			# 	print(ml)
			# 	input()

			n1 = ml[k][0].replace('\'s','').replace('’s','')
			if (k+1<len(ml) and "POS" in ml[k+1][1]):
				# n1 = n1+ml[k+1][0]
				k+=1
			if (k+1<len(ml) and "POS" in ml[k+1][1]):
				# n1 = n1+ml[k+1][0]
				k+=1
			r = "belongs-to"

			if (k+1<len(ml) and "NN" in ml[k+1][1]):
				n2 = ml[k+1][0]
				triplets.append((n2,)+(r,)+(n1,)) #order of n1 and n2 changed intentionally
		k+=1

	# to remove isolated nodes
	# k=0
	# while k<len(triplets):
	# 	f = True
	# 	p=0
	# 	while p<len(triplets):
	# 		if(p!=k):
	# 			if (triplets[k][0]==triplets[p][0] or triplets[k][0]==triplets[p][2]
	# 				or
	# 				triplets[k][2]==triplets[p][0] or triplets[k][2]==triplets[p][2]):
	# 				f = False
	# 				break
	# 		p+=1
	# 	if(f):
	# 		triplets = triplets[:k]+triplets[k+1:]
	# 		k-=1
	# 	k+=1

	# to print triplets
	print("Triplets modified")
	for x in triplets:
		print(x)

	return triplets

def clearBrackets(article): # to clear the text written inside brackets 
	k=0
	p1 = p2 = 0
	while k<len(article):
		if (article[k]=='('):
			p1 = k
		if (article[k]==')'):
			p2 = k
		if(p1!=0 and p2!=0):
			article = article[:p1]+article[p2+1:]
			p1 = p2 = 0
		k+=1
	article = article.replace('(','').replace('(','')
	return article
	



output = [['industry', 'index', 's1', 'r', 's2']]
#change path
with open('NEW_New_Coref_Dataset.csv', 'r') as csvFile:
	reader = csv.reader(csvFile)
	next(reader) #so that first line is ignored
	k=0
	tlen = 300
	for row in reader:
		# print(row[1])
		# input()
		# continue
		article = row[1]
		article = "John Sowa Mayar\'s lawyer appealed to International Museum of Trade and Commerce to hear the case of Nirav Modi, Mehul Choksy and Ramanujam. Enlarge ImageBetween this and the Venue, \"Hyundai Motor Group\" is on a visual roll right now. What's the best way to market a car to millennials? By making one that's small enough for them to actually afford, duh. Kia on Tuesday unveiled the first sketches of its upcoming small SUV. We won't see the full thing until the summer, but for now, the sketches give us an idea of what Kia will bring to market in an effort to woo urbanite millennials into car ownership. The car will allegedly be a global SUV, meaning it's destined for a whole bunch of markets, but considering Autocar's report claims it won't be coming to Europe, it's uncertain if the US is involved in this rollout. It's also unclear if Kia actually understands what \"global\" means. From the design side, Kia apparently took a boatload of inspiration from its SP Signature Concept, which debuted at the Seoul Motor Show in March."
		article = clearBrackets(article)
		triplets = []
		for x in sent_tokenize(article):
			ml = getTriplets(x) #getting triplets for each sentence
			triplets+=ml
			input() #to pause execution


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
		if k>2: #just to see output from top 2 articles
			break

### to write into a file
# file = open('new_5.csv','w')
# for x in output:
# 	for y in x:
# 		file.write(y.replace(',','').replace('‘','\'').replace('’','\'').replace('“','\'').replace('”','\'')+', ')
# 	file.write("\n")
# file.close()
csvFile.close()