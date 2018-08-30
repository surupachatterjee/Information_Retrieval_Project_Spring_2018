import math
import operator
import traceback

lambda_value = 0.35                  # Given. 
neg_lambda_value = 1 - lambda_value

# Set as path of file containing term count for each documents.
path_unigram_term_count = '../../Dataset/Indexer_Files/unigram_terms.txt' 

# Set as path of file containing df for unigrams.
path_unigram_df = '../../Dataset/Indexer_Files/unigram_df.txt' 

# Set as path of file containing inverted index for unigrams.
path_inverted_index = '../../Dataset/Indexer_Files/inverted_index_unigram.txt'

# Set as path for file containing all search queries. 
queries_file = '../../Dataset/processed_queries.txt'  

# Set as path of file containing tf for unigrams.
path_unigram_tf = '../../Dataset/Indexer_Files/unigram_tf.txt' 


dict_term_unigram_df = {} # Dictionary to store uni-gram dfs.
dict_unigram_terms = {} # Dictionary to store uni-gram terms.
dict_unigram_inverted_index = {} # Dictionary to store inverted index for uni-grams.
dict_term_unigram_tf = {} # Dictionary to store the number of occurences of a term in the given corpus.

# calculate average document length for given corpus.
def corpus_size():
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

C = corpus_size()

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

# calculate number of times a query word occurs in the collection of documents.
def calculate_cfi():
    f = open(path_unigram_tf,'r+')
    data = []
    lines = f.readlines()
    for line in lines:
        data.append(line.strip())
    for line in data:
        temp = line.split(":")
        term = temp[0].strip()
        dict_term_unigram_tf[term] = temp[1]
    f.close()

calculate_cfi()

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

# calculate QML_35 score for each docoument for the given query.
def calculate_score(query,doc_id,query_id):
    terms_in_query = query.split()
    score = 1
    for term_in_query in terms_in_query:
        try:
            D = dict_unigram_terms[doc_id]
            if term_in_query in dict_term_unigram_tf :
                num = dict_term_unigram_tf[term_in_query].split(":")
            else:
                num = "0"
            cfi = int(num[-1])
            str_fi = get_fi(term_in_query,doc_id)
            if(isinstance(str_fi, str)):
                fi = float(str_fi.strip(")"))
            else:
                fi = 0
            exp1 = neg_lambda_value * (fi/D)
            exp2 = lambda_value * (cfi/C)
            temp_score = exp2 + exp1
            if temp_score > 0:
                temp_score = math.log(temp_score)
            score += temp_score
        except Exception as e:
            print(traceback.format_exc())
            pass
    return score 

# Get the score for each document and write it in a file.
def query_likelihood_35(query,query_id):
    rank = 0;
    QLM_35_dict = {}
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
        QLM_35 = calculate_score(query,x,query_id)
        QLM_35_dict.update({x:QLM_35})
        
    sorted_dict = sorted(QLM_35_dict.items(), key=operator.itemgetter(1))
    ranked_data = sorted_dict[::-1][0:100]
    
    file = open("Query_Likelihood_Model_0.35_Ranking.txt",'a')
    file.write(str("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"+"\n"))
    file.write("Query : "+str(queryStr)+"\n \n")
    for key,value in ranked_data:
        rank+=1;
        temp_str = str(query_id) + " " + "Q0" + " " + " " + str(key) + " " + str(rank) + " " + str(value) + " " + "QLM35" + "\n"
        file.write(temp_str +"\n")
    file.write(str("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"+"\n"))
    file.close()

# Read queries from a file and calculate QML_35 ranking for all given queries.
def main_program():

    try:
        query_id = 0
        f = open(queries_file,'r+')
        lines = f.read()
        query = ""
        queries = lines.split(",")

        for each_query in queries:
            each_query = each_query.replace("\n"," ")
            query = each_query.split(":")
            if(len(query) > 1):
                query_id = query[0].replace(" ","")
                query_likelihood_35(query[1],query_id)
        f.close()
        
    except Exception as e:
            print(traceback.format_exc())
            pass
 
# call main function
main_program()



