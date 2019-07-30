import spacy
import pandas as pd
from nltk import word_tokenize
nlp = spacy.load('en')
print(spacy.__version__)

import neuralcoref

neuralcoref.add_to_pipe(nlp, greedyness=0.50) #0.55 is best value I've seen

df = pd.read_csv('../datasets/CLEANED2_icdm_contest_data.csv', usecols = ['index', 'content', 'industry'])

longform = pd.DataFrame(columns=['coref_content', 'industry'])

pronouns = ["he", "she","his", "her", "him"]
t = 0 

for idx, index, content, industry in df.itertuples():
	# content = "John married Grace. He loved her and she also loves him."
	# content = "(The GT350R remains unchanged for 2019.) Assisting with the aforementioned development was veteran race driver Billy Johnson, who's spent three years working with the team while also racing Ford GTs and prepping the Mustang GT4 race car, which he's campaigning this year."

	doc = nlp(content)
	# print(doc._.has_coref)
	# print(doc, "\n\n")
	# print(doc._.coref_scores)
	# input('Wait')
	sar = []
	k=0
	while k<len(doc):
		sar.append(str(doc[k]))
		k+=1

	strar = []
	k = 0
	while k<len(doc):
		if(str(doc[k]).lower() in pronouns):
			token = doc[k]
			tstr = str(doc[k])
			# print(token)
			ml = sorted(token._.coref_scores[0].items(), key=lambda kv: kv[1])
			# print(ml)
			tempstr = str(ml[-1][0])
			# if (t==108):
			# 	print(token)
			# 	print(ml)
			# 	input()
			while tempstr.lower() in pronouns:
				ml = (ml[:-1] if len(ml)!=0 else [])
				# if(t==108):
				# 	print(ml)
				# 	input('klklk')
				if(len(ml)==0):
					strar.append(tstr)
					break
				
				tempstr = str(ml[-1][0])
				# print(ml)
			strar.append(tempstr)
			# print(sorted(token._.coref_scores[0].items(), key=lambda kv: kv[1]))
			# tempcontent = ' '.join(strar) + ' ' + ' '.join(sar[k+1:])
			# doc = nlp(tempcontent)

		else:
			strar.append(str(doc[k]))
		k+=1
	# print(' '.join(strar))
	# print(doc._.coref_resolved)
	doc = (' '.join(strar).replace('‘ ','\'').replace(' ’','\'').replace('“ ','\"').replace(' ”','\"').replace(' .','.').replace(' ,',',').replace(' ; ',' ').replace(' - ','-').replace(' – ','–').replace(' : ',': ').replace('( ','(').replace(' )',')'))

	
	# print(doc._.coref_clusters)
	# # print(type(doc._.coref_clusters))
	# print(doc._.coref_clusters[0].mentions[-1])
	# print(doc._.coref_clusters[0].mentions[-1]._.coref_cluster.main)
	# token = doc[4]
	# print(doc)
	# print(token._.coref_scores[0])
	# print(sorted(token._.coref_scores[0].items(), key=lambda kv: kv[1])[-1])
	# y = doc._.coref_clusters[0]
	# print(y[0])
	# print(y[1])
	# print(y[2])
	# print(doc._.coref_clusters[1])
	# print(doc._.coref_scores)
	# input('Wait')
	# doc = doc._.coref_resolved
	longform = longform.append(
		[{'coref_content': doc, 'index':index, 'industry': industry}],
		ignore_index = True
	)
	t+=1
	print("article "+str(t)+" /300")

longform['index'] = longform['index'].astype(int)
longform = longform[['index', 'coref_content', 'industry']]
# print(longform['content'].iloc[1])

input('Wait')
longform.to_csv("../datasets/g050_HeShe_Coref_Dataset.csv", index=False)
