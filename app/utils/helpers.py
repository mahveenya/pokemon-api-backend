def build_pagination(base_url, total, offset, limit):
    next_url = None
    previous_url = None

    if offset + limit < total:
        next_url = f"{base_url}?offset={offset + limit}&limit={limit}"

    if offset > 0:
        previous_url = f"{base_url}?offset={offset - limit}&limit={limit}"

    return next_url, previous_url
