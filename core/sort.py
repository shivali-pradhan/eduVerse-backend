def sort(query, model, model_fields, sort_field, order):
    if sort_field in model_fields:
        sort_column = sort_column = getattr(model, sort_field)
        if order == "desc":
            sort_column = sort_column.desc()
            
        query = query.order_by(sort_column)

    return query