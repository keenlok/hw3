#!/usr/bin/python3
import re
import nltk
import sys
import getopt
import utils


def usage():
    print("usage: " + sys.argv[0] + " -d dictionary-file -p postings-file -q file-of-queries -o output-file-of-results")


def run_search(dict_file, postings_file, queries_file, results_file):
    """
    using the given dictionary file and postings file,
    perform searching on the given queries file and output the results to a file
    """
    print('running search on the queries...')
    searcher = search_engine(dict_file, postings_file)
    with open(queries_file, "r") as f:
        output = ""
        while True:
            query = f.readline()
            if len(query) == 0:
                break
            result = searcher.search(query)
            output += utils.format_result_list(result)

    # write results
    with open(results_file, "w") as f:
        f.write(output)


class search_engine:
    def __init__(self, dict_file, posting_file):
        self.dict, self.docNum = utils.convert_file_to_dict(dict_file)
        self.lengths = utils.convert_file_to_lengths(utils.length_file)
        self.dict_file = dict_file
        self.posting_file = posting_file
        self.f = open(self.posting_file, 'r')

        self.lengths = utils.convert_file_to_lengths(utils.length_file)

    def search(self, query):
        # print(self.docNum)
        # print(self.get_posting("in"))
        return self.calculate_ln_ltc(query)

    def get_posting(self, term):
        """
        given a term in the dictionary,
        using its pointers to retrieve its postings list
        """

        if term not in self.dict.keys():
            return []

        # read in posting list
        self.f.seek(int(self.dict[term][1]))
        posting = self.f.read(int(self.dict[term][2]))
        posting = utils.convert_line_to_posting_list(posting)

        return posting

    def calculate_query_weight(self, term, freq):
        """
        return query term weight as idf? based on ln-ltc example
        """
        if term in self.dict.keys():
            N = self.docNum
            wt = utils.calculate_weight(freq)
            idf = utils.calculate_idf(N, self.dict[term][0])
            return wt * idf
        else:
            return 0

    def calculate_ln_ltc(self, query):
        """
        get the documents with the top 10 scores
        """
        scores = {}
        query_terms_freq = utils.preprocess(query)
        query_terms_freq = utils.count_term(query_terms_freq)
        print(query_terms_freq)
        for term, freq in query_terms_freq.items():
            if term == '':
                continue
            weight = self.calculate_query_weight(term, freq)
            posting_list = self.get_posting(term)
            for docID, term_weight in posting_list:
                product = weight * term_weight
                if docID in scores.keys():
                    scores[docID] += product
                else:
                    scores[docID] = product

        # get length TODO: decide whether to use integers or strings for docID!!
        for docID in scores.keys():
            scores[docID] = scores[docID] / self.lengths[docID]

        sorted_scores = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
        return sorted_scores[:10]  # return the 10 highest scoring items


dictionary_file = postings_file = file_of_queries = output_file_of_results = None

try:
    opts, args = getopt.getopt(sys.argv[1:], 'd:p:q:o:')
except getopt.GetoptError:
    usage()
    sys.exit(2)

for o, a in opts:
    if o == '-d':
        dictionary_file  = a
    elif o == '-p':
        postings_file = a
    elif o == '-q':
        file_of_queries = a
    elif o == '-o':
        file_of_output = a
    else:
        assert False, "unhandled option"

if dictionary_file == None or postings_file == None or file_of_queries == None or file_of_output == None :
    usage()
    sys.exit(2)

run_search(dictionary_file, postings_file, file_of_queries, file_of_output)
