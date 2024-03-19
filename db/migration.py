import sqlite3

def migrate():
    # Connect to SQLite database (creates a new database if it doesn't exist)
    conn = sqlite3.connect('transcripts.db')

    # Create a cursor object to execute SQL commands
    cursor = conn.cursor()

    # Define SQL statement to create a table
    create_table_sql = '''
        CREATE TABLE IF NOT EXISTS transcripts (
            id INTEGER PRIMARY KEY,
            file_name TEXT NOT NULL,
            transcript TEXT NOT NULL,
            created_at DATETIME,
            sha256 TEXT NOT NULL UNIQUE
        )
    '''

    # Execute the SQL statement to create the table
    cursor.execute(create_table_sql)

    # Commit the transaction (save changes)
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

