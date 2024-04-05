import hashlib
import logging
import os
import sqlite3

from datetime import datetime

SALT = os.environ.get("SALT", "some_random_salt")

def find(username):
    """
    Method expected to be used for login
    """
    conn = sqlite3.connect('transcripts.db')
    cursor = conn.cursor()

    query = '''
    SELECT username, password, approved
    FROM users
    WHERE username = ? 
    '''

    cursor.execute(query, (username,))
    row = cursor.fetchone()
    if row is None:
        return None

    user = {}
    user["username"] = row[0]
    user["password"] = row[1]
    user["approved"] = row[2]

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return user

def listNotApproved():
    """
    Method expected to be used by admin to list all the not approved users
    """
    conn = sqlite3.connect('transcripts.db')
    cursor = conn.cursor()

    query = '''
    SELECT username
    FROM users
    WHERE approved = 0
    '''

    cursor.execute(query)
    rows = cursor.fetchall()

    users = []
    for row in rows:
        users.append(row[0])

    # Close the cursor and connection
    cursor.close()
    conn.close()

    return users

def create(username, password):
    """
    When a new user creates an account, create method is expected to be called
    """
    conn = sqlite3.connect('transcripts.db')
    cursor = conn.cursor()

    current_datetime = datetime.now()
    hashed_salted_pwd = hashPassword(password)
    data_to_insert = (username, hashed_salted_pwd, current_datetime.strftime('%Y-%m-%d %H:%M:%S'))

    insert_query = '''
        INSERT INTO users (username, password, created_at)
        VALUES (?, ?, ?)
    '''

    # Execute the INSERT statement with the data to insert
    cursor.execute(insert_query, data_to_insert)

    # Commit the transaction (save changes)
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

def hashPassword(password):
    hashed_salted_pwd = hashlib.sha256("{}_{}".format(password, SALT).encode()).hexdigest()
    return hashed_salted_pwd

def setApproved(username):
    """
    When the admin approves the user, the setApproved method is expected to be called
    """
    conn = sqlite3.connect('transcripts.db')
    cursor = conn.cursor()

    data_to_update = (username,)

    update_query = '''
        UPDATE users SET approved = 1 WHERE username = ? 
    '''

    # Execute the UPDATE statement with the data to update
    cursor.execute(update_query, data_to_update)

    # Commit the transaction (save changes)
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

def removeUser(username):
    """
    When the admin rejects the user, it gets removed
    """
    conn = sqlite3.connect('transcripts.db')
    cursor = conn.cursor()

    data_to_remove = (username,)

    update_query = '''
        DELETE FROM users WHERE username = ?
    '''

    # Execute the INSERT statement with the data to insert
    cursor.execute(update_query, data_to_remove)

    # Commit the transaction (save changes)
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()

