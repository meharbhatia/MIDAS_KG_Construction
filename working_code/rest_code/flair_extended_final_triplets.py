from dt_triplets_Using_Flair import getTriplets

from flair.models import SequenceTagger
from flair.data import Sentence
import spacy
import en_core_web_sm
import csv
import nltk
import re 
from nltk import sent_tokenize

def getTagged(ex, show, main_triplet):
	sentence = Sentence(ex)

	tagger.predict(sentence)
	strchunked = sentence.to_tagged_string()
	# if(show):
	# 	# print("\n")
	# 	print(sentence)
	# 	print("\nChunked sentence")
		# print(strchunked)

	nlp = en_core_web_sm.load()
	doc = nlp(ex)
	# pos_tags = [(i, i.tag_) for i in doc]
	pos_tags = nltk.pos_tag(nltk.word_tokenize(ex))
	

	listchunked = strchunked.split()
	# print(len(listchunked))
	# print(len(pos_tags))
	ph = ""
	sentence = []

	k = 0
	while k+1 < len(listchunked):
		if listchunked[k+1] == '<S-NP>' or listchunked[k+1] == '<S-VP>' or listchunked[k+1] == '<S-PP>':
			ph = listchunked[k]
			sentence.append([(ph), (listchunked[k+1][-3:-1])])
			ph = ""
			k+=2
			# print("S")
		elif listchunked[k+1] == '<B-NP>':
			# ph = ph + listchunked[k]
			while (k+1<len(listchunked) and listchunked[k+1] != '<E-NP>'):
				if not (listchunked[k][0]== '<' and listchunked[k][-1] == '>'):
					ph = ph.strip() + " " + listchunked[k]
				k+=1
			ph = ph.strip() + " " + listchunked[k]
			sentence.append([ph, 'NP'])
			ph = ""
			k+=2
			# print("BNP")
		elif listchunked[k+1] == '<B-VP>':
			while (k+1<len(listchunked) and listchunked[k+1] != '<E-VP>'):
				if not (listchunked[k][0]== '<' and listchunked[k][-1] == '>'):
					ph = ph.strip() + " " + listchunked[k]
				k+=1
			ph = ph.strip() + " " + listchunked[k]
			sentence.append([ph, 'VP'])
			ph = ""
			k+=2
			# print(BVP)
		elif not ( listchunked[k+1][0] == '<' and listchunked[k+1][-1] == '>' ): #happens with 'CC'
			sentence.append([ listchunked[k] , 'CC'])
			k+=1
		else:
			k+=2
			# print("here")

	# if(show):
	# 	# print("\n\n")
	# 	# print("CHUNKS from spacy")
	# 	for x in sentence:
	# 		print(x)

	
	tf = False
	k=m=0
	sentence2 = []
	while k < len(sentence):
		ph = ""
		for x in nltk.word_tokenize(sentence[k][0]):
			m2 = m #old value of m
			while m < len(pos_tags): #find the pos tag of x
				if (x.strip('.') == pos_tags[m][0].strip('.')): #found the pos tag of x
					if(pos_tags[m][1]=="RB" or pos_tags[m][1]=="DT" or pos_tags[m][1]=="." or pos_tags[m][1]=="``"):
						break
					if (pos_tags[m][1]==","):
						if (len(ph) > 0):
							sentence2.append([ ph.strip() , sentence[k][1] ])
							ph = ""
					else:
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

	# if(show):
		# print("\n\n")
		# print("CHUNKS with POS tags")
		
	sentence = sentence2

	k = 0
	while k < len(sentence):
		ph = sentence[k][0].split()
		p = 0
		vbfound = False
		s = ""
		while p < len(ph):
			try:
				fflag = ((re.search(r'.*\^',ph[p]).group()[:-1] == "'s" or re.search(r'.*\^',ph[p]).group()[:-1] == "'") and len(re.search(r'.*\^',ph[p]).group()[:-1]) <= 2)
			except:
				# print(sentence)
				input('ERROR')
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
		print("\n\n\tINTIAL CHUNK AND POS SENTENCE")
		for x in sentence:
			print(x)

	sentence_pos = sentence
	# print("SP", sentence_pos)
	# tripletsADDON = []
	for x in sentence_pos:
		# print(x, len(x), x[0], len(x[0].split()))
		if (len(x[0].split()) > 1 ):
			# print("Use this", x[0])
			a = x[0].split()
			list_fin = []
			sen = " "
			for aa in a:
				list_aa = []
				# print("AAA", aa)
				aaaa = aa.split('^')[0] #word
				sen = sen + " " + aaaa
				# print("SEN", sen)
				bbbb = aa.split('^')[1] #pos tag
				list_aa.append(aaaa)
				list_aa.append(bbbb)
			# print("LIST_AA", list_aa)
				tuple_aa = tuple(list_aa)
				# print("TUUU", tuple_aa)
				list_fin.append(tuple_aa)
			sen = sen.lstrip()
			print("SEN", sen)
			# trip = [['He', 'bought', 'four new cars']]
			triplet_sentence = []
			for tr in main_triplet:
				for t in tr:
					if sen == t:
						break
					else:
						triplet_sentence.append(t)
			print(triplet_sentence)

			# print("\n")
			print("INPUT REQUIRED:", list_fin)
			# getBrokenTriplets(list_fin, sen)

	# print(tripletsADDON)
	return list_fin, sen

def getQuality(ml, ex, main_triplet):
	tripletsADDON = []
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
			return 0, main_triplet
			# print("NO JJ found")
		k+=1
	#DONE

	#NOW DELETE n1(JJ) from main_triplets
	# main_triplet =  [['He', 'bought', 'four new cars']]
	main_triplet_qual = []
	for m_triplet in main_triplet:
		# print(m_triplet)
		for mt in m_triplet:
			if n1 in mt:
				mt = mt.replace(n1, '')
				# print(mt)
				main_triplet_qual.append(mt)
			else:
				main_triplet_qual.append(mt)
	# print(main_triplet_qual)
	main_triplet_new = []
	main_triplet_new.append(main_triplet_qual)
	print(main_triplet_new)		

	return tripletsADDON, main_triplet_new


def getNumber(ml, ex, main_triplet):
	
	# print("==========NUMBER==========")
	tripletsADDON = []
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
			return 0
		k+=1

	main_triplet_new = []
	for m_triplet in main_triplet:
		# print(m_triplet)
		for mt in m_triplet:
			if n1 in mt:
				mt = mt.replace(n1, '')
				# print(mt)
				main_triplet_new.append(mt)
			else:
				main_triplet_new.append(mt)
	print(main_triplet_new)



	return tripletsADDON, main_triplet_new

def preprocess(sent):
	sent = nltk.word_tokenize(sent)
	sent = nltk.pos_tag(sent)
	return sent


def getBelongs(ex):
	sent = preprocess(ex)
	# print("NORMAL POS TAGGING")
	# print(sent)
	# print("NER DEFAULT")
	# print(nltk.ne_chunk(sent))


	tripletsADDON_POS = []
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


	# print("ML", ml)
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
					print("N2", n2)
					# print("Quality JJ triplets:", (n1), (r), (n2))
					
					pos_triplets = [n2, r, n1]
					# print(pos_triplets)
					tripletsADDON_POS.append(pos_triplets)
					print("NEW TRIPLETS", tripletsADDON_POS)
					# triplets.append((n2,)+(r,)+(n1,)) #order of n1 and n2 changed intentionally
				i+=1
		k2+=1

	# print(tripletsADDON)
	return tripletsADDON_POS



tagger = SequenceTagger.load('chunk')

# ex  = "John has amazing dancing skills"
ex = "Akash Kumar's friend bought four new cars."

triplet = getTriplets(ex, False)
#Finally generated our main triplets

#Need to extend upon this

#First bring the triplet to be broken down in this format '<pos tagged string>, NP'
print("MAIN triplet: ", triplet)
mylist, sent = getTagged(ex, True, triplet)

# output:   [('four', 'CD'), ('new', 'JJ'), ('cars', 'NNS')]

#Now look at JJ

triplet_quality_addon, triplet_removeQuality = getQuality(mylist, sent, triplet)
# print(triplet_removeQuality)

# NEW TRIPLETS [['new', 'quality', 'cars']]
# ['He', 'bought', 'four  cars']

triplet_number_addon, triplet_removeNumber = getNumber(mylist, sent, triplet_removeQuality)
# getNumber(mylist, sent, triplet_removeQuality)

for x in triplet:
	for trip in x:
		# print(trip.split())
		if (len(trip.split())>1):
			triplet_belongs_addon = getBelongs(trip)
			print(triplet_belongs_addon)

print("\n\n\t FINAL TRIPLETS")
print(triplet_removeNumber)
print(triplet_quality_addon)
print(triplet_number_addon)
print(triplet_belongs_addon)

# getBelongs(ex)
