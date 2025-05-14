
def build_insert_query(entity, fields, foreign_keys):
    fields.append("imported_from")
    query_string = ""
    if foreign_keys:
        query_string = f"""
            INSERT INTO {entity} ({', '.join(fields)})
            SELECT 
                e.employee_id,
                e.name,
                e.hire_datetime,
                d.id,
                j.id,
                e.imported_from
            FROM
                stg_{entity} e
            JOIN
                departments d ON e.department_id = d.department_id
            JOIN
                jobs j ON e.job_id = j.job_id
        """
    else:
        query_string = f"""
            INSERT INTO {entity} ({', '.join(fields)})
            SELECT
                {', '.join(fields)} 
            FROM 
                stg_{entity}
                
        """

    return query_string

