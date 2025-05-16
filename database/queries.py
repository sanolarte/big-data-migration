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


def employees_by_quarter(year_of_hire):
    query = f"""
        SELECT
            d.department_name AS department,
            j.job_name AS job,
            COUNT(CASE WHEN QUARTER(e.hire_datetime) = 1 THEN 1 END) AS q1,
            COUNT(CASE WHEN QUARTER(e.hire_datetime) = 2 THEN 1 END) AS q2,
            COUNT(CASE WHEN QUARTER(e.hire_datetime) = 3 THEN 1 END) AS q3,
            COUNT(CASE WHEN QUARTER(e.hire_datetime) = 4 THEN 1 END) AS q4
        FROM employees e
        JOIN departments d ON e.department_id = d.id
        JOIN jobs j ON e.job_id = j.id
        WHERE YEAR(e.hire_datetime) = {year_of_hire}
        GROUP BY
            d.department_name,
            j.job_name
        ORDER BY
            d.department_name ASC,
            j.job_name ASC;


        """
    return query