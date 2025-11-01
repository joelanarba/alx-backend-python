
import mysql.connector

def stream_users_in_batches(batch_size):
    """Yield lists of rows (batches) from user_data."""
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="ALX_prodev"
    )

    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data;")

    batch = []
    for row in cursor:          # loop 1
        batch.append(row)
        if len(batch) == batch_size:
            yield batch
            batch = []

    if batch:
        yield batch

    cursor.close()
    conn.close()


def batch_processing(batch_size):
    """
    Generator that yields users older than 25 from the DB in batches.
    Use like: for user in batch_processing(50): print(user)
    """
    for batch in stream_users_in_batches(batch_size):  # loop 2
        for user in batch:                             # loop 3
            if user['age'] > 25:
                yield user
