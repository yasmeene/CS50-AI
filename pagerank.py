import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    n_links = len(corpus[page])
    n_pages = len(corpus)
    distribution = {}

    if corpus[page]:
        for key in corpus:
            # calculates the distribution of the respectitive page (key) by using
            distribution[key] = (1- damping_factor) / n_pages

            if key in corpus[page]:
                # assigns the distribution for all pages in corpus
                distribution[key] += damping_factor / n_pages
    else:
        # if the number of links on a page is 0, then we treat it as if it has links to every page (including itself)
        for key in corpus:
            distribution[key] = 1 / n_pages
    
    # returns a dictionary value with the page as the key and the probability as the value
    return distribution

def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    counts = {page: 0 for page in corpus}

    # chooses a random page in the corpus to start with
    samples = random.choice(list(counts))

    # counts the amount of times we go on each page
    counts[samples] += 1

    # loops through all the samples
    for i in range(n - 1):
        # runs our model through transision model to get probabilities so we can what % of times we should land on a specified page
        model = transition_model(corpus, samples, damping_factor)

        # randomly chooses the next page to go on using the probablities from the last step
        samples = random.choices(list(model), list(model.values()))[0]

        # add a count to keep track of the amount of times we land on a page
        counts[samples] += 1

    # finds estimated pagerank value by dividing the amount of times we've landed on a specific page by the sample (n)
    return {page: count/n for page, count in counts.items()}


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus)
    dist = {}
    current = {}

    # assignes a value of 1/N for each page in the corpus
    for page in corpus:
        dist[page] = 1/N

    repeat = True
    while repeat:
        repeat = False

        sum = 0
        for page in corpus:
            # makes a copy of the distribution
            current[page] = dist[page]

            sum = 0
            # kinda replicates PR(i) / NumLinks(i) from PageRank equation 
            sum += dist[page] / len(corpus[page])
            # using PageRank equation
            dist[page] = (1 - damping_factor) / N + damping_factor * sum
            current[page] = abs(current[page] - dist[page])
            repeat = repeat or current[page] > 0.001

    return dist


if __name__ == "__main__":
    main()
