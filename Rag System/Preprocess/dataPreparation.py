import re
import nltk
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

# Pos Tag Finder function
def posTagFinder(nltkTag):
    if nltkTag.startswith('J'):
        return wordnet.ADJ
    elif nltkTag.startswith('V'):
        return wordnet.VERB
    elif nltkTag.startswith('N'):
        return wordnet.NOUN
    elif nltkTag.startswith('R'):
        return wordnet.ADV
    else:
        return None
  
# Lemmatization Process
def lemmatizer(sentence):
    # Getting pos tags
    posTags = nltk.pos_tag(nltk.word_tokenize(sentence))
    wordnetTagged = list(map(lambda x: (x[0], posTagFinder(x[1])), posTags))
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatizedSentence = []
    for word, tag in wordnetTagged:
        if tag is None:
            lemmatizedSentence.append(word) # Avoid tagging unnecesary words
        else:
            lemmatizedSentence.append(lemmatizer.lemmatize(word, tag)) # Adding tag to lemmatize
    lemmatizedSentence = " ".join(lemmatizedSentence)
    return lemmatizedSentence

numWords = {
    'zero': '0', 'one': '1', 'two': '2', 'three': '3', 'four': '4', 'five': '5',
    'six': '6', 'seven': '7', 'eight': '8', 'nine': '9', 'ten': '10',
    'eleven': '11', 'twelve': '12', 'thirteen': '13', 'fourteen': '14',
    'fifteen': '15', 'sixteen': '16', 'seventeen': '17', 'eighteen': '18',
    'nineteen': '19', 'twenty': '20', 'thirty': '30', 'forty': '40',
    'fifty': '50', 'sixty': '60', 'seventy': '70', 'eighty': '80', 'ninety': '90',
    'hundred': '100', 'thousand': '1000', 'million': '1000000', 'billion': '1000000000'
}

def convertNumberToWords(text):
    # Replacing written numbers for literal ones
    for word, digit in numWords.items():
        text = re.sub(r'\b' + word + r'\b', digit, text)
    return text
