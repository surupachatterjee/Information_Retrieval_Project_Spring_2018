import os.path
import traceback
import math
from BM25_Model import main_program
from generate_files import *

query_list = {}             # contains the queryid and its corresponding query
#relevance_list = {}
uni_gram_index = {}         # unigram index
bm25_rankings = {}          # results of bm25 rankings as to be considered relevant
#dict_query_documents = {}
common_words =[]            # contains stopwords

# popolates the dictionary queury_list that contains query_id and corresponding query
def populate_query_list(queries_file):
    try:
        f = open(queries_file, 'r+')
        lines = f.read()
        queries = lines.split(",")
        # print(len(queries))
        for each_query in queries[:len(queries) - 1]:
            each_query = each_query.replace("\n", " ")
            query = each_query.split(":")
            query_list[query[0].strip()] = query[1].lstrip().rstrip()
    except Exception as e:
        print(traceback.format_exc())
        pass

# populates the dictionary uni_gram_index that contains the term and the inverted list
def generate_index_from_file(file_name):
    with open(file=file_name,
              mode="r",
              encoding="utf-8",
              errors="UnicodeDecodeError") as index_file:
        index_line = index_file.readline().rstrip("\n")
        while index_line:
            index_terms = index_line.split("---->")
            term_files_frequencies = index_terms[1].split("),(")
            files_frequencies = {}
            
            for term_files_frequency in term_files_frequencies:
                file_frequency = term_files_frequency.lstrip(
                    "(").rstrip(")").split(",")
                files_frequencies[file_frequency[0].strip(
                    " ")] = int(file_frequency[1].strip(" "))
            #if index_terms[0] not in common_words:
            uni_gram_index[index_terms[0]] = files_frequencies
            #else:
            #    print(index_terms[0] + "--->" + str(files_frequencies))
            index_line = index_file.readline().rstrip("\n")
        index_file.close()

# populates the dictionary bm25_rankings that contains the query_id and correspoding
# list of documents that appear in bm25 rankings for this query
def load_bm25_ranking_docs(filename):
    file = open(filename, 'r')
    filelines = file.readlines()
    filelines = [line.strip() for line in filelines]
    filelines = [x for x in filelines if x]
    for fileline in filelines:
        if not (fileline.startswith('Query')
                or fileline.startswith('^')):
            line_cols = fileline.split(" ")
            query_id = line_cols[0]
            if query_id not in bm25_rankings.keys():
                bm25_rankings[query_id] = [line_cols[3]]
            else:
                doc_list = bm25_rankings[query_id]
                doc_list.append(line_cols[3])
                bm25_rankings[query_id] = doc_list
    # print(bm25_rankings)

# contains the term frequency for each term in the given query
def generate_query_vector(query):
    query_term_vector = {}
    for term in query.split():
        #print(term)
        if term not in query_term_vector.keys():
            query_term_vector[term] = 1
        else:
            #print("in else " + str(query_term_vector[term]))
            query_term_vector[term] += 1

    for term in uni_gram_index.keys():
        if term not in query_term_vector.keys():
            query_term_vector[term] = 0
    return query_term_vector

# generates the relevant/non relevant document set as per the given type
def generate_doc_vector(rel_count, type, query_id):
    document_vector = {}
    if type == 'rel':
        start_index = 0
        end_index = rel_count
    else:
        start_index = rel_count
        end_index = len(bm25_rankings[query_id])
        
    for document in bm25_rankings[query_id][start_index:end_index]:
        for term, doc_term_frq_list in uni_gram_index.items():
            if document in doc_term_frq_list.keys():
                #print(term + " : " + document + " : " + str(doc_term_frq_list[document]))
                if document not in document_vector.keys():
                    document_vector[term] = doc_term_frq_list[document]
                else:
                    document_vector[term] += doc_term_frq_list[document]
    
    for term in uni_gram_index.keys():
        if term not in document_vector.keys():
            document_vector[term] = 0
    
    return document_vector


# def read_relevance_file(rel_filename):
#     rel_doc_list = []
#     rel_file = open(rel_filename, "r")
#     lines = rel_file.readlines()
#     for line in lines:
#         l = line.replace('\n', "").split(" ")
#         query_id = l[0]
#         if query_id not in relevance_list.keys():
#             relevance_list[query_id] = [l[2]]
#         else:
#             rel_doc_list = relevance_list[query_id]
#             rel_doc_list.append(l[2])
#             relevance_list[query_id] = rel_doc_list

# calculates the magnitude of the document vector
def calculate_magnitude(doc_vector):
    magnitude = 0
    for term, frequency in doc_vector.items():
        magnitude += float(frequency**2)
    magnitude = float(math.sqrt(magnitude))
    return magnitude

# processes a query to enrich into a new query
def process_query(relevant_doc_count,query_id,query):
    term_weights = {}
    new_query =""#= query.lower()
    query_vector = generate_query_vector(query.lower())
    #print(query_vector)
    rel_doc_vector = generate_doc_vector(relevant_doc_count, 'rel', query_id)
    rel_magnitude = calculate_magnitude(rel_doc_vector)
    print("Relevant Magnitude : " + str(rel_magnitude))
    #print(rel_doc_vector)
    non_rel_doc_vector = generate_doc_vector(relevant_doc_count, 'non-rel', query_id)
    non_rel_magnitude = calculate_magnitude(non_rel_doc_vector)
    print("Non Relevant Magnitude : " + str(non_rel_magnitude))
    #print(non_rel_doc_vector)
    for term in uni_gram_index.keys():
        #print(term)
        if(not term.isdigit()):
            term_weights[term] = query_vector[term] + ((0.75/rel_magnitude) * rel_doc_vector[term]) - ((0.15/non_rel_magnitude) * non_rel_doc_vector[term])
    sorted_term_weights = sorted(term_weights.items(),
                                key=lambda score: score[1],
                                reverse=True)
    #print(len(common_words))


    query_lst = query.lower().split(" ")
    for query_term in query_lst:
        if query_term not in common_words:
            new_query += query_term + " "
    new_query = new_query.lstrip().rstrip()
    print(new_query)

    modified_query = ''
    for i in range(10):
        term,weight = sorted_term_weights[i]
        if term in new_query and term not  in common_words:
            for i in range(new_query.count(term)):
                modified_query += " " + term
        else:
            modified_query += " " + term
    return modified_query

# popoulates the list of common_words in the corpus
def fetch_common_words(filename):
    global common_words
    file = open(filename,'r')
    common_words = file.readlines()
    for i in range(len(common_words)):
        common_words[i] = common_words[i].strip('\n')
    #for term in common_words:
        #if term in uni_gram_index.keys():
            # print(term)
            #print(term + " ---->  " + str(uni_gram_index[term]))


# caller method
def start():

    relevant_doc_count = 5
    current_path = os.path.dirname(os.path.dirname(os.getcwd()))
    result_path = current_path + "/Task2/Results"
    fetch_common_words(current_path + '/Dataset/common_words.txt')
    #print(common_words)
    # print(result_path)
    delete_directory(result_path)
    create_project_dir(result_path)

    enriched_query_filename = os.path.join(result_path,'enriched_queries.txt')

    # print(enriched_query_filename)
    populate_query_list(current_path + '/Dataset/processed_queries.txt')
    # print(query_list)
    # read_relevance_file(current_path + '/Dataset/cacm.rel.txt')
    generate_index_from_file(current_path + '/Dataset/Indexer_Files/inverted_index_unigram.txt')
    # print(uni_gram_index)
    load_bm25_ranking_docs(current_path + '/Task1/BM25/BM25_Ranking.txt')


    counter = 0;
    delete_file(enriched_query_filename)
    f = open(enriched_query_filename, 'w')
    for query_id, query in query_list.items():
        #print(query.count('system'))
        enriched_query = process_query(relevant_doc_count,query_id,query)
        f.write(query_id + ":" + enriched_query +",\n")
        print(str(counter) + " : " + query + " \n" + enriched_query)
        counter += 1
        #if counter > 5:
         #   break
    f.close()
    # calll the BM25 baseline model to re rank the documents
    main_program(enriched_query_filename,result_path)

start()
