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
    Return a dictionary where each key is a page, and values are a list of
    all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"",
                               contents)
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
    N = len(corpus)
    links = corpus.get(page)
    links_size = len(links)
    distribution = {k: 0 for k in corpus}

    for page_key in corpus:
        distribution[page_key] += (1-damping_factor)/N
        if page_key is not page and page_key in links:
            distribution[page_key] += damping_factor / links_size

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    distribution = {k: 0 for k in corpus}

    # pick the first page then update the distribution and transition_dict
    page = random.choice(list(corpus))
    distribution[page] = 1/n
    transition_dict = transition_model(corpus, page, damping_factor)
    
    # update the distribution for each newly generated sample
    for _ in range(n-1):
        page = random.choices(list(transition_dict.keys()), 
                              weights=list(transition_dict.values()),
                              k=1).pop()
        distribution[page] += 1/n
        transition_dict = transition_model(corpus, page, damping_factor)

    return distribution


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    N = len(corpus.keys()) # number pages in corpus
    C = ((1-damping_factor) / N) # constant in the equation

    distribution = {} # current interation
    next_distribution = {} # next iteration
    update_dist = {}
    
    # create incoming_links and first iteration distribution dictionary
    incoming_links = {k: set() for k in corpus.keys()}
    for page in corpus:
        distribution[page] = 1/N
        update_dist[page] = False

        # if the page has no links, update corpus to include all the 
        # possible links
        if not corpus[page]:
            corpus[page] = set(corpus.keys())

        # update incoming_links dictionary
        for linked_page in corpus[page]:
            incoming_links[linked_page].add(page)


    while not all(update_dist.values()):
        # create new iteration for each page
        for page in corpus:

            # start of rank equation
            rank_val = C 
            # summation part of the equation
            for i in incoming_links[page]:
                rank_val += (damping_factor * distribution[i] / len(corpus[i]))

            next_distribution[page] = rank_val
            
            update_dist[page] =  abs(rank_val - distribution[page]) <= 0.001
        
        # switch distributions to reuse previous iteration dictionary
        distribution, next_distribution = next_distribution, distribution

    
    return next_distribution


if __name__ == "__main__":
    main()
