
# Let's make a self learning chat bot( BayernBot )

#Packages (Install) : NLTK, newspaper3k (Scraping Articles)

#Problem Statement: An article would be used to train the bot and the bot would then be able to answer
# questions based upon the topic of that article.

#Project Guide Link:
# https://medium.com/@randerson112358/build-your-own-ai-chat-bot-using-python-machine-learning-682ddd8acc29

#REFRENCE DOCS:
#https://www.youtube.com/watch?v=QpMsT0WuIuI&t=769s
#https://www.machinelearningplus.com/nlp/cosine-similarity/ : Cosine Similarity would be used to find out the similarity
#between the query and the response.
#https://scikit-learn.org/stable/modules/feature_extraction.html
#https://newspaper.readthedocs.io/en/latest/
#https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise_distances.html
#https://docs.python.org/3/library/warnings.html
#https://pythonprogramming.net/wordnet-nltk-tutorial/

#We would be using https://scikit-learn.org/stable/modules/feature_extraction.html: Vectorizer

#Imports:
from typing import Dict

from newspaper import Article
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
import numpy as np
import warnings

# Ignore warning messages:
warnings.filterwarnings('ignore')

#Download packages from NLTK
nltk.download('punkt')
nltk.download('wordnet')

# Create an article object: Article can be changes.

article = Article('https://en.wikipedia.org/wiki/FC_Bayern_Munich')
article.download()
article.parse()
#Natural Language Processing
article.nlp()
corpus = article.text
print(corpus)
#Tokenize

text = corpus
# Converting the text into a list of sentences
sent_tokens = nltk.sent_tokenize(text)
# A tokenizer that divides a string into substrings by splitting on the specified string

#Remove Punctuations:
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)

# Form a list of words
# Use nltk.word_tokenize()


def lem_normalize(text):
    return nltk.word_tokenize(text.lower().translate(remove_punct_dict))
#Form a list of words and then translate with remove_punct_dict to replace all punctuations with none


#Keyword Matching for Greetings:
greeting_inputs = ["hi", "hello", "how, are you?", "good morning", "hola", "hey"]
greeting_outputs = ["namaskar", "namaste", "aham bhramastmi", "hey"]


def greet(sentence):
    for word in sentence.split():
        if word.lower() in greeting_inputs:
            return random.choice(greeting_outputs)


#Generating Response:
def response(user_response):
    robo_response = ''
    sent_tokens.append(user_response)

    #Use Tfidf Vectorizer: Scoring sent_tokens based upon frequency
    tfidf_vec = TfidfVectorizer(tokenizer=lem_normalize, stop_words='english')
    tfidf = tfidf_vec.fit_transform(sent_tokens)

    #Finding Cosine Similarity between tfidf[-1] and other words in tfidf as tfidf[-1] is the user's response itself:
    #vals = cosine_similarity of scent_tokens[[index=-1]]
    vals = cosine_similarity(tfidf[-1], tfidf)

    #Sort this list to find the sentence closest to the query:
    #Argsort will help us find the index in sent_tokens of the second last sentence in vals
    idx1 = vals.argsort()
    idx = idx1[0][-2]

    #flat = vals i.e. a list of a single list would be converted to just a single list
    flat = vals.flatten()
    flat.sort()
    score = flat[-2]

    #To check if the answer to the query even exits.
    if score == 0:
        robo_response=robo_response+"Ask me about Bayern Munchen."
    else:
        robo_response = robo_response + sent_tokens[idx]

    sent_tokens.remove(user_response)
    return robo_response


flag = True
print("BayernBot: Ask me anything about FC Bayern Munich "
      "If you want to exit, type Bye!")
while flag:
    user_response = input()
    user_response=user_response.lower()
    if user_response != 'bye':
        if user_response == 'thanks' or user_response == 'thank you':
            flag = False
            print("DOCBot: You're welcome !")
        else:
            if greet(user_response):
                print("BayernBot: " + greet(user_response))
            else:
                print("BayernBot: " + response(user_response))
    else:
        flag = False
        print("DOCBot: Chat with you later !")

