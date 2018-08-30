import os
import re
import operator


# Set as location of raw html text files which are to be used for generating a clean corpus.
corpus_file = '../../Dataset/cacm_stem.txt'

# Set as location of cleaned corpus which are to be used for generating inverted lists for n-grams.
cleaned_files_path = '../../Dataset/cleaned_files_with_stemming'

# Set as location to store the files consisting of the total term-count (with duplicates)
# of each document in the cleaned corpus.
term_count = '../../Dataset/Indexer_Files_with_stemming'

# Set as location to store the files consisting of the n-grams index generated of
# each document in the cleaned corpus.
inverted_index_unigrams = '../../Dataset/Indexer_Files_with_stemming'

# Set as location to store the files consisting of term-frequency table for all the
# documents in the cleaned corpus.
unigram_tf = '../../Dataset/Indexer_Files_with_stemming'

# Set as location to store the files consisting of document-frequency table for all
# the documents in the cleaned corpus.
unigram_df = '../../Dataset/Indexer_Files_with_stemming'

# Dictionaries to store the inverted indexes and terms generated.
unigram = {}

# Dictionaries to store the term count for each document.
unigram_terms = {}


# Function to generate uni-gram tokens.
def unigram_index_without_stopping(word_list, file_name):
    term_count = 0  # For storing the term-count for entire document (with duplicates).
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
    unigram_terms.update({file_name[0]: str(term_count)})


# Function to generate term frequency table for uni-grams.
def create_tf(any_dictionary, fileName):
    dict_tf = {}
    for key in any_dictionary.keys():
        sum_tf = 0
        dict_temp = any_dictionary[key]
        for each_file in dict_temp.keys():
            sum_tf = sum_tf + dict_temp[each_file]

        dict_tf.update({key: sum_tf})

    dict_tf_temp = sorted(dict_tf.items(), key=operator.itemgetter(1), reverse=True)

    f = open(fileName, 'w')
    f.write("term:" + " tf " + "\n")
    write_to = ''
    for key, value in dict_tf_temp:
        write_to += key + ':' + str(value) + '\n'

    f.write(write_to)
    f.close()


# Function to generate df tables for uni-grams.
def create_df(any_dictionary, fileName):
    dict_df = sorted(any_dictionary.items(), key=operator.itemgetter(0))
    f = open(fileName, 'w')
    f.write("term : " + " docIDs : " + " df " + "\n")
    for key, value in dict_df:
        term = key
        docIds = ''
        df = len(value)
        k = 0  # Append ',' only if k < count.
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
        f.write(keys[i] + ":" + str(values[i]) + "\n")
    f.close()


# Function to generate inverted index files for uni-grams with term, docId and
# term positions in each document [term :(docId,term position)].
def create_index_with_term_pos(any_dictionary, fileName):
    dict_term_pos = sorted(any_dictionary.items(), key=operator.itemgetter(0))
    f = open(fileName, 'w')
    f.write("term : " + " (docIDs : " + " termPos) " + "\n")
    for key, value in dict_term_pos:
        term = key
        docs = ''
        dict_index = any_dictionary[key]
        count = len(value)
        k = 0  # Append ',' only if k < count.
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

        f.write(term + "---->" + docs + "\n")

    f.close()


def create_inverted_index(dir_nam):
    files = os.listdir(dir_nam)

    for eachFile in files:
        file_name = eachFile.split(".txt")
        print("Generated index for : " + eachFile)
        complete_file_name = os.path.join(dir_nam, eachFile)
        file = open(complete_file_name, 'r+')
        data = file.read()
        word_list = data.split(None)
        # To create inverted index for uni-grams.
        unigram_index_without_stopping(word_list, file_name)

    # To create tf and df for uni-grams.
    create_tf(unigram, os.path.join(unigram_tf, "unigram_tf.txt"))
    create_df(unigram, os.path.join(unigram_df, "unigram_df.txt"))

    # To create files containing number of terms in each file.
    create_term_count_dict(unigram_terms, os.path.join(term_count, "unigram_terms.txt"))

    # To creates file containing inverted index for uni-grams.
    create_inverted_index_file(unigram, os.path.join(inverted_index_unigrams, "inverted_index_unigram.txt"))


# Function creates seperate docs and indexes them
def get_clean_corpus(corpusFile):
    gen_filename = "CACM-"

    with open(corpusFile, 'r') as file:
        data = file.read().split('#')

    num = 0
    for doc in data[1:]:
        num += 1

        document_no = format(num, "04")
        filename = gen_filename + str(document_no) + ".txt"

        document_data = find_content(doc.strip().split(" "))
        if document_data != "":
            document_data = document_data[2:]
            document_data = document_data[:-1]

        with open(os.path.join(cleaned_files_path, filename), 'w') as f:
            f.write(document_data)

        print("Document parsed successfully " + filename)


# Function to get content for each doc
def find_content(doc_content):
    document_data = ""
    # To terminate if we see an "am" or "pm" in the file as we ignore numbers after content
    flag = 0

    for line in doc_content:
        if not ((line == "") or (line == "['") or (line == "']")):
            line = line.replace(r"\t", " ")
            line = line.replace("\n", " ")
            words = line.split(" ")
            for word in words:
                if not re.match("^[A-Za-z0-9]*$", word):
                    continue
                if (word == "pm") or (word == "am"):
                    flag = 1
                document_data = document_data + word + " "
            if flag == 1:
                break

    return document_data


# Main function for generating clean corpus from raw CACM articles.
def main():
    # To generate clean corpus from the stemmed corpus
    get_clean_corpus(corpus_file)
    # Create Inverted index from the cleaned corpus
    create_inverted_index(cleaned_files_path)


if __name__ == "__main__":
    main()
