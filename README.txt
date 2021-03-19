This is the README file for A0000000X-A0173238A's submission

== Python Version ==

We're using Python Version 3.4.6/3.8.5 for this assignment.

== General Notes about this assignment ==

For this project, we did away with the scalable index construction as it was no longer
required. Instead, for each document, we generate tuples of the term, the docID the term
came from and the weight of the term for the docID it originates from. At this step we
calculate the length of document vector. After, We then use these tuples to generate a
giant dictionary for the entire set of documents, before writing the dictionary
and the posting lists to their respective files. We also store the total number of documents N
in before writing out the dictionary for the calculation of idf.

During the search, we implemented the cosine function that was went through in the slides.
For each query term, we retrieve the posting lists, calculate the product of the weights for
each document and the weight of the query (the tf-idf). At the end, we normalize the score
for all the documents by their pre-calculated length value and return the top 10 documents.

== Files included with this submission ==

index.py
The file responsible for indexing the documents from the Reuters data set, and
storing the the indexes to dictionary.txt and postings.txt.

search.py
The file responsible for performing the query search on the indexed files and writing
the results out to the specified output file.

utils.py
A list of common functions and variables used by both index.py and search.py.

dictionary.txt
The dictionary file containing the terms and the document frequency, as well as the pointer
locations to the corresponding terms posting lists in the postings.txt.

postings.txt
The text file containing the posting lists of the all the terms in the dictionary file.

lengths.txt
The metadata file containing the calculated lengths of all the documents to their respective
document id.

README.txt
This file.

ESSAY.txt
The text file containing the answers to the discussion questions.

== Statement of individual work ==

Please put a "x" (without the double quotes) into the bracket of the appropriate statement.

[x] We, A0000000X-A0173238A, certify that I/we have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I/we
expressly vow that I/we have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.  

[ ] I/We, A0000000X, did not follow the class rules regarding homework
assignment, because of the following reason:

<Please fill in>

We suggest that we should be graded as follows:

<Please fill in>

== References ==

<Please list any websites and/or people you consulted with for this
assignment and state their role>
