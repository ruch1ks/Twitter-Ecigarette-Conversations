#necessary for working with files
import csv
import string
import sys

#necessary for cleaning and tokenizing text
import nltk.corpus
from nltk.corpus import stopwords
from nltk.text import Text 
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer

#used for topic modeling
from nltk.corpus import wordnet as wn
import pickle
import gensim
from gensim import corpora

#accounts for variations in keywords and for twitter hashtags
juul_keywords = ['juul', 'juuls', '#juul', '#juuls']
ecig_keywords = ['ecig', 'ecigs', 'e-cig', 'ecigs', 'ecigarette', 'ecigarettes', 'e-cigarette', 'e-cigarettes', '#ecig', '#ecigs', '#e-cig', '#e-cigs', '#ecigarette', '#ecigarettes', '#e-cigarette', '#e-cigarettes']


#this method uses NLTK's concordance
#to find the surrounding context of a specific keyword
#only works with one keyword (not a list)
#takes in a filename, width of surrounding context, max number of lines, keyword, and a non-tokenized string
#saves the output to a .txt file
def find_context(filename, width, maxlines, keyword, tweets_str): 

	#NLTK has a unique tokenizer for tweets
	t = nltk.tokenize.TweetTokenizer()
	tweet_txt_obj = Text(t.tokenize(tweets_str))

	#by default concordance() prints to console
	#this reroutes the output to a file
	concordance_file = open(filename, 'w', encoding = 'utf8')
	tmpout = sys.stdout
	sys.stdout = concordance_file
	tweet_txt_obj.concordance(keyword, width, maxlines)
	concordance_file.close()
	sys.stdout = tmpout

#this method cleans strings of text
#removes stop words and punctuation
#removes additional symbols that are commonly found in tweets  
def clean_text(tweet_str):
	#remove stop words and punctuation
	#as well as common words in tweets
	#tokenize appropriately
	stop_words = set(stopwords.words('english'))
	stop_words.add('rt')
	stop_words.add('https')
	stop_words.add("'m")
	stop_words.add("``")
	stop_words.add('...')
	punctuation = set(string.punctuation)

	#it seemed necessary to tokenize tweets before cleaning them
	#otherwise punctuation, etc was left behind
	tokenized_str = nltk.tokenize.word_tokenize(tweet_str)

	stop_words_rem_str = ""
	for word in tokenized_str:
		if not word.lower() in stop_words and not word in punctuation and not word.isnumeric() and len(word) > 1:
			stop_words_rem_str = stop_words_rem_str + word.lower() + " "
	
	return stop_words_rem_str


def main():
    #reading in tweets from csv
	#deleting first entry (title)
	with open ('EcigSearch.csv', 'r', encoding = 'utf8') as f:
		reader = csv.reader(f)
		filter_list = list(reader)
		del filter_list[0]

	ecig_tweets = []
	juul_tweets = []
	ecig_tweets_str = ""
	juul_tweets_str = ""

	#other columns have irrelevant information
	#ensure tweets are written in english
	#split by e-cig versus juul
	for tweet in filter_list[:20000]:
		if(tweet[15] == 'en'):
			if any(substring in tweet[5] for substring in ecig_keywords) and any(substring in tweet[5] for substring in juul_keywords):
				ecig_tweets.append(tweet[5])
				ecig_tweets_str = ecig_tweets_str + tweet[5] + " "
				juul_tweets.append(tweet[5])
				juul_tweets_str = juul_tweets_str + tweet[5] + " "
			elif any(substring in tweet[5] for substring in ecig_keywords): 
				ecig_tweets.append(tweet[5])
				ecig_tweets_str = ecig_tweets_str + tweet[5] + " "
			elif any(substring in tweet[5] for substring in juul_keywords) : 
				juul_tweets.append(tweet[5])
				juul_tweets_str = juul_tweets_str + tweet[5] + " "

	find_context('test.txt', 80, sys.maxsize, 'juul', juul_tweets_str)
	print("done")


if __name__ == '__main__':
    main()


# ** the functions below were used for various preliminary tasks of analyzing the data ** 

#this method takes in a list and prints out the frequencies
#at which the primary keywords (juul/e-cig/etc) appear
def keyword_counts(tweet_list):

	juul_count = 0
	ecig_count = 0
	electronic_cig_count = 0
	vape_count = 0
	vaping_count = 0

	#the distinction between 'ecig' and 'electronic cigarette' was significant
	#as was the distinction between 'vape' versus 'vaping' (noun versus verb)
	for tweet in tweet_list:
		for word in tweet:
			if word in juul_keywords:
				juul_count += 1
			elif word in ecig_keywords: 
				ecig_count += 1

		electronic_cig_count = electronic_cig_count + tweet.count("electronic cigarette")
		vape_count = vape_count + tweet.count("vape")
		vaping_count = vaping_count + tweet.count("vaping")

	print("Juul: " + str(juul_count))
	print("Ecig: " + str(ecig_count))
	print("E-cig: " + str(e_cig_count))
	print("Electronic cigarette: " + str(electronic_cig_count))
	print("Vape: " + str(vape_count))
	print("Vaping: " + str(vaping_count))


#this method calculates the most frequent words 
#takes in the number of desired terms and a (cleaned) text string
#and writes the frequencies to a .txt file
def calculate_freq(clean_tweet_str, num, filename): 
	tokenized_clean_str = nltk.tokenize.word_tokenize(clean_tweet_str)

	fdist = nltk.FreqDist(tokenized_clean_str)

	#write top frequencies to a file
	with open(filename, 'w', encoding = 'utf8') as f:
	 	for word, frequency in fdist.most_common(num):
	 		f.write(u'{};{}\n'.format(word, frequency))


#this method displays the words immediately before a keyword
#it takes in a list of keywords to search for
#and a list of tokenized tweets (can be either cleaned or uncleaned)
#returns a list containing all words immediately preceding a keyword (or any variations of the keyword)
def words_before(keywords, tokenized_tweet_list): 
	words_before = []

	for token_tweet in tokenized_tweet_list:
		
		for i in range(len(token_tweet)):

	 		if(token_tweet[i].lower() in keywords):
				check out of range
				if(i - 1 > 0): 
					#words_before.append(token_tweet[i-1])

	return words_before


#see words_before
#functionality is identical 
#it returns a list of words immediately following a keyword/its variations
def words_after(keywords, tokenized_tweet_list): 
	words_after = []

	for token_tweet in tokenized_tweet_list:
		
		for i in range(len(token_tweet)):

	 		if(token_tweet[i].lower() in keywords):
			#check out of range
				if(i + 1 < len(token_tweet)): 
					words_after.append(token_tweet[i+1])

	return words_after



# #tokenize as both list and string
# t = nltk.tokenize.TweetTokenizer()
# tokenized_ecig_list = []
# tokenized_juul_list = []
# for tweet in ecig_tweets:
# 	tokenized_ecig_list.append(t.tokenize(tweet))
# search_ecig_obj = Text(t.tokenize(ecig_tweets_string))
# search_juul_obj = Text(t.tokenize(juul_tweets_string))





# def get_lemma(word):
# 	lemma = wn.morphy(word)
# 	if lemma is None:
# 		return word 
# 	else: 
# 		return lemma

# stop_words_rem_juul = ""
# juul_tweets_tokens = nltk.tokenize.word_tokenize(juul_tweets_string)
# for word in juul_tweets_tokens:
# 	if not word.lower() in stop_words and not word in punctuation and not word.isnumeric() and len(word) > 3:
# 		stop_words_rem_juul = stop_words_rem_juul + word.lower() + " "
# edited_juul_tokens = nltk.tokenize.word_tokenize(stop_words_rem_juul)

# lemma_tokens = [get_lemma(token) for token in edited_juul_tokens]

# dictionary = corpora.Dictionary(lemma_tokens.split())
# corpus = [dictionary.doc2bow(token) for token in lemma_tokens.split()]

# pickle.dump(corpus, open('corpus.pkl', 'wb'))
# dictionary.save('dictionary.gensim')

# NUM_TOPICS = 5
# ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
# ldamodel.save('model5.gensim')

# topics = ldamodel.print_topics(num_words=4)
# for topic in topics:
  #  print(topic)


#***************unused***************



#words in similar context
#similar_file = open('e-cigaretteSimilarSearch.txt', 'w', encoding = 'utf8')
#tmpout1 = sys.stdout
#sys.stdout = similar_file
#search_text_obj.similar('e-cigarette', sys.maxsize)



#search = Text(nltk.corpus.gutenberg.words('EcigSearch.txt'))

