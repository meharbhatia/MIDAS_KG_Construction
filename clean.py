import re
import csv

output = [['index', 'content', 'industry']]
str1 = ""
with open('icdm_contest_data.csv', 'r') as csvFile:
	reader = csv.reader(csvFile)
	next(reader)
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

		

		tl.append(row[0])
		tl.append(row[1])
		tl.append(row[2])
		output.append(tl)

file = open('CLEANED_icdm_contest_data.csv','w')
for x in output:
	file.write(x[0]+",\""+x[1].replace('"','""')+"\","+x[2])
	file.write("\n")
	# for y in x:
	# 	file.write('"'+y.replace('"','""')+'"'+',')
	# file.write("\n")
file.close()
csvFile.close()




