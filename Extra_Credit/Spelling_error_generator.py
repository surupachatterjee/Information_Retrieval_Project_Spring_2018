import traceback
import random
from random import randint

query_list ={} # contains the query id and the query


# fetch the processed queries in a dictionary
def populate_query_list(queries_file):
    try:
        f = open(queries_file, 'r+')
        lines = f.read()
        queries = lines.split(",")
        for each_query in queries[:len(queries) - 1]:
            each_query = each_query.replace("\n", " ")
            query = each_query.split(":")
            query_list[query[0].strip()] = query[1].lstrip().rstrip()
    except Exception as e:
        print(traceback.format_exc())
        pass

# creates a shuffling in the terms
def error_generator(word):
    num = 0
    print(word)

    if len(word) <= 6:
        return word
    elif (len(word) > 6) and (len(word) <= 10):
        num = 2
    elif (len(word) > 10) and (len(word) <= 14):
        num = 4
    elif len(word) > 14:
        num = 6

    index = random.sample(range(1, len(word)-2), num)
    temp = list(word)
    if len(index) == 2:
        temp[index[0]], temp[index[1]] = temp[index[1]], temp[index[0]]
    elif len(index) == 4:
        temp[index[0]], temp[index[1]] = temp[index[1]], temp[index[0]]
        temp[index[2]], temp[index[3]] = temp[index[3]], temp[index[2]]
    elif len(index) == 6:
        temp[index[0]], temp[index[1]] = temp[index[1]], temp[index[0]]
        temp[index[2]], temp[index[3]] = temp[index[3]], temp[index[2]]
        temp[index[4]], temp[index[5]] = temp[index[5]], temp[index[4]]
    new_word = ''.join(temp)

    return new_word


# generate the spelling error in the list and returns a list of words with
# spelling mistakes
def generate_spelling_error(query):
	query_word_list = query.split()
	#print(query + " : " + str(len(query_word_list)))
	sorted_query_word_list = sorted(query_word_list,key=len,reverse=True)
	query_length = len(query_word_list)
	print(query + ": " + str(len(query_word_list)))
	random_num = round(random.uniform(0.0, 0.4),1)
	num_of_words_to_error = round(query_length * random_num)
	print(num_of_words_to_error)
	for term in sorted_query_word_list[0:num_of_words_to_error]:
		position_of_term_in_list = query_word_list.index(term)
		mispelled_word = error_generator(term)
		query_word_list.remove(term)
		query_word_list.insert(position_of_term_in_list,mispelled_word)
	new_query = " ".join(query_word_list)
	print(new_query)
	return new_query


# Reads the processed_queries file and calls the spell error generator
def start():
	populate_query_list("../Dataset/processed_queries.txt")
	spelling_error_query_file_path = "../Dataset/spelling_error_queries.txt"
	spell_err_file = open(spelling_error_query_file_path,'w')
	for query_id,query in query_list.items():
		new_query = generate_spelling_error(query)
		spell_err_file.write(query_id + ":" + new_query +",\n")
	spell_err_file.close()


# call
start()
