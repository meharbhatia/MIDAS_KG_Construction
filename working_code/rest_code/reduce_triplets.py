from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from nltk.util import ngrams
from collections import Counter

example_sent = "Ford says shifter cables can snap off and render the gear selector broken or useless on 2013–2016 Ford Fusion sedans. The automaker's latest recall expands a July 2018 recall of about a half-million cars. The 2019 Ranger also has a similar transmission problem under a separate new recall. Ford is recalling 259,182 additional Fusion sedans in the United States for faulty shifter cables that can cause rollaways, the automaker said Wednesday. In July, Ford recalled more than a half-million Fusion and Escape models for these shifter cables, which can break off the transmission due to a bad bushing at the connection point. A supplier had added lubricant to these bushings, which ultimately led them to fail on 2013–2016 Fusion and 2013–2014 Escape models, according to a recall filing with the National Highway Traffic Safety Administration (NHTSA). Several dangerous things can happen, such as the gear selector indicating the wrong gear or a driver switching off the vehicle in park and exiting with the key when the transmission is actually in neutral."

stop_words = set(stopwords.words('english')) 

word_tokens = word_tokenize(example_sent) 

filtered_sentence = [w for w in word_tokens if not w in stop_words] 

filtered_sentence = [] 

for w in word_tokens: 
	if w not in stop_words: 
		filtered_sentence.append(w) 

print(word_tokens) 
print("\n\n")
print(filtered_sentence) 
print("\n\n")
print(Counter(ngrams(filtered_sentence,1)).most_common(10))
print("\n\n")
print(Counter(ngrams(filtered_sentence,2)).most_common(10))
print("\n\n")
print(Counter(ngrams(filtered_sentence,3)).most_common(10))