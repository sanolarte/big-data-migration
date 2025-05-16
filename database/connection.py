from sqlalchemy import create_engine, text

# Connection parameters
username = "XXXXXXXX"
password = "XXXXXXXX"
host = "localhost"         # or a remote host
port = 3307                # default MySQL port
database = "abc_hr"

# Create SQLAlchemy engine
engine = create_engine(
    f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}"
)


def run_query(string_query):
    with engine.begin() as conn:
        result = conn.execute(text(string_query), {})

    return result


def run_duplicate_precheck(entity, fields):
    primary_key_field = fields[0]  # First element is primary key from imported data
    query = f"""
        SELECT {primary_key_field} FROM stg_{entity}
        WHERE {primary_key_field} IN (SELECT {primary_key_field} FROM {entity})
    """

    results = run_query(query)

    return results.fetchall()
