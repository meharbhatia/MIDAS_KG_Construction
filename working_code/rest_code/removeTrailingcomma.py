
file = open('../../submissions/new_13_withJjPosCdExtractor.csv','r')
content = file.readlines()
file.close()
file = open('../../submissions/new_13_withJjPosCdExtractor.csv','w')

k=0
while k<len(content):
	content[k] = content[k].strip().strip(',')
	file.write(content[k]+'\n')
	k+=1

file.close()