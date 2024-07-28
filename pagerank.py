def calculate_page_rank(pages, links, iterations=100, damping_factor=0.85):
    print("***A PAGE IS BEING RANKED NOW***")

    # Initialize pagerank dictionary
    pagerank = {page: 1.0 for page in pages}
    num_pages = len(pages)

    # Open the file and set the initial value to 0
    with open('page_rank_progress_value.txt', 'w') as f:
        f.write('0')

    for iteration in range(iterations):
        new_pagerank = {}

        # Calculate progress as a percentage
        page_rank_progress = (iteration + 1) / iterations * 100

        # Update the progress in the file
        with open('page_rank_progress_value.txt', 'w') as f:
            f.write(f'{page_rank_progress}')

        #print(page_rank_progress)

        for page in pages:
            # Calculate the rank sum for the current page
            inbound_links = [src for src, dst in links if dst == page]
            rank_sum = sum(pagerank[src] / len([dst for src_, dst in links if src_ == src]) for src in inbound_links)
            new_pagerank[page] = (1 - damping_factor) / num_pages + damping_factor * rank_sum

        pagerank = new_pagerank

    return pagerank
