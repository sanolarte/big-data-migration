FIELDS = {
    "employees": {
        "fields": ["employee_id", "name", "hire_datetime", "department_id", "job_id"],
        "mandatory_fields": ["employee_id", "name"],
        "foreign_keys": ["department_id", "job_id"],
    },
    "jobs": {
        "fields": ["job_id", "job_name"],
        "mandatory_fields": ["job_id", "job_name"],
    },
    "departments": {
        "fields": ["department_id", "department_name"],
        "mandatory_fields": ["department_id", "department_name"],
    },
}


def get_foreign_keys(entity):
    return FIELDS.get(entity).get("foreign_keys")


def get_fields(entity):
    return FIELDS.get(entity)["fields"]


def get_mandatory_fields(entity):
    return FIELDS.get(entity)["mandatory_fields"]
