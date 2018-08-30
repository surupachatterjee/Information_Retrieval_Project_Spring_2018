import os
from collections import defaultdict

# Path for Different ranking results output
Query_ranking_path_Task1 = "../Task1"
Query_ranking_path_Task2 = "../Task2"
Query_ranking_path_Task3 = "../Task3"
Query_ranking_path_Extra_Credit = "../Extra_Credit"

BM25_baseline = "BM25/BM25_Ranking.txt"
Lucene_baseline = "Lucene/Lucene_Ranking.txt"
Query_likelihood_baseline = "Query_Likelihood_Model_0.35/Query_Likelihood_Model_0.35_Ranking.txt"
TF_IDF_baseline = "TF_iDF/TF_iDF_Ranking.txt"
Query_enriched_bm25 = "Results/BM25_Ranking_After_Query_Enriched.txt"
BM25_stopping = "Stopping/BM25/BM25_Ranking_with_stopping.txt"
Query_likelihood_stopping = "Stopping/Query_Likelihood_Model_0.35/Query_Likelihood_Model_0.35_Ranking_with_stopping.txt"
TF_IDF_stopping = "Stopping/TF_iDF/TF_iDF_Ranking_with_stopping.txt"
BM25_with_error_queries = "BM25/BM25_Ranking_with_error_queries.txt"
BM25_with_spell_check = "BM25/BM25_Ranking_with_spell_checking.txt"
Query_likelihood_baseline_with_error_query = \
            "Query_Likelihood_Model_0.35/Query_Likelihood_Model_0.35_Ranking_with_error_queries.txt"
Query_likelihood_baseline_with_spell_check =\
            "Query_Likelihood_Model_0.35/Query_Likelihood_Model_0.35_Ranking_with_spell_checking.txt"
TF_IDF_with_error_query = "TF_iDF/TF_iDF_Ranking_with_error_queries.txt"
TF_IDF_with_spell_check = "TF_iDF/TF_iDF_Ranking_with_spell_checking.txt"

Query_ranking_path_bm25_baseline = Query_ranking_path_Task1 + '/' + BM25_baseline
Query_ranking_path_lucene_baseline = Query_ranking_path_Task1 + "/" + Lucene_baseline
Query_ranking_path_query_likelihood_baseline = Query_ranking_path_Task1 + "/" + Query_likelihood_baseline
Query_ranking_path_tf_idf_baseline = Query_ranking_path_Task1 + "/" + TF_IDF_baseline
Query_ranking_path_bm25_query_enrichment = Query_ranking_path_Task2 + "/" + Query_enriched_bm25
Query_ranking_path_bm25_stopped = Query_ranking_path_Task3 + "/" + BM25_stopping
Query_ranking_path_query_likelihood_stopped = Query_ranking_path_Task3 + "/" + Query_likelihood_stopping
Query_ranking_path_tf_idf_stopped = Query_ranking_path_Task3 + "/" + TF_IDF_stopping
Query_ranking_path_bm25_with_error_queries = Query_ranking_path_Extra_Credit + "/" + BM25_with_error_queries
Query_ranking_path_bm25_with_spell_check = Query_ranking_path_Extra_Credit + "/" + BM25_with_spell_check
Query_ranking_path_query_likelihood_with_error_query = Query_ranking_path_Extra_Credit + "/" \
                                                       + Query_likelihood_baseline_with_error_query
Query_ranking_path_query_likelihood_with_spell_check = Query_ranking_path_Extra_Credit + "/" \
                                                       + Query_likelihood_baseline_with_spell_check
Query_ranking_path_tf_idf_with_error_check = Query_ranking_path_Extra_Credit + "/" + TF_IDF_with_error_query
Query_ranking_path_tf_idf_with_spell_check = Query_ranking_path_Extra_Credit + "/" + TF_IDF_with_spell_check


# Path for Storing evaluation results
evaluation_results_path = "evaluation_results/"
results_path_bm25_baseline = evaluation_results_path + "BM25_baseline/"
results_path_lucene_baseline = evaluation_results_path + "Lucene_baseline/"
results_path_query_likelihood_baseline = evaluation_results_path + "Query_likelihood_baseline/"
results_path_tf_idf_baseline = evaluation_results_path + "TF_IDF_baseline/"
results_path_bm25_query_enrichment = evaluation_results_path + "BM25_Query_Enrichment/"
results_path_bm25_stopped = evaluation_results_path + "BM25_with_stopping/"
results_path_query_likelihood_stopped = evaluation_results_path + "Query_likelihood_with_stopping/"
results_path_tf_idf_stopped = evaluation_results_path + "TF_IDF_with_stopping/"
results_path_bm25_with_error_query = evaluation_results_path + "BM25_with_error_query/"
results_path_bm25_with_spell_check = evaluation_results_path + "BM25_with_spell_check/"
results_path_query_likelihood_with_error_query = evaluation_results_path + "Query_likelihood_with_error_query/"
results_path_query_likelihood_with_spell_check = evaluation_results_path + "Query_likelihood_with_spell_check/"
results_path_tf_idf_with_error_query = evaluation_results_path + "TF_IDF_with_error_query/"
results_path_tf_idf_with_spell_check = evaluation_results_path + "TF_IDF_with_spell_check/"


# Path for the relevance data
relevance_data_path = "../Dataset/cacm.rel.txt"


def evaluate_effectiveness():
    if not os.path.exists(evaluation_results_path):
        os.mkdir(evaluation_results_path)

    # Calculate effectiveness for BM25_baseline
    query_ranks = get_query_ranks(Query_ranking_path_bm25_baseline)
    relevance_information = get_relevance_data()
    calculate_effectiveness_measures(query_ranks, relevance_information, results_path_bm25_baseline)

    # Calculate effectiveness for Lucene_baseline
    query_ranks = get_query_ranks(Query_ranking_path_lucene_baseline)
    relevance_information = get_relevance_data()
    calculate_effectiveness_measures(query_ranks, relevance_information, results_path_lucene_baseline)

    # Calculate effectiveness for Query_likelihood_baseline
    query_ranks = get_query_ranks(Query_ranking_path_query_likelihood_baseline)
    relevance_information = get_relevance_data()
    calculate_effectiveness_measures(query_ranks, relevance_information, results_path_query_likelihood_baseline)

    # Calculate effectiveness for TF-IDF_baseline
    query_ranks = get_query_ranks(Query_ranking_path_tf_idf_baseline)
    relevance_information = get_relevance_data()
    calculate_effectiveness_measures(query_ranks, relevance_information, results_path_tf_idf_baseline)

    # Calculate effectiveness for BM25_with_query_enrichment
    query_ranks = get_query_ranks(Query_ranking_path_bm25_query_enrichment)
    relevance_information = get_relevance_data()
    calculate_effectiveness_measures(query_ranks, relevance_information, results_path_bm25_query_enrichment)

    # Calculate effectiveness for BM25_with_stopping
    query_ranks = get_query_ranks(Query_ranking_path_bm25_stopped)
    relevance_information = get_relevance_data()
    calculate_effectiveness_measures(query_ranks, relevance_information, results_path_bm25_stopped)

    # Calculate effectiveness for Query_likelihood_with_stopping
    query_ranks = get_query_ranks(Query_ranking_path_query_likelihood_stopped)
    relevance_information = get_relevance_data()
    calculate_effectiveness_measures(query_ranks, relevance_information, results_path_query_likelihood_stopped)

    # Calculate effectiveness for TF-IDF_with_stopping
    query_ranks = get_query_ranks(Query_ranking_path_tf_idf_stopped)
    relevance_information = get_relevance_data()
    calculate_effectiveness_measures(query_ranks, relevance_information, results_path_tf_idf_stopped)

    # Calculate effectiveness for BM25 with error queries
    query_ranks = get_query_ranks(Query_ranking_path_bm25_with_error_queries)
    relevance_information = get_relevance_data()
    calculate_effectiveness_measures(query_ranks, relevance_information, results_path_bm25_with_error_query)

    # Calculate effectiveness for BM25_with_spell_checker results
    query_ranks = get_query_ranks(Query_ranking_path_bm25_with_spell_check)
    relevance_information = get_relevance_data()
    calculate_effectiveness_measures(query_ranks, relevance_information, results_path_bm25_with_spell_check)

    # Calculate effectiveness for Query likelihood with error queries
    query_ranks = get_query_ranks(Query_ranking_path_query_likelihood_with_error_query)
    relevance_information = get_relevance_data()
    calculate_effectiveness_measures(query_ranks, relevance_information, results_path_query_likelihood_with_error_query)

    # Calculate effectiveness for Query likelihood with spell checker
    query_ranks = get_query_ranks(Query_ranking_path_query_likelihood_with_spell_check)
    relevance_information = get_relevance_data()
    calculate_effectiveness_measures(query_ranks, relevance_information, results_path_query_likelihood_with_spell_check)

    # Calculate effectiveness for TF-IDF with error query
    query_ranks = get_query_ranks(Query_ranking_path_tf_idf_with_error_check)
    relevance_information = get_relevance_data()
    calculate_effectiveness_measures(query_ranks, relevance_information, results_path_tf_idf_with_error_query)

    # Calculate effectiveness for TF-IDF with spell checker
    query_ranks = get_query_ranks(Query_ranking_path_tf_idf_with_spell_check)
    relevance_information = get_relevance_data()
    calculate_effectiveness_measures(query_ranks, relevance_information, results_path_tf_idf_with_spell_check)


def calculate_effectiveness_measures(query_ranks, relevance_information, results_path):
    if not os.path.exists(results_path):
        os.mkdir(results_path)

    # List containing avg_precisions
    avg_precision_list = []
    # List containing reciprocal rank for the first relevant doc retrieved for the query
    first_rec_rank = []

    for qid in query_ranks:
        for val in query_ranks[qid]:
            # If the query is not in the relevance list skip the query
            if qid not in relevance_information:
                continue
            if val[0] not in relevance_information[qid]:
                continue

            directory_name = results_path + "Query" + str(qid) + "/"
            doc_list = query_ranks[qid]

            # Calculating precision for the given query ranks using the relevance
            precision_table = calculate_precision(doc_list, qid, relevance_information, first_rec_rank)
            output = ""
            if precision_table:
                if not os.path.exists(directory_name):
                    os.mkdir(directory_name)
                for doc_name in precision_table:
                    output = output + doc_name + "\t" + str(precision_table[doc_name]) + "\n"
                file_path = directory_name + "PrecisionTable.txt"
                with open(file_path, 'w') as f:
                    f.write(output)

                # Calculating Precision_at_5 and Precision_at_20
                precision_at_5 = calculate_precision_at_k(5, precision_table)
                precision_at_20 = calculate_precision_at_k(20, precision_table)
                output = "\nPrecision_@_5 :" + str(precision_at_5)
                output = output + "\nPrecision_@_20 :" + str(precision_at_20)
                file_path = directory_name + "Precision_at_K.txt"
                with open(file_path, 'w') as f:
                    f.write(output)

            avg_precision = calculate_average_precision(doc_list, qid, relevance_information, precision_table)
            avg_precision_list.append(avg_precision)

            # Calculating recall for the given query ranks using the relevance
            recall_table = calculate_recall(doc_list, qid, relevance_information)
            output = ""
            if recall_table:
                if not os.path.exists(directory_name):
                    os.mkdir(directory_name)
                for doc_name in recall_table:
                    output = output + doc_name + "\t" + str(recall_table[doc_name]) + "\n"
                file_path = directory_name + "RecallTable.txt"
                with open(file_path, 'w') as f:
                    f.write(output)

    mean_avg_precision = calculate_mean_avg_precision(avg_precision_list)
    mean_reciprocal_rank = calculate_mean_reciprocal_rank(first_rec_rank)
    output = "Mean Average Precision : " + str(mean_avg_precision) + "\n"
    output = output + "Mean Reciprocal Rank : " + str(mean_reciprocal_rank)

    file_path = results_path + "MAP_MRR.txt"
    with open(file_path, 'w') as f:
        f.write(output)
    print("Evaluation Completed for the given model.")


def calculate_precision(doc_list, qid, relevance_information, first_rec_rank):
    precision_table_calc = {}
    retrieved_relevant_cnt = 0
    retrieved_cnt = 0

    for doc_id_rank_tuple in doc_list:
        rank = doc_id_rank_tuple[1]
        doc_name = doc_id_rank_tuple[0]

        if doc_name in relevance_information[qid]:
            retrieved_relevant_cnt = retrieved_relevant_cnt + 1
            if retrieved_relevant_cnt == 1:
                first_rec_rank.append(1 / int(rank))

        retrieved_cnt = retrieved_cnt + 1
        precision_table_calc.update({doc_name: (retrieved_relevant_cnt / retrieved_cnt)})

    return precision_table_calc


def calculate_average_precision(doc_list, qid, relevance_information, precision_table):
    total = 0
    for doc_name in relevance_information[qid]:
        for item in doc_list:
            if item[0] == doc_name:
                total = total + precision_table[doc_name]
                break

    return total / len(relevance_information[qid])


# Function to calculate precision at K
def calculate_precision_at_k(k, precision_table):
    rank = 1

    for doc_name in precision_table:
        if rank == k:
            return precision_table[doc_name]
        rank += 1

    return 0


def calculate_recall(doc_list, qid, relevance_information):
    recall_calc_table = {}
    retrieved_relevant_cnt = 0
    relevant_cnt = len(relevance_information[qid])

    for doc_id_rank_tuple in doc_list:
        doc_name = doc_id_rank_tuple[0]
        doc_name = doc_name.rsplit()[0]
        if doc_name in relevance_information[qid]:
            retrieved_relevant_cnt = retrieved_relevant_cnt + 1

        recall_calc_table.update({doc_name: (retrieved_relevant_cnt / relevant_cnt)})

    return recall_calc_table


# Function to calculate MAP
def calculate_mean_avg_precision(avg_precision_list):
    total = 0

    for precision in avg_precision_list:
        total = total + precision

    return total / len(avg_precision_list)


# Function to calculate MRR
def calculate_mean_reciprocal_rank(first_rec_rank):
    total = 0

    for reciprocal_rank in first_rec_rank:
        total = total + reciprocal_rank

    return total / len(first_rec_rank)


def get_query_ranks(path):
    query_ranks = defaultdict(list)
    termination = "^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"

    with open(path, 'r') as file:
        data = file.read().split(termination)

    for results in data[1:]:
        query_results = results.strip().split('\n')
        for line in query_results:
            line = line.strip()
            if not (("Query" in line) or line == ''):
                tokens = line.split(" ")
                # Extra condition for Lucene to trim .txt at the end
                if ".txt" in tokens[3]:
                    temp = tokens[3].replace('.txt', '')
                    doc_id_rank_tuple = (temp, tokens[4])
                else:
                    doc_id_rank_tuple = (tokens[3], tokens[4])
                query_ranks[tokens[0]].append(doc_id_rank_tuple)

    return query_ranks


# Retrieve relevance data and store it in a dictionary
def get_relevance_data():
    with open(relevance_data_path, "r") as f:
        data = f.read().split("\n")

    relevance_information = {}

    for line in data:
        line = line.strip()
        if line == "":
            continue
        token = line.split(" ")
        query_id = token[0]
        doc_id = token[2]
        if query_id in relevance_information:
            relevance_information[query_id].append(doc_id)
        else:
            relevance_information.update({query_id: [doc_id]})

    return relevance_information


if __name__ == "__main__":
    evaluate_effectiveness()
