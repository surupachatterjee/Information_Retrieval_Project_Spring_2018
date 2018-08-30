import math
import operator
import traceback
import os

N = 0       # Number of documents in corpus.
b = 0.75    # Given.
k1 = 1.2    # Given.
k2 = 100    # Given.
R = 0       # Given.
ri = 0      # Given.

# Set as path of file containing term count for each documents.
path_unigram_term_count = '../../../Dataset/Indexer_Files_with_stemming/unigram_terms.txt'

# Set as path of file containing df for unigrams.
path_unigram_df = '../../../Dataset/Indexer_Files_with_stemming/unigram_df.txt'

# Set as path of file containing inverteIndexer_Files_with_stoppingd index for unigrams.
path_inverted_index = '../../../Dataset/Indexer_Files_with_stemming/inverted_index_unigram.txt'

# Set as path for file containing all search queries.
queries_file = '../../../Dataset/processed_queries_stemmed.txt'

# Set as path for file relevance information.
relevance_info = '../../../Dataset/cacm.rel.txt'

# Set as path for directory containing the corpus.
corpus = '../../../Dataset/cleaned_files_with_stemming'

# Set as True whenever we do retrieval after query enrichment (using psuedo-relevance feedback).
query_enrichment = False

dict_term_unigram_df={} # Dictionary to store uni-gram dfs.
dict_unigram_terms={} # Dictionary to store uni-gram terms.
dict_unigram_inverted_index={} # Dictionay to store inverted index for uni-grams.

# calculate the number of documents in given corpus.
def total_document_count():
    global N
    files = os.listdir(corpus)
    N = len(files)

total_document_count()

# calculate average document length for given corpus.
def total_document_length():
    sum = 0
    string_entry=[]
    f = open(path_unigram_term_count,'r+')
    lines = f.readlines()
    for line in lines:
        string_entry.append(line.strip())
    for line in string_entry:
        temp = line.split(":")
        dict_unigram_terms.update({temp[0]:int(temp[1])})
        sum+=int(temp[1])
    f.close()
    return sum

avdl = (float (total_document_length())/float(N))

# find all the relevant documents for a given query id.
def relevance_doc_query(query_id):
    try:
        rDoc_ids = []
        file = open(relevance_info,'r')
        for line in file.readlines():
            params = line.split()
            # If the document is relevant for given query id, add it to relevant document list.
            if params and (params[0] == str(query_id)):
                rDoc_ids.append(params[2])
        file.close()
        return rDoc_ids
    except Exception as e:
        print(traceback.format_exc())
        pass

# find count of relevant documents containing the given query term.
def relevance_doc_term(term_in_query, dict_term_unigram_df, relevance_docIds):
    try:
        ri = 0
        if term_in_query in dict_term_unigram_df:
            documents = dict_term_unigram_df[term_in_query].split(":")[0].split(",")
            for document in documents:
                 if document in relevance_docIds:
                          ri+=1
        return ri
    except Exception as e:
        print(traceback.format_exc())
 
# calculate frequency of each term in ith document and add it in the dictionary.
def calculate_fi():
    f = open(path_inverted_index,'r+')
    lines = f.readlines()
    for line in lines:
        temp = line.split("---->")
        tf = temp[1].strip()
        dict_unigram_inverted_index.update({temp[0]:tf})
    f.close()

calculate_fi()

# calculate number of documents which contains terms from the query.
def calculate_ni():
    f = open(path_unigram_df,'r+')
    data = []
    lines = f.readlines()
    for line in lines:
        data.append(line.strip())
    for line in data:
        temp = line.split(":")
        term = temp[0].strip()
        df = temp[2].split(",")
        rest_temp = temp[1]+":"+df[0]
        dict_term_unigram_df[term]=rest_temp
    f.close()
    
calculate_ni()

# Get term frequency in the document for the given term.
def get_fi(term,doc_id):
    if term in dict_unigram_inverted_index:
        postings = dict_unigram_inverted_index[term]
        doc_ids = postings.split(",")
        for index, val in enumerate(doc_ids):
            if doc_id == val[1:]:
                fi = doc_ids[index + 1]
                return fi
    else :
        return "0"

# calculate BM25 score for each docoument for the given query.
def calculate_score(query,doc_id,query_id):
    terms_in_query = query.split()
    bm25_score=0
    relevance_docIds = relevance_doc_query(query_id)
    # R = len(relevance_docIds) # Total number of relevant documents for query.
    for term_in_query in terms_in_query:
        try:
            dl = dict_unigram_terms[doc_id]
            K = k1 * ((1-b) + (b * (dl/avdl)))
            # ri = relevance_doc_term(term_in_query, dict_term_unigram_df, relevance_docIds)
            if term_in_query in dict_term_unigram_df:
                num = dict_term_unigram_df[term_in_query].split(":")
            else:
                num = "0"
            ni = int(num[-1])
            str_fi = get_fi(term_in_query,doc_id)
            if(isinstance(str_fi, str)):
                fi = float(str_fi.strip(")"))
            else:
                fi=0
            qfi = terms_in_query.count(term_in_query)
            exp1 = (((float(ri) + 0.5) 
                / (float(R) - float(ri) + 0.5)) 
            / ((float(ni) - float(ri) + 0.5) 
                / (float(N) - float(ni) - float(R) + float(ri) + 0.5)))
            exp2 = math.log(exp1)
            exp3 = (((float(k1) + 1) * float(fi)) / (float(K) + float(fi)))
            exp4 = (((float(k2) + 1) * float(qfi)) / (float(k2) + float(qfi)))
            temp_score = exp2*exp3*exp4
            bm25_score+=temp_score
        except Exception as e:
            print(traceback.format_exc())
            pass
    return bm25_score

# Get the score for each document and write it in a file.
def calculate_BM25(query,query_id,query_enrichment, result_folder_path):
    rank = 0;
    BM25_dict = {}
    terms_in_query = query.split()
    doc_list = []
    queryStr = ""
    for term in terms_in_query:
        queryStr+=term+" "
        if term in dict_term_unigram_df.keys():
            str1 = dict_term_unigram_df[term]
            str2 = str1.split(",")
            for x in str2[:-1]:
                if x.strip() not in doc_list:
                    doc_list.append(x.strip())

    for x in doc_list:
        BM25_score = calculate_score(query,x,query_id)

        BM25_dict.update({x:BM25_score})
        
    sorted_dict = sorted(BM25_dict.items(), key=operator.itemgetter(1))
    ranked_data = sorted_dict[::-1][0:100]
    
    if query_enrichment :
        fileName = os.path.join(result_folder_path, "BM25_Ranking_After_Query_Enriched.txt") 
    else:
        fileName = os.path.join(result_folder_path, "BM25_Ranking_with_stemming.txt")
     
    file = open(fileName,'a')
    file.write(str("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"+"\n"))
    file.write("Query : "+str(queryStr)+"\n \n")
    for key,value in ranked_data:
        rank+=1;
        temp_str = str(query_id) + " " + "Q0" + " " + " " + str(key) + " " + str(rank) + " " + str(value) + " " + "BM25_Stem" + "\n"
        file.write(temp_str +"\n")
    file.write(str("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"+"\n"))
    file.close()

# Read queries from a file and calculate BM25 ranking for all given queries.
def main_program(queries_file, query_enrichment,result_folder_path):
    try:
        f = open(queries_file,'r+')
        lines = f.read()
        query = ""
        queries = lines.split(",")

        for each_query in queries:
            each_query = each_query.replace("\n"," ")
            query = each_query.split(":")
           
            if(len(query) > 1):
                query_id = query[0].replace(" ","")
                calculate_BM25(query[1],query_id,query_enrichment,result_folder_path)
        f.close()
    except Exception as e:
            print(traceback.format_exc())
            pass
 
# call main function
main_program(queries_file, query_enrichment, "")



