import os
from dotenv import load_dotenv
from sqlalchemy import text, inspect
from backend import database

def check_structure():
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    print(f"Connecting to: {url.split('@')[-1]}") # Print host only for safety
    
    engine = database.engine
    inspector = inspect(engine)
    
    schemas = inspector.get_schema_names()
    print(f"Available Schemas: {schemas}")
    
    for schema in schemas:
        tables = inspector.get_table_names(schema=schema)
        if tables:
            print(f"Tables in schema '{schema}': {tables}")
            for table in tables:
                columns = [c['name'] for c in inspector.get_columns(table, schema=schema)]
                print(f"  - {table}: {columns}")

if __name__ == "__main__":
    check_structure()
