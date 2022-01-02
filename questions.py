import nltk
import sys
import os
import string
from math import log
nltk.download('stopwords')

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
    # for k,v in file_words.items():
    #     print(k,':',len(v))
        
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))
    print(query)

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
    file_mapping = {}
    
    files = os.listdir(directory)

    # iterate through all the files
    for filename in files:
        
        # checks all .txt files
        if filename.endswith('.txt'):
            f_path = os.path.join(directory, filename)
            with open(f_path, 'r', encoding="utf-8") as file:
                f_string = file.read()
                file_mapping[filename[:-4]] = f_string
                
    return file_mapping 

def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    
    list_words = []
    
    # tokenize the document in order to iterate through them
    word_document = nltk.tokenize.word_tokenize(document.lower())
    punct = string.punctuation
    stop_words = nltk.corpus.stopwords.words('english')
    
    for word in word_document:
        
        # check to see if the word has punctuation or is a stop word
        if word not in punct and word not in stop_words:
            list_words.append(word)
    
    return list_words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    IDFS= {}
    num_docs = len(documents)
    count = {}
    
    for file in documents:
        words_doc = set(documents[file])
        
        for word in words_doc:
            if word in count.keys():
                count[word] += 1
            else:
                count[word] = 1

    for word in count:
        # find IDF value of word
        IDFS[word] = log((num_docs/count[word]))
    
    return IDFS

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidfs = {}
    
    
    for file in files:
        tfidfs[file] = 0
        
        for word in query:
            words = files[file]
            tf = words.count(word)
            
            if word in idfs:
                idf = idfs[word]
                tfidfs[file] += idf * tf
                # print(file)
                
    rank = sorted([file for file in files], key = lambda x : tfidfs[x], reverse=True)
    # print(file)
    return rank[:n]        


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    
    top_sentence = {}
    
    for sentence in sentences:
        top_sentence[sentence] = {}
        top_sentence[sentence]['idf'] = 0
        top_sentence[sentence]['matches'] = 0

        length = len(sentences[sentence])
        
        for word in query:
            if word in sentences[sentence]:
                top_sentence[sentence]['idf'] += idfs[word]
                top_sentence[sentence]['matches'] += sentences[sentence].count(word)
        top_sentence[sentence]['qtd'] = float(top_sentence[sentence]['matches'] / length)
        
    sorted_sentences = sorted(top_sentence.keys(), key= lambda sentence: (top_sentence[sentence]['idf'], top_sentence[sentence]['qtd']), reverse=True)
    return sorted_sentences[:n]   


if __name__ == "__main__":
    main()
