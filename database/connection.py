from sqlalchemy import create_engine, text

# Connection parameters
username = "XXXXXXXX"
password = "XXXXXXXX"
host = "localhost"         # or a remote host
port = 3307                # default MySQL port
database = "abc_hr"

# Create SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database}")


# with engine.connect() as con:
#     with open("init.sql") as file:
#         query = text(file.read())
#         con.execute(query)