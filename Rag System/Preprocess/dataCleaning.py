import re
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords

nltk.download('punkt')
nltk.download('stopwords')

# Create stop words list
stopWords = stopwords.words('english')
# Remove 'not' and 'no' from the stop words list since they have value in context
stopWords.remove('not')
stopWords.remove('no')

def stopWordsRemoval(sentence):
    # Tokenize
    tokens = nltk.word_tokenize(sentence)
    # Filter stop words
    filteredTokens = [token for token in tokens if token.lower() not in stopWords]
    processedText = ' '.join(filteredTokens)
    return processedText

# (\\b[A-Za-z] \\b|\\b [A-Za-z]\\b):
# - \\b[A-Za-z] \\b: Matches a single alphabetic character [A-Za-z] surrounded by word boundaries \\b (i.e., not preceded or followed by other letters or digits).
# - |: Alternation operator to match either of the patterns separated by it.
# - \\b [A-Za-z]\\b: Matches a single alphabetic character [A-Za-z] preceded or followed by a space \\b and followed or preceded by word boundaries \\b.
# - '': Replace the matched patterns with an empty string, effectively removing them from the text.
def singleCharactersRemoval(sentence):
    sentence = re.sub('(\\b[A-Za-z] \\b|\\b [A-Za-z]\\b)', '', sentence)
    return sentence

# Creates a regex pattern to match any character from charsList, treating them literally.
def specialCharactersRemoval(sentence, charsList):
    sentence = re.sub('[' + re.escape(''.join(charsList)) + ']', ' ', sentence)
    return sentence

# \s+ matches one or more whitespace characters.
def multipleSpacesRemoval(sentence):
    sentence = re.sub(r'\s+', ' ', sentence)
    return sentence

def htmlTagsRemoval(inputString):
    # Check if inputString is indeed a string and looks like it might contain HTML
    if isinstance(inputString, str) and '<' in inputString and '>' in inputString:
        soup = BeautifulSoup(inputString, 'html.parser')
        return soup.get_text()
    # If inputString doesn't look like HTML, return it unchanged
    return inputString
