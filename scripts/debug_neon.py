import os
from dotenv import load_dotenv
from sqlalchemy import text
from backend import database, models

def check_db():
    load_dotenv()
    url = os.getenv("DATABASE_URL")
    print(f"Checking Database: {url[:30]}...")
    
    session = database.SessionLocal()
    try:
        user_count = session.execute(text("SELECT count(*) FROM users")).scalar()
        print(f"Total Users in 'users' table: {user_count}")
        
        users = session.execute(text("SELECT id, username, email, role FROM users")).fetchall()
        for u in users:
            print(f" - ID: {u[0]}, User: {u[1]}, Email: {u[2]}, Role: {u[3]}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    check_db()
