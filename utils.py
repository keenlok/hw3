import math


def calculate_weight(freq):
    if freq == 0:
        return 0
    weight = 1 + math.log(freq, 10)
    return round(weight, 5)


def convert_line_to_posting_list(line):
    new_pl = []
    for token in line.split(" "):
        docID, weight = token.split(",")
        new_pl.append([docID, float(weight)])

    return new_pl


def convert_file_to_dict(dict_file):
    dictionary = {}
    with open(dict_file, 'r') as f:
        docNum = int(f.readline())
        while True:
            line = f.readline()
            if not line:
                break
            term, doc_freq, start, end = line.split(" ")
            dictionary[term] = [int(doc_freq), int(start), int(end)]

    return dictionary, docNum


def calculate_idf(N_total_docs, doc_freq):
    return math.log(N_total_docs / (doc_freq * 1.0), 10)


def format_result_list(results):
    output = ""
    for i in range(len(results)):
        output += str(results[i])
        if i != len(results) - 1:
            output += " "
    output += "\n"
    return output

# line = "797,1.47712 1069,1.30103 9036,1.60206 9204,1.47712 13089,1.47712"
# print(convert_line_to_posting_list(line))

# dic = convert_file_to_dict("dictionary.txt")
# print(dic)