import sqlite3
import logging
from datetime import datetime

def find(hash_str):
    conn = sqlite3.connect('transcripts.db')
    cursor = conn.cursor()

    query = '''
    SELECT transcript
    FROM transcripts
    WHERE sha256 = ?
    '''

    cursor.execute(query, (hash_str,))
    rows = cursor.fetchall()

    transcript = ""
    found = False
    logger = logging.getLogger()
    for row in rows:
        logger.info("found transcript")
        transcript = row
        found = True

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return transcript, found

def insert(file_name, transcript, hash_str):
    conn = sqlite3.connect('transcripts.db')
    cursor = conn.cursor()

    current_datetime = datetime.now()
    data_to_insert = (file_name, transcript, current_datetime.strftime('%Y-%m-%d %H:%M:%S'), hash_str)

    insert_query = '''
        INSERT INTO transcripts (file_name, transcript, created_at, sha256)
        VALUES (?, ?, ?, ?)
    '''

    # Execute the INSERT statement with the data to insert
    cursor.execute(insert_query, data_to_insert)

    # Commit the transaction (save changes)
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()
