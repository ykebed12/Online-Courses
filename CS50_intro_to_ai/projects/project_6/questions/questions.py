import nltk
import sys
import os
from string import punctuation as punc
from math import log

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    file_contents = dict()

    for filename in os.listdir(directory):
        file_dir = os.path.join(directory, filename)
        if (filename.endswith('.txt') and os.path.isfile(file_dir)):
            file_obj = open(file_dir, mode='r')
            file_contents[filename] = file_obj.read()
            file_obj.close()

    return file_contents


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokens = nltk.tokenize.word_tokenize(document.lower())

    filtered_words = list(filter(
        lambda word:
            (word not in nltk.corpus.stopwords.words("english"))
            and (word not in punc),
        tokens
    ))

    return filtered_words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """

    word_counts = dict()

    for document in documents:
        text_set = set(documents[document])
        for word in text_set:
            word_counts[word] = word_counts.get(word, 0) + 1

    doc_size = len(documents)
    return {k: log(doc_size/v) for k, v in word_counts.items()}


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idfs = dict()

    for file in files:
        tfidf_sum = 0
        for word in query:
            tf = files[file].count(word)
            tfidf_sum += tf*idfs[word]
        tf_idfs[file] = tfidf_sum

    return sorted(tf_idfs, key=tf_idfs.get, reverse=True)[:n]
    # return nlargest(n, tf_idfs, key=tf_idfs.get)


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """

    query_terms = dict()

    def get_q_density(query_term):
        return query_terms.get(query_term)[1]

    def get_idf_sum(query_term):
        return query_terms.get(query_term)[0]

    for sentence in sentences:
        idf_sum = 0
        query_count = 0
        for word in query:
            if word in sentences[sentence]:
                idf_sum += idfs[word]
                query_count += sentences[sentence].count(word)

        q_density = query_count/len(sentences[sentence])
        query_terms[sentence] = (idf_sum, q_density)

    sorted_keys = sorted(query_terms, key=get_q_density, reverse=True)

    return sorted(sorted_keys, key=get_idf_sum, reverse=True)[:n]


if __name__ == "__main__":
    main()
