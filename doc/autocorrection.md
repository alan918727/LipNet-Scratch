# LipNet-Scratch



## LipNet spell correction and prediction


### Grid Corpus dictionary usage

For this project, the grid corpus word dictionary is used to predict the output sentence from lips reading. It contains all the possible words which occurs in the video. 

    def __init__(self, path):
        self.dictionary = Counter(list(string.punctuation) + self.words(open(path).read()))
The counter function is used to return a counter list, which calculates the frequency of each word. The path is point to the dictionary text file path.

### Tokenize all the sentence 
Read all the sentence and tokenize the sentence. As a result, it returns a list contains all the single word in a sentence. Then lowercase all the single word.

	def tokenize(text):
		return re.findall(r"\w+|[^\w\s]", text, re.UNICODE)
  	def words(self, text):
	 	return re.findall(r'\w+', text.lower())

### Check Subset of Dictionary
    def known(self, words):
        return set(w for w in words if w in self.dictionary)

This code is to return all the **correct** subset words if the words appear in the GRID dictionary. The subset words are put in one set.

### Edit the word spelling
      

Here are several spelling error and difference from the correct word. As a result, there are several ways to edit the word spelling.


*  Delete letter
*  Add letter
* Replace letter
* Transpose letter

Below is the 4 ways to edit the misspell word **one time**.
	
	def edits1(self, word):

        letters    = 'abcdefghijklmnopqrstuvwxyz'
        splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
        deletes    = [L + R[1:]               for L, R in splits if R]
        transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
        replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
        inserts    = [L + c + R               for L, R in splits for c in letters]
        return set(deletes + transposes + replaces + inserts)

Since there may be some big misspelling which cannot be corrected in single time. So if the word is still not in the subset of dictionary, one more edit is executed.

	def edits2(self, word):
		return (e2 for e1 in self.edits1(word) for e2 in self.edits1(e1))


### Generate all candidates word

Then all the spelling corrections candidates are generated.

    def candidates(self, word):
        return (self.known([word]) or self.known(self.edits1(word)) or self.known(self.edits2(word)) or [word])

### Predict the maximum probability

From the counter list of dictionary, we could calculate the probability of appearace for each word.
	
	def P(self, word, N=None):
		if N is None:
			N = sum(self.dictionary.values())
		return self.dictionary[word] / N

Choose the candidates word with the maximum probability.

	def correction(self, word):
    	return max(self.candidates(word), key=self.P)

Then this correction function is applied toto correct all the sentence.

    def corrections(self, words):
        return [self.correction(word) for word in words]


### Untokenize sentence

Untokenize the tokenized sentence. Combine all the words into a full sentence, a **string** type will be returned.

	def untokenize(words):
	    text = ' '.join(words)
	    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...')
	    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
	    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
	    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
	    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
	         "can not", "cannot")
	    step6 = step5.replace(" ` ", " '")
	    return step6.strip()

### Command to autocorrection the sentence

For the Spell class, the **spell.sentence(self,sentence)** is to autocorrect the input sentence and return the correction string type sentence.

	def sentence(self, sentence):
		return untokenize(self.corrections(tokenize(sentence)))

As a result, we could import the rough sentence output by the lips reading prediction. Then the autocorrection program will correct the sentence and gives a more accuracy output. 

Below is a simple example of autocorrection. The rough input sentence is ``thiis obwjecd is an redd apwle``.
After correction, the autocorrection program gives a correct output ``this object is an red apple``

	>>> from lipnet.utils.spell import Spell
	>>> import os
	>>> PREDICT_DICTIONARY = "D:/GitHub/LipNet/common/dictionaries/big.txt"
	>>> spell=Spell(path=PREDICT_DICTIONARY)
	>>> corr=spell.sentence('thiis obwjecd is an redd apwle')
	>>> print(corr)
	this object is an red apple
	>>>
