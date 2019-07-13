Updates about submission
```new_6.csv``` is created by using spacyNER+rulebased , dataset input was cleaned dataset, removed isolated nodes (even with isolated nodes number of tupples were more or less same)
# 2019 ICDM/ICBK Knowledge Graph Contest #
Link: http://icdm2019contest.mlamp.cn/#/app/home 

## Install ##
```
git clone https://github.com/meharbhatia/MIDAS_KG_Construction.git
cd MIDAS_KG_Construction
chmod +x install.sh
yes y | ./install.sh
```

Your submission should include an output file that contains all graphs constructed from each article provided, source code with instructions for installation and execution, any external sources of data used, and a ReadMe report on how your graphs are represented in the output file. The submitted source code is expected to process the published dataset and output all triples or predicates in a file in the same format as submitted. The submitted ZIP file can be organized as follows:

-KGC2019/ 
| +readme.txt
| +submission.csv
| +sourcecode/

Team submissions will be judged by competition organizers on (a) their overall quality of the constructed knowledge graphs, and (b) generalization ability of their methodology in multiple domains.

After the submission deadline, some shortlisted teams will be invited to each build a web application to deploy the model they have submitted. The web application should generate a knowledge graph from each input text. Each contest reviewer will score the quality of the generated graph from the web application. The final score for each shortlisted team is the average of scores from all reviewers.


### Following FAQs copied from the site ###

FAQs
Q: Where is the team registration portal?
A: Please sign in first to create your group or join an existing group.
Q: How can I invite someone to join my team/ How can I join an existing team?
A: Please use the password during the team creation/ Please ask any member of the team for the password.
Q: What are the contents of the dataset?
A: Our sample dataset contains 300 short text data with an industry label from the following four labels:‘automotiveEngineering’, ‘cosmetics’, ‘publicSecurity’, ‘cateringServices’.
Q: Do we have limitation on trial submissions?
A: Each team is allowed to submit result up to 6 times a day.
Q: What does an expected output look like?
A: The output for each sample should be a knowledge graph stored in several triplets. The submission is supposed to contain a CSV file containing the triplets for all sample data with an index column specifying the respecting text, and a column of the industry. For more details, please log in to the contest website and go to Personal Scores -> Upload Result.
Q: Does the example code generate expected output?
A: The example code gives an appropriate form of the submission file, however, the samples might not be the true answers.
Q: Is there any specification for the entities and relations expected from the contest?
A: There is no specification for the type of relation or range of entities, except the entities must be spans from the text dataset.
Q: Do we have a limit on the number of tuples that we extract from each article?
A: There is no limitation, but we are expecting 5-10 for each text. Too much or too less tuples could affect your score according to the evaluation algorithm.
Q: The example submission file contains only four types of relationships. Are we allowed to extend upon this?
A: Of course you can have more types of relations as long as naming the same kind of relation by the same name.
Q: Since there is an example image of a knowledge graph shown in the website specification page, is knowledge graph visualization also a part of the contest?
A: The knowledge graph image is not required to submit in the first stage of the contest. In the second stage, each team is expected to develop a web application which visualizes the knowledge graph of each text data.
Q: Are the output triplets supposed to rely on each independent article or cross the texts among each industry?
A: The triplets should be extracted for each article independently, but candidates can design different model for each industry.
Q: Are external resources allowed in the contest?
A: Candidates are welcomed to use external resources to design the model as long as specified in your report.
Q: What are the evaluation metrics?
A: Please sign in first and find the scoring rule on Personal Scores -> Upload Result.
Q: what quantitative standards are used to measure the quality of the generated graphs? How do you weigh this score?
A: Please sign in to the contest website and read the guide on upload result page, which has been explained in detail. (http://icdm2019contest.mlamp.cn/#/app/upload). Briefly speaking, in the online evaluation process, the quality of the graph is measured by calculating the average graph edit distance between the results of each article you submit with ones labeled by experts. The graph edit distance is the number of edge/node changes needed to make two graphs isomorphic. To quantitative assessment, we adopt the graph edit distance function of networkx, a Python library for graph calculation.
Q: What are the synonym fault tolerance standards for the same node?
A: In the labeling process, industry experts will firstly label the synset of entity words mentioned in the article one by one, so as to form a synonym dictionary for each article. Before calculating the graph edit distance, we will first replace the entity words in your submitted results with the synset label to which the entity words belong according to the synonyms, then compare them with the results marked by experts to achieve the purpose of synonym tolerance. The standard of fault tolerance is determined by the industry experts responsible for labeling.
Q: In the figure of the example, the information covering the passage only includes the first sentence to the third sentence, and the information of the fourth sentence to the sixth sentence is not reflected. When measuring, do you consider measuring the quality of a graph using a full text?
A: The purpose of this competition is to generate the knowledge map in the brain of experts when they read the text. Different experts will have different attention on each sample data, which inevitably leads to subjective results. In order to ensure the objectivity as much as possible, each article is marked by two experts and then proofread by the organizers. Please note that online evaluation (as described publicly on the website) is only a tool to help everyone track their model iterations. The final shortlist is determined by the organizing committee after examining all the materials submitted in the package.
