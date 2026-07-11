def build_pagination(base_url, total, offset, limit, search=None):
    next_url = None
    previous_url = None
    search_suffix = f"&search={search}" if search else ""

    if offset + limit < total:
        next_url = f"{base_url}?offset={offset + limit}&limit={limit}{search_suffix}"

    if offset > 0:
        previous_url = (
            f"{base_url}?offset={offset - limit}&limit={limit}{search_suffix}"
        )

    return next_url, previous_url
