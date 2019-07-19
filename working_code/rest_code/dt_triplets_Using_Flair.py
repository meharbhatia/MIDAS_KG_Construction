#sudo pip3 install flair
from flair.models import SequenceTagger
from flair.data import Sentence
import spacy
import en_core_web_sm
import csv
import nltk
import re
import time
from statistics import mean 
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

tagger = SequenceTagger.load('chunk')

def getTriplets(ex, show):
	# ex = "RX also gets a brake-based torque vectoring system the subtly applies the brakes on the inner wheels for better handling and stability through turns. F Sport models get an updated Active Variable Suspension system that's said to be more responsive than before"
	ex = ex.strip('.').strip('!').replace('‘','\'').replace('’','\'').replace('“','"').replace('”','"')
	sentence = Sentence(ex)

	tagger.predict(sentence)
	strchunked = sentence.to_tagged_string()
	if(show):
		print("\n")
		print(sentence)
		print("\nChunked sentence")
		print(strchunked)

	nlp = en_core_web_sm.load()
	doc = nlp(ex)
	# pos_tags = [(i, i.tag_) for i in doc]
	pos_tags = nltk.pos_tag(nltk.word_tokenize(ex))
	if(show):
		print("\nPOS tags")
		print(pos_tags)


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

	if(show):
		print("\n\n")
		print("CHUNKS from spacy")
		for x in sentence:
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

	if(show):
		print("\n\n")
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
			try:
				fflag = ((re.search(r'.*\^',ph[p]).group()[:-1] == "'s" or re.search(r'.*\^',ph[p]).group()[:-1] == "'") and len(re.search(r'.*\^',ph[p]).group()[:-1]) <= 2)
			except:
				print(sentence)
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
			if (k+1 < len(sentence) and sentence[k+1][1] == "NP" and len(nouns) > 1):
				n1 = nouns[-1]
				r = sentence[k][0]
				n2 = sentence[k+1][0]
				# print(nouns, k+1)
				triplets.append([n1, r, n2])
				k+=2
				continue

		if (sentence[k][1] == "CC" and k+1 < len(sentence) and sentence[k+1][1] == "NP"):
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
					r = sentence[k2][0]
					if (k2+1 < len(sentence) and sentence[k2+1][1] == "PP"):
						r = r + " " + sentence[k2+1][0]
					triplets.append([sentence[k2-1][0], r, nouns[-1]])

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
	if(show):
		print("\n\n\tGENERATED TRIPLETS")
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
			article = article[:p1]+article[p2+1:].strip()
			p1 = p2 = 0
		k+=1
	article = article.replace('(','').replace('(','')
	return article


output = [['industry', 'index', 's1', 'r', 's2']]
show = False
tvar = time.time()
tlist = []
#change path
with open('../../datasets/g050_Coref_Dataset.csv', 'r') as csvFile:
	reader = csv.reader(csvFile)
	next(reader) #so that first line is ignored
	k=0
	tlen = 300
	for row in reader:
		article = row[1]

		#YOU CAN PUT AN ARTICLE HERE. It'll replace the article you fetched from dataset

		# article = "May 15, 2019, 4:11am ETby Ronan GlonThe Coupe line-up gains a mid-range model. Porsche has expanded the Cayenne Coupe line-up with a mid-range model called S. Porsche slots between the entry-level Cayenne Coupe and the range-topping Cayenne Coupe Turbo in the growing model hierarchy. ETby Ronan GlonThe Coupe is mechanically identical to the Cayenne S that's already part of the Porsche family. That means power comes from a twin-turbocharged, 2.9-liter V6 engine tuned to develop 434 horsepower from 5,700 to 6,600 rpm and 405 pound-feet of torque over a broad range that stretches from 1,800 to 5,500 rpm. The six spins the four wheels through an eight-speed automatic transmission. Porsche pegs the mid-range model's zero-to-60-mph time at 4.7 seconds with the standard Sport Chrono package, and Porsche top speed at 164 mph."
		# article = "Since then, Nissan says more than 20% of buyers in the U.S. have opted for the $1,350 package. (Photo: Nissan)All-wheel drive sedans used to be a niche market limited to park rangers and uptight snow-belt drivers. These days, These days’re becoming a more popular choice for decidedly mainstream models. The latest entrants to the all-wheel stable include the Mazda6, Nissan Altima and Toyota Prius. As sales of crossovers, sport utility vehicles and pickups have grown, automakers are equipping more of automakers sedans with all-wheel drive to hang onto buyers wanting more SUV-like features. All-wheel or four-wheel drive is standard on most SUVs and trucks, helping to boost its availability to a record 63.4% of new vehicles sold last year, up from 56.4% a decade ago, according to data from Edmunds."
		article = clearBrackets(article)
		triplets = []
		for x in sent_tokenize(article):
			ml = getTriplets(x, show) #getting triplets for each sentence
			triplets+=ml
			# print("here2")
			if(show):
				input("\n\t\t\tPress ENTER to see next sentence...") #to pause execution
		if(show):
			input("\n\t\tPress ENTER to see next ARTICLE...")


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
		ttaken = round(time.time() - tvar, 2)
		tlist.append(ttaken)
		trem = round(mean(tlist)*300 - mean(tlist)*k, 2)
		print("article "+str(k)+" / "+str(tlen)+"\t\ttime taken: "+str(ttaken)+" sec | Mean time: "+str(round(mean(tlist),2))+" | Time remaining: "+str(trem)+" sec or "+str(round(trem/60,2))+" mins")
		tvar = time.time()
		# if k>2: #just to see output from top 2 articles
		# 	break

if(show):
	exit()

## to write into a file
file = open('new_9.csv','w')
for x in output:
	for y in x:
		file.write(y.replace(',','').replace('‘','\'').replace('’','\'').replace('“','\'').replace('”','\'').replace('"','').replace('\n',' ')+', ')
	file.write("\n")
file.close()
csvFile.close()


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
