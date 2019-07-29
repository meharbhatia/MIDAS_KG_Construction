from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk import sent_tokenize 
from nltk.util import ngrams
from collections import Counter
from spacyNER import getNERs
from flairChunking import getPhrasesfromfile
from nltk.stem import WordNetLemmatizer
from statistics import mean 
import csv
import time
import en_core_web_sm

def removeNgrams(ngrams):
	k=0 
	while k < len(ngrams):
		if(len(ngrams[k][0][0]) == 1 or ngrams[k][1] < 2 or ngrams[k][0][0] == "'s"):
			ngrams = ngrams[:k] + (ngrams[k+1:] if k+1 < len(ngrams) else [])
			k-=1
		k+=1
	return ngrams


def getNgrams(ex):
	nngrams = []
	stop_words = set(stopwords.words('english')) 
	word_tokens = word_tokenize(ex) 
	filtered_sentence = [w for w in word_tokens if not w in stop_words] 
	uni = removeNgrams(Counter(ngrams(filtered_sentence,1)).most_common(10))
	bi = removeNgrams(Counter(ngrams(filtered_sentence,2)).most_common(10))
	tri = removeNgrams(Counter(ngrams(filtered_sentence,3)).most_common(10))
	nngrams.append(uni)
	nngrams.append(bi)
	nngrams.append(tri)
	return nngrams

def nounfilter(nphrases):
	k = 0
	while k < len(nphrases):
		if(nphrases[k][1] != 'NP'):
			nphrases = nphrases[:k] + (nphrases[k+1:] if k+1 < len(nphrases) else [])
			k-=1
		k+=1
	return nphrases

def presentIn(gword, nlist):
	f = False
	k=0
	while k < len(nlist):
		if (gword in nlist[k][0]):
			f = True
			break
		k+=1
	return f

def traverseConnected(triplets):
	k = 0
	ignorelist = ["it", "us", "we", "I"]
	while k < len(triplets):
		if (triplets[k][5] == 'X'):
			triplets[k][5] = 'Y'
			k2 = 0
			while k2 < len(triplets):
				# if ( (triplets[k][2] == triplets[k2][2] or triplets[k][2] == triplets[k2][4] or triplets[k][4] == triplets[k2][4] or triplets[k][4] == triplets[k2][2]) and triplets[k2][5] == 'O'):
				if ( (triplets[k][2] == triplets[k2][4] or triplets[k][4] == triplets[k2][2]) and triplets[k2][5] == 'O'):
					triplets[k2][5] = 'X'				
				k2+=1
			k = -1
		k+=1
	return triplets

def removeDuplicates(triplets):
	k=0
	while k < len(triplets) - 1:
		if (triplets[k] in (triplets[:k] + triplets[k+1:]) or triplets[k][2] == triplets[k][4]):
			triplets = triplets[:k] + triplets[k+1:]
			k-=1
		k+=1
	return triplets

def getXY(triplets):
	k = c = 0
	while k < len(triplets):
		if (triplets[k][5] != 'O'):
			c+=1
		k+=1
	return c


if __name__ == "__main__":
	file = open('../../datasets/CLEANED_icdm_contest_data.csv', 'r')
	reader = csv.reader(file)
	nlp = en_core_web_sm.load()
	show = False
	next(reader)
	ftriplets = [['industry', 'index', 's1', 'r', 's2','Y']]
	tvar = time.time()
	tlist = []
	tlen = 300
	count = 0
	for row in reader:
		article = row[1]
		Ngrams = getNgrams(article)
		ners = getNERs(article, nlp)
		sent = sent_tokenize(article)
		s = 0
		nphrases = []
		while s < len(sent):
			nphrases += getPhrasesfromfile(row[2], int(row[0]), s)
			s+=1
		nphrases = nounfilter(nphrases)
		if(show):
			print("\n\n")
			print(Ngrams)
			print(Ngrams[0])
			print(Ngrams[0][0])
			print(Ngrams[0][0][0])
			print(Ngrams[0][0][0][0])
			print("\n\n")
			print(ners)
			print("\n\n")
			print(nphrases)
			print("\n\n")
		tfile = open('../../submissions/new_20_CLEAN.csv','r')
		treader = csv.reader(tfile)
		next(treader)
		atriplets = []
		for trow in treader:
			if (row[2] == trow[0] and int(trow[1]) == int(row[0])):
				tl = []
				tl.append(trow[0])
				tl.append(trow[1])
				tl.append(trow[2])
				tl.append(trow[3])
				tl.append(trow[4])
				tl.append('Z')
				atriplets.append(tl)
		tfile.close()
		
		atriplets = removeDuplicates(atriplets)
		if(show):
			for x in atriplets:
				print(x)
			# input('Wait... Enter...')


		# n = 0
		# while n < len(Ngrams[0]):
		# 	if ( presentIn(Ngrams[0][n][0][0], ners) or presentIn(Ngrams[0][n][0][0], nphrases)):
		# 		k = 0
		# 		while k < len(atriplets):
		# 			if (atriplets[k][2] == Ngrams[0][n][0][0] or atriplets[k][4] == Ngrams[0][n][0][0]):
		# 				atriplets[k][5] = 'X'
		# 			k+=1

		# 	n+=1


		# if(show):
		# 	print("\n\n")
		# 	for x in atriplets:
		# 			print(x)
		
		# atriplets = traverseConnected(atriplets)

		# if(show):
		# 	print("\n\n")
		# 	for x in atriplets:
		# 			print(x)

		# if(show):
		# 	print(getXY(atriplets))
		# 	input('enter')

		ftriplets+=atriplets

		count+=1
		ttaken = round(time.time() - tvar, 2)
		tlist.append(ttaken)
		trem = round(mean(tlist)*300 - mean(tlist)*count, 2)
		print("article "+str(count)+" / "+str(tlen)+"\t\ttime taken: "+str(ttaken)+" sec | Mean time: "+str(round(mean(tlist),2))+" | Time remaining: "+str(trem)+" sec or "+str(round(trem/60,2))+" mins")
		tvar = time.time()

	file.close()

	file = open('../../submissions/new_19_REDUCED.csv','w')
	for x in ftriplets:
		k=0
		while k<len(x)-1 and x[-1] != 'O':
			file.write(x[k].replace(';','').replace(',','').replace('‘','\'').replace('’','\'').replace('“','\'').replace('”','\'').replace('"','').replace('\n',' '))
			if(k+2 != len(x)):
				file.write(',')
			k+=1
		if(x[-1] != 'O'):
			file.write("\n")
	file.close()


