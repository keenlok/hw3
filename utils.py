import math


def calculate_weight(freq):
    if freq == 0:
        return 0
    weight = 1 + math.log(freq, 10)
    return round(weight, 5)


def calculate_idf(N_total_docs, doc_freq):
    return math.log(N_total_docs / (doc_freq * 1.0), 10)


def calculate_ln_ltc(query, dictionary):
    pass


def cosine_score(query, dictionary):
    """
    get the documents with the top 10 scores
    """
    scores = []
    # get length
    pass



