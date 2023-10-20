from sqlalchemy import create_engine

username = 'lyv_user'
password = 'pgadmin'
host = 'localhost'
port = '5432'
database_name = 'temp_data'

connection_string = f"postgresql://{username}:{password}@{host}:{port}/{database_name}"
engine = create_engine(connection_string, echo=True)