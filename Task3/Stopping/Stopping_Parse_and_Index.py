from bs4 import BeautifulSoup
import os
import re
import string
import operator

# Set as location of raw html text files which are to be used for generating a clean corpus.
raw_files_path = '../../Dataset/raw_html_text_files'

# Set as location of cleaned corpus which are to be used for generating inverted lists for n-grams.
cleaned_files_path = '../../Dataset/cleaned_files_with_stopping'

# Set as location to store the files consisting of the total term-count (with duplicates)
# of each document in the cleaned corpus.
term_count = '../../Dataset/Indexer_Files_with_stopping'

# Set as location to store the files consisting of the n-grams index generated of
# each document in the cleaned corpus.
inverted_index_unigrams = '../../Dataset/Indexer_Files_with_stopping'

# Set as location to store the files consisting of term-frequency table for all the
# documents in the cleaned corpus.
unigram_tf = '../../Dataset/Indexer_Files_with_stopping'

# Set as location to store the files consisting of document-frequency table for all
# the documents in the cleaned corpus.
unigram_df = '../../Dataset/Indexer_Files_with_stopping'

# Dictionaries to store the inverted indexes and terms generated.
unigram = {}

# Dictionaries to store the term count for each document.
unigram_terms = {}

# Stop words list
stop_list_file = '../../Dataset/common_words.txt'
stop_words_list = []


# Function to generate uni-gram tokens.
def unigram_index_with_stopping(word_list, file_name):
    term_count = 0    # For storing the term-count for entire document (with duplicates).
    for each_word in word_list:
        term_count += 1
        if each_word not in stop_words_list:
            if each_word in unigram:
                # Check if the file is exists in the dictionary.
                # Add file along with the term, if non-existent.
                if file_name[0] not in unigram[each_word]:
                    unigram[each_word].update({file_name[0]: 1})
                else:
                    # If the file exists, updated term-count for the term.
                    unigram[each_word][file_name[0]] += 1
            else:
                unigram[each_word] = {file_name[0]: 1}
    unigram_terms.update({file_name[0]:str(term_count)})


# Function to generate uni-gram tokens.
def unigram_index_without_stopping(word_list, file_name):
    term_count = 0    # For storing the term-count for entire document (with duplicates).
    for each_word in word_list:
        term_count += 1
        if each_word in unigram:
            # Check if the file is exists in the dictionary.
            # Add file along with the term, if non-existent.
            if file_name[0] not in unigram[each_word]:
                unigram[each_word].update({file_name[0]: 1})
            else:
                # If the file exists, updated term-count for the term.
                unigram[each_word][file_name[0]] += 1
        else:
            unigram[each_word] = {file_name[0]: 1}
    unigram_terms.update({file_name[0]:str(term_count)})


# Function to generate term frequency table for uni-grams.
def create_tf(any_dictionary, fileName):
    dict_tf ={}
    for key in any_dictionary.keys():
        sum_tf = 0
        dict_temp = any_dictionary[key]
        for each_file in dict_temp.keys():
            sum_tf = sum_tf + dict_temp[each_file]

        dict_tf.update({key:sum_tf})

    dict_tf_temp = sorted(dict_tf.items(), key=operator.itemgetter(1),reverse = True)

    f = open(fileName, 'w')
    f.write("term:"+" tf "+"\n")
    write_to = ''
    for key,value in dict_tf_temp:
        write_to += key + ':' + str(value)+'\n'

    f.write(write_to)
    f.close()


# Function to generate df tables for uni-grams.
def create_df(any_dictionary, fileName):
   
    dict_df = sorted(any_dictionary.items(), key=operator.itemgetter(0))
    f = open(fileName, 'w')
    f.write("term : "+" docIDs : "+" df "+"\n")
    for key, value in dict_df:
        term = key
        docIds = ''
        df = len(value)
        k = 0        # Append ',' only if k < count.
        for each_value in value.keys():
            k += 1
            if k < df:
                docIds += each_value + ","
            else:
                docIds += each_value

        f.write(term + ":" + docIds + ":" + str(df) + ",\n")

    f.close()


def create_term_count_dict(any_dictionary, fileName):
    f = open(fileName, 'w')
    keys = list(any_dictionary.keys())
    values = list(any_dictionary.values())
    for i in range(0, len(keys)):
        f.write(keys[i]+":"+str(values[i]) + "\n")
    f.close()


# Function to generate inverted index files for uni-grams with term, docId and
# term positions in each document [term :(docId,term position)].
def create_index_with_term_pos(any_dictionary, fileName):
    dict_term_pos = sorted(any_dictionary.items(), key=operator.itemgetter(0))
    f = open(fileName, 'w')
    f.write("term : "+" (docIDs : "+" termPos) "+"\n")
    for key, value in dict_term_pos:
        term = key
        docs = ''
        dict_index = any_dictionary[key]
        count = len(value)
        k = 0       # Append ',' only if k < count.
        for each_key in dict_index.keys():
            k += 1
            if k < count:
                docs += "(" + each_key + ":" + str(dict_index[each_key]) + ")" + ","
            else:
                docs += "(" + each_key + ":" + str(dict_index[each_key]) + ")"

        f.write(term + ":" + docs + ",\n")

    f.close()


# Function to generate inverted index files for uni-grams.
def create_inverted_index_file(any_dictionary, fileName):
    f = open(fileName, 'w')
    keylist = any_dictionary.keys()
    keylist = sorted(keylist)
    for key in keylist:
        term = key
        dict_index = any_dictionary[key]
        df = len(dict_index)
        k = 0
        docs = ''
        for each_key in dict_index.keys():
            k += 1
            if k < df:
                docs += "(" + each_key + "," + str(dict_index[each_key]) + ")" + ","
            else:
                docs += "(" + each_key + "," + str(dict_index[each_key]) + ")"

        f.write(term+"---->"+docs+"\n")

    f.close()


def create_inverted_index(dir_nam, handle_stopping):

    files = os.listdir(dir_nam)

    if handle_stopping:
        read_stop_list_from_file(stop_list_file)

    for eachFile in files:
        file_name = eachFile.split(".txt")
        print("Generated index for : " + eachFile)
        complete_file_name = os.path.join(dir_nam, eachFile) 
        file = open(complete_file_name, 'r+')
        data = file.read()
        word_list = data.split(None)
        # To create inverted index for uni-grams.
        if handle_stopping:
            unigram_index_with_stopping(word_list, file_name)
        else:
            unigram_index_without_stopping(word_list, file_name)

    # To create tf and df for uni-grams.
    create_tf(unigram, os.path.join(unigram_tf,"unigram_tf.txt"))
    create_df(unigram, os.path.join(unigram_df, "unigram_df.txt"))

    # To create files containing number of terms in each file.
    create_term_count_dict(unigram_terms, os.path.join(term_count,"unigram_terms.txt"))
    
    # To creates file containing inverted index for uni-grams.
    create_inverted_index_file(unigram,os.path.join(inverted_index_unigrams,"inverted_index_unigram.txt"))


# Function to read stop words from the given file and storing them in a list
def read_stop_list_from_file(filename):
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            stop_words_list.append(line)

def get_clean_corpus(dir_name, handle_casefold, handle_punctuations):

    files = os.listdir(dir_name)
    for eachFile in files:
        fileName = os.path.join(dir_name, eachFile)
        print("Cleaning file : " + eachFile)
        file = open(fileName, 'r+', encoding = 'utf-8')
        data = file.read()

        soup = BeautifulSoup(data, 'html.parser')

        # To remove formualae present in a document
        for formulae in soup('semantics'):
            formulae.decompose()
        raw_data = ""

        # Consider text between p,h1,h2,h3,h4 tags only
        for data in soup.find_all(['p','h1','h2','h3','h4','html']):
            raw_data = raw_data + data.text + " "
        # print(raw_data)
        # Regex to remove citations present in the document
        raw_data = re.sub('\\[[0-9,.]*\\]','',raw_data)

        # Regex to remove "," , "." and " ' " everywhere except if in between numbers.
        raw_data = re.sub('(?<=[^0-9])[.,\']|[.,\'](?=[^0-9])', '', raw_data)

        # For handling punctuations using string.punctuation.
        if handle_punctuations:
            intab = "\"#!$%&()*+/:;<=>?@[\]_`{|}^~?\'"
            outtab = "                              "
            raw_data = raw_data.translate(str.maketrans(intab, outtab, string.punctuation))

        # Regex to remove extra spaces between the words.
        raw_data = re.sub('\s\s+', ' ', raw_data)

        # Regex to remove extra lines between the words.
        raw_data = re.sub('\n', ' ', raw_data)

        # For handling case-folding using lower() to convert all the text in lower-case.
        if handle_casefold:
            raw_data = raw_data.lower()

        # To write parsed and tokenized data to file.
        filename = eachFile[eachFile.rfind('/')+1:len(eachFile)]
        filename = filename.replace(".html",".txt")
        completeName = os.path.join(cleaned_files_path, filename)
        f = open(completeName, 'w', encoding='utf-8')
        f.write(raw_data)
        f.close()


# Main function for generating clean corpus from raw CACM articles.
def main():

    # Option to handle case-folding, set as 'False' if case-folding is not required.
    handle_casefold = True

    # Option to handle punctuations, set as 'False' to retain all the punctuations.
    handle_punctuations = True

    # Option to handle stopping, set as 'False' to retain all the punctuations.
    handle_stopping = True

    # To generate clean corpus
    get_clean_corpus(raw_files_path, handle_casefold, handle_punctuations)

    create_inverted_index(cleaned_files_path, handle_stopping)


if __name__ == "__main__":
    main()
