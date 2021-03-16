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
    searcher.search()


class search_engine:
    def __init__(self, dict_file, posting_file):
        self.dict, self.docNum = utils.convert_file_to_dict(dict_file)
        self.dict_file = dict_file
        self.posting_file = posting_file
        self.f = open(self.posting_file, 'r')


    def search(self):
        print(self.docNum)
        print(self.get_posting("in"))


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
