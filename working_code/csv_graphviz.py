# sudo apt-get update
# sudo apt-get install graphviz
# sudo pip3 install graphviz
from graphviz import *
import pandas as pd
import re



data = pd.read_csv('../submissions/submission.csv')


k=0
while k<len(data):
	k2 = k
	while k2+1 != len(data) and data.iloc[k2]["index"]==data.iloc[k2+1]["index"]:
		k2+=1
	sdata = data.loc[k:k2,:]
	# print(sdata)
	nset = list(set(sdata["s1"]).union(set(sdata["s2"])))
	dot = Graph()
	for x in nset:
		dot.node(re.sub(r'\W+', ' ', x), x)
	i = 0
	while i < len(sdata):
		try:
			dot.edge(re.sub(r'\W+', ' ', sdata.iloc[i]["s1"]), re.sub(r'\W+', ' ', sdata.iloc[i]["s2"]), label=sdata.iloc[i]["r"])
		except:
			pass
		i+=1
	pathstr = "images/"+sdata.iloc[0]["industry"]+str(sdata.iloc[0]["index"])
	# dot.render(pathstr, format='png', view=True)
	dot.render(pathstr, format='png')


	# input('Press Enter...')

	k = k2
	k+=1
	print(str(k)+" / "+str(len(data)))
