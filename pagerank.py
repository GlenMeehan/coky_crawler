# pagerank.py

def calculate_pagerank(pages, links, iterations=100, damping_factor=0.85):
    pagerank = {page: 1.0 for page in pages}
    num_pages = len(pages)

    for _ in range(iterations):
        new_pagerank = {}
        for page in pages:
            inbound_links = [src for src, dst in links if dst == page]
            rank_sum = sum(pagerank[src] / len([dst for src_, dst in links if src_ == src]) for src in inbound_links)
            new_pagerank[page] = (1 - damping_factor) / num_pages + damping_factor * rank_sum
        pagerank = new_pagerank

    return pagerank
