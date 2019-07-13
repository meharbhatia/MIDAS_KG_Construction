#sudo pip3 install flair
from flair.models import SequenceTagger
from flair.data import Sentence

tagger = SequenceTagger.load('chunk')

sentence = Sentence('BYD quickly debuted its E-SEED GT concept car and Song Pro SUV alongside its all-new e-series models at the Shanghai International Automobile Industry Exhibition . ')

tagger.predict(sentence)
print(sentence.to_tagged_string())