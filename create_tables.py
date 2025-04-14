import psycopg2
import os
from dotenv import load_dotenv

def create_tables():
    # Load environment variables from .env.cloud
    load_dotenv('.env.cloud')
    
    # Get database connection parameters
    db_params = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')
    }
    
    try:
        # Connect to the database
        print("Connecting to database...")
        conn = psycopg2.connect(**db_params)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Read and execute the SQL script
        print("Creating tables...")
        with open('create_tables.sql', 'r') as f:
            sql_script = f.read()
            cur.execute(sql_script)
        
        # Verify the table was created
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'users'
            );
        """)
        if cur.fetchone()[0]:
            print("Table 'users' created successfully!")
        else:
            print("Failed to create table 'users'")
        
        # Show table structure
        cur.execute("""
            SELECT column_name, data_type, character_maximum_length
            FROM information_schema.columns
            WHERE table_name = 'users'
            ORDER BY ordinal_position;
        """)
        print("\nTable structure:")
        for row in cur.fetchall():
            print(f"Column: {row[0]}, Type: {row[1]}, Length: {row[2]}")
        
        # Close database connection
        cur.close()
        conn.close()
        print("\nDatabase connection closed.")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == '__main__':
    create_tables() 