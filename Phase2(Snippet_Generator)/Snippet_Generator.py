import traceback
from collections import defaultdict
import os
import re

# Set as name of file where you want to store the snippet generation results.
snippet_results_file = 'Snippet_Generator_Results.html' 

# Set as path for file containing all search queries. 
queries_file = '../Dataset/processed_queries.txt'  

# Set as path for directory containing the corpus. 
corpus = '../Dataset/cleaned_files'  

# Set as path for file containing all the stop words.
stop_file = '../Dataset/common_words.txt'

# Set as path for file containing ranking results of any retrieval model
# for which snippet generation needs to done.
ranking_file = '../Task1/BM25/BM25_Ranking.txt'

stop_list = list() # Stores the stop words, which are to be ignored during query term highlighting. 

dict_query_documents = defaultdict(list)

# Get top 100 results for all the given queries.
def top_100_documents(file_name):
    file = open(file_name, 'r+')
    lines = file.readlines()
    lines = [line.strip() for line in lines]
    global dict_query_documents
    for each_doc in lines:
        doc_rank_details = each_doc.split(" ")
        # print(doc_rank_details)
        if len(doc_rank_details) > 1:
            query_id = doc_rank_details[0]
            doc_id = doc_rank_details[3]
            # print(query_id)
            # Add all the doc ids for a given query.
            dict_query_documents[query_id].append(doc_id)
    # print(dict_query_documents)
    file.close()

# Generates list of stop words to be ignored during query term highlighting. 
# def generate_stop_list():
#     file = open(stop_file, 'r+')
#     lines = file.readlines()
#     lines = [line.strip() for line in lines]
#     global stop_list
#     for stop_word in lines:
#         stop_list.append(stop_word)
#     file.close()

# When n terms of query co-occur.
def ngram_snippet(qStr,doc_id,n):

    fileName = os.path.join(corpus, doc_id+".txt") 
    f = open(fileName, 'r+')    # Read the document.
    data = f.read()
    found_ngram = False
    snippet = "Sorry! No Useful Snippet Found."
    is_stop_word = False
    for term in range(len(qStr) - n):
        if n > 0:
            n_terms = qStr[term:(term+(n+1))]
            ngram = " ".join(n_terms)
             
        else:
            ngram = qStr[term]
             
        # If the n-gram co-occurs in the document.
        if data.find(ngram) != -1 and bool(re.findall('\\b'+ngram + '\\b', data)):
            
            matching_term = re.findall('\\b'+ ngram+ '\\b', data)
            term_start = re.search('\\b'+ ngram+ '\\b', data)
                
            # index of the found term.
            index = term_start.start()
            
            # Set as true when n-gram is found in the document.
            found_ngram = True

            # Get the terms that appear before the ngram terms.
            s_index = max(index-50, 0)

            # To get the whole term.
            if s_index != 0:
                while s_index > 0:
                    if data[(s_index - 1):s_index] not in [" ", "\n"]:
                        s_index -= 1
                    else:
                        break

            # Get the terms that appear after the ngram terms.
            e_index = min(data.index(ngram) +  len(matching_term[0]) + 50, len(data))

            # To get the whole term.
            if e_index != len(data):
                while e_index < len(data):
                    if data[e_index:(e_index + 1)] not in [" ", "\n"]:
                        e_index += 1
                    else:
                        break

            # Get terms before n-gram terms to be highlighted.
            before_qTerms = data[s_index:index]
                
            # Get n-gram terms to be highlighted.
            qTerms = data[index : (index + len(matching_term[0]))]

            # Using mark tag highlight the query terms.
            qTerms = '<mark>{}</mark>'.format(qTerms)

            # Get terms after n-gram terms.
            after_qTerms = data[(index + len(matching_term[0])):e_index]

            # Generate snippet for the given query and document.
            snippet = before_qTerms + qTerms + after_qTerms

            return found_ngram,snippet

    return found_ngram,snippet
    

# Generates snippets depending on if the terms in given query co-occur as tri, bi or uni-grams.
def generate_snippet(qStr,doc_id):
    terms_in_query = qStr.split()
    has_trigrams, s_sentence = ngram_snippet(terms_in_query,doc_id,2)
    if has_trigrams:
        return s_sentence
    has_bigrams, s_sentence = ngram_snippet(terms_in_query,doc_id,1)
    if has_bigrams:
        return s_sentence
    has_unigrams, s_sentence = ngram_snippet(terms_in_query,doc_id,0)
    if has_unigrams:
        return s_sentence
    else :
        return s_sentence

# Read queries from a file and generate snippets for all given queries.
def main_program():
    try:
        top_100_documents(ranking_file)
        f = open(queries_file,'r+')
        lines = f.read()
        query = ""
        queries = lines.split(",")
        f.close()
        f = open(snippet_results_file, 'w+', encoding = 'utf-8')
        f.write("<!DOCTYPE html>")
        for each_query in queries:
            each_query = each_query.replace("\n"," ")
            query = each_query.split(":")
           
            if( len(query) > 1):
                query_id = query[0].replace(" ","")
                qStr = query[1]
                f.write("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^<br/>")
                f.write("Query " +query_id+ " : "+qStr + " <br />")
                for doc_id in dict_query_documents[query_id]:
                    f.write("Document : " + doc_id + "<br />")
                    f.write(" {Snippet} <br />")
                    sentence = generate_snippet(qStr,doc_id)
                    f.write(str(sentence) +"<br />")
                    f.write(" {\Snippet} <br />")
                    f.write("_____________________________________________________________________________<br/>")
                    f.write("<br \>")
                f.write("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^<br/>")
        f.close()

    except Exception as e:
            print(traceback.format_exc())
            pass
 
# call main function
main_program()



