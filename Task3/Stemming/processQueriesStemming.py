from bs4 import BeautifulSoup
import re
import string

#Set as location to store all the processed queries.
processed_queries_file = '../../Dataset/processed_queries_stemmed.txt'

#Set as location of unprocessed queries file which are to be used for processed queries file.
unprocessed_queries_file = '../../Dataset/cacm_stem.query.txt'


def get_processed_queries(fileName,handle_punctuations,handle_casefold):
	with open(unprocessed_queries_file, 'r') as file:
		data = file.read().split("\n")

	queries = []

	query_id = 0
	for line in data:
		if line != "":
			query_id = query_id + 1
			query = str(query_id) + ":" + line
			query = query.lstrip()
			query = query.rstrip()
			query = query + ",\n"
			queries.append(query)

	# To write processed queries to file.
	f = open(processed_queries_file, 'w',encoding = 'utf-8')
	for query in queries:
		f.write(query)
	f.close()


def main () :
	#Option to handle case-folding, set as 'False' if case-folding is not required.
	handle_casefold = False

	#Option to handle punctuations, set as 'False' to retain all the punctuations.
	handle_punctuations = False

	get_processed_queries(unprocessed_queries_file,handle_punctuations,handle_casefold)


if __name__ == "__main__":
	main()