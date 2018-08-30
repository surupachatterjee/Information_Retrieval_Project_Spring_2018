import requests
from bs4 import BeautifulSoup
import os
import re
import string
import operator

#Set as location to store all the processed queries.
processed_queries_file = '../../Dataset/processed_queries_stopped.txt'

#Set as location of unprocessed queries file which are to be used for processed queries file.
unprocessed_queries_file = '../../Dataset/cacm.query.txt'

# Stop words list
stop_list_file = '../../Dataset/common_words.txt'
stop_words_list = []

def get_processed_queries(fileName, handle_punctuations, handle_casefold, handle_stopping):
	file = open(fileName, 'r+', encoding = 'utf-8')
	data = file.read()
	soup = BeautifulSoup(data,'html.parser')

	# To remove formualae present in a document
	for formulae in soup('semantics'):
		formulae.decompose()
	queries = []

	# Consider text between DOC tags only
	for data in soup.find_all(['doc']):

		# Regex to remove extra spaces between the words.
		raw_query = re.sub('\s\s+', ' ', data.text)
		# print(raw_query)
		# print("******")
		# Split the query and query id.
		query_id = int(re.sub('\s\s+', ' ', raw_query[:3]))

		# Regex to remove extra spaces between the query id and query.
		if(query_id > 9):
			raw_query = re.sub('\s\s+', ' ', raw_query[4:])
		else :
			raw_query = re.sub('\s\s+', ' ', raw_query[3:])

		# Regex to remove "," , "." and " ' " everywhere except if in between numbers.
		raw_query = re.sub('(?<=[^0-9])[.,\']|[.,\'](?=[^0-9])', '', raw_query)
		# For handling punctuations using string.punctuation.
		if(handle_punctuations):
			intab =  "\"#!$%&()*+/:;<=>?@[\]_`{|}^~?\'"
			outtab = "                              "
			raw_query = raw_query.translate(str.maketrans(intab, outtab, string.punctuation))

		# For handling case-folding using lower() to convert all the text in lower-case.
		if(handle_casefold):
			raw_query = raw_query.lower()

		token = raw_query.split(" ")

		if handle_stopping:
			stopped_query = ""
			for words in token:
				if words not in stop_words_list:
					stopped_query = stopped_query + words + " "
			stopped_query = stopped_query.strip()
			query = str(query_id) + ":" + stopped_query
		else:
			query = str(query_id) + ":" + raw_query

		query = query.lstrip()
		query = query.rstrip()
		query = query+",\n"

		queries.append(query)
	# To write processed queries to file.
	f = open(processed_queries_file, 'w',encoding = 'utf-8')
	for query in queries:
		f.write(query)
	f.close()


# Function to read stop words from the given file and storing them in a list
def read_stop_list_from_file(filename):
	with open(filename, 'r') as file:
		for line in file:
			line = line.strip()
			stop_words_list.append(line)
	print(stop_words_list)


def main () :
	#Option to handle case-folding, set as 'False' if case-folding is not required.
	handle_casefold = True

	#Option to handle punctuations, set as 'False' to retain all the punctuations.
	handle_punctuations = True

	handle_stopping = True

	read_stop_list_from_file(stop_list_file)
	get_processed_queries(unprocessed_queries_file,handle_punctuations,handle_casefold, handle_stopping)


if __name__ == "__main__":
	main()