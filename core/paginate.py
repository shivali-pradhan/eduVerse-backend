def paginate(page_num: int, page_size: int, query_items):
    offset = (page_num - 1) * page_size
    paginated_items = query_items.offset(offset).limit(page_size).all()

    return {
        "total_items": len(query_items.all()),
        "page_num": page_num,
        "page_size": page_size,
        "items": paginated_items
    }