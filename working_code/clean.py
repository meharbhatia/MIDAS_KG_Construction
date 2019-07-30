import re
import csv

output = [['index', 'content', 'industry']]
str1 = ""
with open('../datasets/icdm_contest_data.csv', 'r') as csvFile:
	reader = csv.reader(csvFile)
	next(reader)
	t = 0
	for row in reader:
		# print(row[1])
		# # input()
		tl = []
		re1 = re.search(r'\w—\w',row[1])
		while (re1):
			index = row[1].find(re1.group())
			row[1] = row[1][:index] + row[1][index:index+len(re1.group())].replace('—', ', ') + row[1][index+len(re1.group()):]
			re1 = re.search(r'\w—\w',row[1])
		re1 = re.search(r'[a-z]\.[A-Z]',row[1])
		while (re1):
			index = row[1].find(re1.group())
			row[1] = row[1][:index+2] + " " + row[1][index+2:]
			re1 = re.search(r'[a-z]\.[A-Z]',row[1])
		str1 = row[1]
		str1 = str1.replace('\n','.\n')
		ml = str1.split('\n')
		k = 0
		while k<len(ml):
			if (len(ml[k])<4 or "{{" in ml[k] or (len(ml)<35 and "Thanks for being a subscriber" in ml[k])):
				# print(ml,"\n\n\n")
				ml = ml[:k] + (ml[k+1:] if k+1<len(ml) else [])
				k-=1
				# print(ml)
				# input('wait')
			k+=1
		str1 = ' '.join(ml)

		tl.append(row[0])
		tl.append(str1)
		tl.append(row[2])
		output.append(tl)
		t+=1

file = open('../datasets/CLEANED_icdm_contest_data.csv','w')
for x in output:
	file.write(x[0]+",\""+x[1].replace('"','""')+"\","+x[2])
	file.write("\n")
	# for y in x:
	# 	file.write('"'+y.replace('"','""')+'"'+',')
	# file.write("\n")
file.close()
csvFile.close()




