# Questions

Write an AI to answer questions.

```
$ python questions.py corpus
Query: What are the types of supervised learning?
Types of supervised learning algorithms include Active learning, classification and regression.

$ python questions.py corpus
Query: When was Python 3.0 released?
Python 3.0 was released on 3 December 2008.

$ python questions.py corpus
Query: How do neurons connect in a neural network?
Neurons of one layer connect only to neurons of the immediately preceding and immediately following layers.
```

## Background

Question Answering (QA) is a field within natural language processing focused on designing systems that can answer questions. Among the more famous question answering systems is Watson, the IBM computer that competed (and won) on Jeopardy!. A question answering system of Watson’s accuracy requires enormous complexity and vast amounts of data, but in this problem, we’ll design a very simple question answering system based on inverse document frequency.

Our question answering system will perform two tasks: document retrieval and passage retrieval. Our system will have access to a corpus of text documents. When presented with a query (a question in English asked by the user), document retrieval will first identify which document(s) are most relevant to the query. Once the top documents are found, the top document(s) will be subdivided into passages (in this case, sentences) so that the most relevant passage to the question can be determined.

How do we find the most relevant documents and passages? To find the most relevant documents, we’ll use tf-idf to rank documents based both on term frequency for words in the query as well as inverse document frequency for words in the query. Once we’ve found the most relevant documents, there many possible metrics for scoring passages, but we’ll use a combination of inverse document frequency and a query term density measure (described in the Specification).

More sophisticated question-answering systems might employ other strategies (analyzing the type of question word used, looking for synonyms of query words, lemmatizing to handle different forms of the same word, etc.) but we’ll leave those sorts of improvements as exercises for you to work on if you’d like to after you’ve completed this project!

## Getting Started

### Dependencies

* Python 3.10 and Python package installer, Pip3

### Executing program

* Open the project in your terminal
* Download dependencies
` $ pip install -r requirements.txt`
* Run the script with a corpus of .txt files (you can use the one provided)
`$ python questions.py [your_corpus]`
