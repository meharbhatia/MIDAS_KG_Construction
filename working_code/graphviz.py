from graphviz import *
import pandas as pd
import re



data = pd.read_csv('/path/to/submission.csv')


k=0
while k<len(data):
	k2 = k
	while k2+1 != len(data) and data.iloc[k2]["index"]==data.iloc[k2+1]["index"]:
		k2+=1
	sdata = data.loc[k:k2,:]
	print(sdata)
	nset = list(set(sdata["s1"]).union(set(sdata["s2"])))
	dot = Graph()
	for x in nset:
		dot.node(re.sub(r'\W+', ' ', x), x)
	i = 0
	while i < len(sdata):
		dot.edge(re.sub(r'\W+', ' ', sdata.iloc[i]["s1"]), re.sub(r'\W+', ' ', sdata.iloc[i]["s2"]), label=sdata.iloc[i]["r"])
		i+=1
	pathstr = "images/"+sdata.iloc[0]["industry"]+str(sdata.iloc[0]["index"])
	dot.render(pathstr, format='png', view=True)


	input('Press Enter...')

	k = k2
	k+=1
