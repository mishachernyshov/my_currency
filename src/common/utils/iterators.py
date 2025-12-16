from itertools import islice


def paginate_stream(iterator, page_size=10):
    while True:
        page = list(islice(iterator, page_size))
        if not page:
            break
        yield page
