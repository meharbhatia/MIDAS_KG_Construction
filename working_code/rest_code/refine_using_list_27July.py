from flair.models import SequenceTagger
from flair.data import Sentence
import spacy
import en_core_web_sm
import csv
import nltk
import re
from nltk import sent_tokenize, word_tokenize
from fuzzywuzzy import process
import time
from statistics import mean

from spacyNER import getNERs


# ex = 'The company also showcased it\'s latest Dynasty series of marvellous vehicles, which were recently unveiled at the company\'s spring product launch in Beijing'
# ex = 'BYD quickly debuted it\'s E-SEED GT concept car and Song Pro SUV alongside it\'s all-new e-series models at the Shanghai International Automobile Industry Exhibition'
# ex = 'Ritwik Mishra\'s lawyer appealed to Reserve Bank of India to hear the case of Nirav Modi, Mehul Choksy, Rahul Gandhi, Arvind Keriwal and Ramanujam'
# ex = "John Sowa from India exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework"
# ex = "An Indian resident, John Sowa, exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework"
# ex = "A total of 23 new car models were exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework"
# ex = "John Sowa from India exhibited amazing dancing skills and performed Salsa at the event"
# ex = "\"What is your name?\", asked John"
# ex = "That is the place where John died"
# ex = "The Akash eagerly wanted Mehar Bhatia's four black jackets, green umbrella of John Sowa and Ritwik Mishra's red jeans"

# ex = "Norway has a lot of electric cars—so many that it can make anyone driving a new vehicle with an internal combustion engine look like a Luddite. Mercedes-Benz brought us there to experience the EQC—and possibly to normalize it in a sea of EVs that makes California look like a land of late adopters. Outside Oslo, where cars were larger and more upscale than in other parts of Europe, and Tesla vehicles (S and X) are a more common sight than around Los Angeles or the Bay Area, the EQC fit right in. DON'T MISS: Mercedes-Benz EQC Edition 1886 electric SUV kicks off a new era After a couple of rain-soaked days driving the EQC there last week, we can say that it will be a great addition in the U.S. when it arrives sometime in 2020. At about 187 inches long, the EQC400 4Matic crossover splices into the American mid-sizers."
ex = "BYD debuted its E-SEED GT concept car and Song Pro SUV alongside its all-new e-series models at the Shanghai International Automobile Industry Exhibition. The company also showcased its latest Dynasty series of vehicles, which were recently unveiled at the company’s spring product launch in Beijing. A total of 23 new car models were exhibited at the event, held at Shanghai’s National Convention and Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework. Today, China’s new energy vehicles have entered the ‘fast lane’, ushering in an even larger market outbreak. Presently, we stand at the intersection of old and new kinetic energy conversion for mobility, but also a new starting point for high-quality development. To meet the arrival of complete electrification, BYD has formulated a series of strategies, and is well prepared."
# ex = "BYD debuted BYD E-SEED GT concept car and Song Pro SUV alongside BYD all-new e-series models at the Shanghai International Automobile Industry Exhibition. BYD also showcased BYD latest Dynasty series of vehicles, which were recently unveiled at BYD spring product launch in Beijing. A total of 23 new car models were exhibited at its latest Dynasty series of vehicles, which were recently unveiled at the companys spring product launch in Beijing, held at Eâ€™s National Convention and the Shanghai International Automobile Industry Exhibition Center, fully demonstrating the BYD New Architecture (BNA) design, the 3rd generation of Dual Mode technology, plus the e-platform framework. Today, Chinaâ€™s new energy vehicles have entered the â€˜fast laneâ€™, ushering in an even larger market outbreak. Presently, BYD stand at the intersection of old and new kinetic energy conversion for mobility, but also a new starting point for high-quality development. To meet the arrival of complete electrification, BYD has formulated a series of strategies, and is well prepared."
# ex = "Celebrity chef Jamie Oliver's British restaurant chain has become insolvent, putting 1,300 jobs at risk. The firm said Tuesday that it had gone into administration, a form of bankruptcy protection, and appointed KPMG to oversee the process. The company operates 23 Jamie's Italian restaurants in the U.K. The company had been seeking buyers amid increased competition from casual dining rivals, according to The Guardian. Oliver began his restaurant empire in 2002 when he opened Fifteen in London. Oliver, known around the world for his cookbooks and television shows, said he was 'deeply saddened by this outcome and would like to thank all of the staff and our suppliers who have put their hearts and souls into this business for over a decade. 'He said 'I appreciate how difficult this is for everyone affected.' I’m devastated that our much-loved UK restaurants have gone into administration."

# ex = "John went to the market by car, and Mary went to the school"
# ex = "Akash Kumar Sharma's friend bought four new cars"

# ex = ex.strip('.').strip('!').replace('‘','\'').replace('’','\'').replace('“','"').replace('”','"')



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

tagger = SequenceTagger.load('chunk')
nlp = en_core_web_sm.load()

csv_final_list = []
with open(r'C:\Users\mehar\Desktop\MIDAS\Internship\data\icdm_trial.csv','rt', encoding="utf8")as mainfile:
	
	data = csv.reader(mainfile)
	next(data)
	for row in data:
		ex = row[1]
		ex = clearBrackets(ex)
		industry = row[2]
		index = row[0]
		

		# sentence = Sentence('BYD quickly debuted it\'s E-SEED GT concept car and Song Pro SUV alongside it\'s all-new e-series models at the Shanghai International Automobile Industry Exhibition .')
		sentence = Sentence(ex)

		tagger.predict(sentence)
		strchunked = sentence.to_tagged_string()
		# print("\n")
		# sentence = nltk.sent_tokenize(sentence)
		# print(sentence)
		# print("\nChunked sentence")
		# print(strchunked)

		# nlp = en_core_web_sm.load()
		doc = nlp(ex)
		# pos_tags = [(i, i.tag_) for i in doc]
		pos_tags = nltk.pos_tag(nltk.word_tokenize(ex))
		# print("\nPOS tags")
		# print(pos_tags)


		listchunked = strchunked.split()
		# print(len(listchunked))
		# print(len(pos_tags))
		# print("\n\n")
		ph = ""
		sentence = []

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

		entity_list_old = []
		entity_list = []
		# print("CHUNKS from spacy")
		for x in sentence:
			# print(x)
			if (x[1] == 'NP'):
				# print(x)
				entity_list_old.append(x[0])

		#Uses Function 
		# print("Spacy NER")
		# nlp = en_core_web_ssm.load()
		# print(ex)
		for x in getNERs(ex, nlp):
			# print(x)
			entity_list_old.append(x[0])

		# print("\n\n\t INITAL LIST")
		# print(entity_list_old)
		# print(len(entity_list_old))

		# print("\n\n\t REMOVED DUPLICATE FROM LIST")
		for x in entity_list_old:
			if (x not in entity_list):
				entity_list.append(x)
		# print(entity_list)
		# print(len(entity_list))

		fin_list = entity_list
		# print("\n\n\t REMOVED punctuations")


		punctuations = '''!()-[]{};:'",<>./?@#$%^&*_~'''


		entity_list_punc = []
		entity_list_no_punc = []
		for entity in fin_list:
			e = entity[-1:]
			if(e in punctuations):
				entity_no_punct = entity[:-1]
				# print(entity_no_punct)
				entity_list_punc.append(entity_no_punct)
			else: 
				entity_list_no_punc.append(entity)

		entity_list = entity_list_no_punc + entity_list_punc
		# print(entity_list)
		# print(len(entity_list))

		# print("Remove middle fullstops")

		fullstops = '''.'''

		entity_list_break = entity_list

		def before(value, a):
		    # Find first part and return slice before it.
		    pos_a = value.find(a)
		    if pos_a == -1: return ""
		    return value[0:pos_a]

		def after(value, a):
		    # Find and validate first part.
		    pos_a = value.rfind(a)
		    if pos_a == -1: return ""
		    # Returns chars after the found string.
		    adjusted_pos_a = pos_a + len(a)
		    if adjusted_pos_a >= len(value): return ""
		    return value[adjusted_pos_a:]

		e1_list = []
		e1_list_2 = []
		for entity in entity_list_break:
			for char in entity:
				if char in fullstops:
					e1 = before(entity, ".")
					e1 = e1.lstrip()
					e2 = after(entity, ".")
					e2 = e2.lstrip()
					if (e1.isupper() and e2.isupper()):
						e1_list.append(entity)
						break
					e1_list.append(e1)
					e1_list.append(e2)
					break
			else:
				e1_list_2.append(entity)
		# print(e1_list)
		# print(e1_list_2)
		entity_list = e1_list + e1_list_2
		# print("DONE", entity_list)

		# print("\n\n Remove middle commas")
		fullstops_comma = ''','''
		entity_list_break = entity_list
		e1_list = []
		e1_list_2 = []
		for entity in entity_list_break:
			for char in entity:
				if char in fullstops_comma:
					e1 = before(entity, ",")
					e1 = e1.lstrip()
					e2 = after(entity, ",")
					e2 = e2.lstrip()
					if (e1.isupper() and e2.isupper()):
						e1_list.append(entity)
						break
					e1_list.append(e1)
					e1_list.append(e2)
					break
			else:
				e1_list_2.append(entity)
		# print(e1_list)
		# print(e1_list_2)
		entity_list = e1_list + e1_list_2
		# print("DONE", entity_list)

		# print("\n\n Remove middle ")
		fullstops_comma = '''”'''
		entity_list_break = entity_list
		e1_list = []
		e1_list_2 = []
		for entity in entity_list_break:
			for char in entity:
				if char in fullstops_comma:
					e1 = before(entity, "”")
					e1 = e1.lstrip()
					e2 = after(entity, "”")
					e2 = e2.lstrip()
					if (e1.isupper() and e2.isupper()):
						e1_list.append(entity)
						break
					e1_list.append(e1)
					e1_list.append(e2)
					break
			else:
				e1_list_2.append(entity)
		# print(e1_list)
		# print(e1_list_2)
		entity_list = e1_list + e1_list_2
		# print("DONE", entity_list)

		for entity in entity_list:
			if (entity == ''):
				entity_list.remove(entity)

		entity_list_old_old = entity_list


		for x in entity_list_old_old:
			if (x not in entity_list):
				entity_list.append(x)
		# print(entity_list)
		# print(len(entity_list))

		for entity in entity_list:
			if (entity == ''):
				entity_list.remove(entity)

		entity_list_clean = []
		for entity in entity_list:
			if (entity != ''):
				entity_list_clean.append(entity)
		entity_list = entity_list_clean
		# print("\n\n CHECKKK", entity_list)
		
		import nltk
		from nltk.corpus import stopwords
		stop_words = set(stopwords.words('english'))

		ent_list = entity_list
		entity_list_nostop = []
		entity_list_stop = []

		for entity in ent_list:
			first_word = entity.split()[0]
			first_word = first_word.lower()
			if first_word in stop_words:
				# print(entity)
				new_entity = entity.partition(' ')[2]
				if new_entity is not "":
					# print(new_entity)
					entity_list_nostop.append(new_entity)
			else:
				entity_list_stop.append(entity)

		entity_list = entity_list_nostop + entity_list_stop
		# print(entity_list)
		# print(len(entity_list))

		# print("Removed stopwords if present in first")

		entity_list_3 = entity_list
		entity_list4 = []
		for en in entity_list_3:
			if(len(en.split())) ==1:
				# print("ONE WORD", en)
				if (len(en) == 1 or len(en) == 2):
					# print("ONE CHAR", en)
					entity_list4.append(en)
		
		# print("LOOOK", entity_list4)
		# print(len(entity_list))
		entity_list = list(set(entity_list) - set(entity_list4))
		# print(entity_list)
		# print(len(entity_list))

		entity_list_old = entity_list
		for x in entity_list_old:
			if (x not in entity_list):
				entity_list.append(x)
		

		# print("\n\n", entity_list)
		# print(len(entity_list))




		for entity in entity_list:
			for i in range(1, len(entity.split())):
				# print(i)
				first = ' '.join(entity.split()[:i])
				last  = ' '.join(entity.split()[i:])
				for match in entity_list:
					if first in match:
						# print("MMM", match)
						for m in entity_list:
							if (last in m):
								if (first == match):
									# print("FIRST", first)
									# print("LAST", last)
									if first in entity_list:
										entity_list.remove(first)
								if (last == m):
									if last in entity_list:
										entity_list.remove(last)
						# print("FOUND FIRST", first)
						# print("last is", last)
						# entity_list.remove(first)
						# print("CHECK F", entity_list)
				# for match in entity_list:
					# if last == match:
						# print("MMMMM", match)
						# print("FOUND last", last)
						# print("First is", first)
						# entity_list.remove(last)
						# print("CHECK L", entity_list)

		print("\n \n FINAL LIST ")
		print(entity_list)
		# print(len(entity_list))


		# entity_list2 = entity_list
		# for x in entity_list2:
		# 	#x in the entity here. Compare with all
		# 	for y in entity_list2


		# entity_list = ['process', 'company', 'Guardian', 'a decade', 'U', 'firm', 'form', 'company', 'restaurant empire', 'world', 'outcome', 'staff', 'suppliers', 'hearts and souls', 'business', 'much-loved UK restaurants', 'a decade', 'cookbooks and television shows', 'K', 'London', 'U.K', "Celebrity chef Jamie Oliver's British restaurant chain", '1,300 jobs', 'Tuesday', 'KPMG', "23 Jamie's Italian restaurants", 'buyers', 'increased competition', '2002', 'Fifteen', 'everyone', 'Jamie Oliver', 'British', '23 Jamie', 'Italian', 'Guardian', 'London', 'UK', 'insolvent', 'risk', 'administration', 'bankruptcy protection', 'casual dining rivals']

		tvar = time.time()	
		tlen = 300	
		print("Reading triplets from csv file")
		i = 0
		csv_list = []
		with open(r'C:\Users\mehar\Desktop\MIDAS\Internship\submission_11_52.csv','rt', encoding="utf8")as infile:
			data = csv.reader(infile)
			for row in data:
				if (row[0] == industry and row[1] == index):
					# print(row)
					csv_list.append(row)
					# data_dict.append(row)
					i+=1

		# print(csv_list)
		# print("Number of triplets for file 12: ", i)

		def check(string, sub_str): 
			if (string.find(sub_str) == -1): 
				ans = False
			else: 
				ans = True 
			
			return ans        
		# driver code 
		string = "Celebrity chef Jamie Oliver's British restaurant chain"
		sub_str = "Celebrity chef Jamie Oliver"
		# print(check(string, sub_str)) 

		for rowlist in csv_list:
			# rowlist = ['cateringServices', '0', ' insolvent', ' quality', ' Celebrity chef Jamie Oliver']
			count = 0
			attribute1 = rowlist[2]
			attribute3 = rowlist[4]
			attribute2 = rowlist[3]

			# if (attribute1 == attribute3):
			# 	print("SAME SO Remove", rowlist)
			# 	csv_list.remove(rowlist)

			for entity in entity_list:
				if (check(entity, attribute1) or check(entity, attribute3)) == True:
					# print("1", attribute1)
					# print("3", attribute3)
					# print("CORRES", entity)
					# print("\n")
					# print("A1, A3", attribute1, attribute3)
					# print("CORESS", rowlist)
					count+=1
				if((attribute1 == entity) or (attribute3 == entity)):
					count+=1
			if ((count == 0) or (attribute1 == attribute3)):
				# print("REM THESE ONES", rowlist)
				csv_list.remove(rowlist)


			#Making sure attiribute is not one letter or symbol or empty

		csv_list2 = csv_list
		for rowlist in csv_list2:	
			c = 0
			# del = False
			attribute1 = rowlist[2] #s1
			attribute3 = rowlist[4] #s2
			attribute2 = rowlist[3]
			for attr1 in attribute1:
				if attr1.isspace() != True:
					c+=1
			if (c == 1 or c == 0 or attr1 == ' ’'):
				# print("DEL1", rowlist)
				row_del = rowlist
				csv_list.remove(rowlist)
				# del = True

			c2 = 0
			for attr2 in attribute3:
				if attr2.isspace() != True:
					c2+=1
			if (c2 == 1 or c2 == 0 or attr2 == ' ’'):
				# print("DEL2", rowlist)
				if rowlist not in csv_list:
					break
				csv_list.remove(rowlist)

			c3 = 0
			for attr3 in attribute2:
				if attr3.isspace() != True:
					c3+=1
			if (c3 == 1 or c3 == 0 or attr3 == ' ’'):
				# print("DEL3", rowlist)
				if rowlist not in csv_list:
					break
				csv_list.remove(rowlist)

			
		print("FINAL")
		i=0
		for rowlist in csv_list:
			
			attribute1 = rowlist[2]
			attribute3 = rowlist[4]
			attribute2 = rowlist[3]
			
			if (attribute2 != " number"):
			#Switch with attribute 1
				#IF THERE IS AN EXACT MATCH
				for entity in entity_list:
					if (attribute1 == entity):
						continue
					if (attribute3 == entity):
						continue

					else:

						Ratios = process.extract(attribute1,entity_list)
						highest = process.extractOne(attribute1,entity_list)
						rowlist[2] = highest[0]
						# print("MATCH", highest[0], attribute1)

						# Ratios = process.extract(attribute2,entity_list)
						# highest = process.extractOne(attribute2,entity_list)
						# rowlist[3] = highest[0]
						# print("MATCH", highest[0], attribute2)

						Ratios = process.extract(attribute3,entity_list)
						highest = process.extractOne(attribute3,entity_list)
						rowlist[4] = highest[0]
						# print("MATCH", highest[0], attribute3)

					# i+=1
			print(rowlist)
		# print("Final Number", i)

		
		csv_final_list.append(csv_list)

output = [['industry', 'index', 's1', 'r', 's2']]
tl = []
for x in csv_final_list:
	for xx in x:
		output.append(xx)

with open("output_refined_11_52_take2_full_rest.csv", "w", newline = "", encoding="utf8") as f:
    writer = csv.writer(f)
    writer.writerows(output)
