
def build_insert_query(entity, fields):
    fields.append("imported_from")
    query_string = f"""
        INSERT INTO {entity} ({', '.join(fields)})
        SELECT
            {', '.join(fields)} 
        FROM 
            stg_{entity}
            
    """

    return query_string

