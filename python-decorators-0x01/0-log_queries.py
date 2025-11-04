#!/usr/bin/env python3
import sqlite3
import functools

def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # get query argument from either args or kwargs
        # because some might pass like fetch_all_users("SELECT ...")
        # or fetch_all_users(query="SELECT ...")
        query = kwargs.get('query') if 'query' in kwargs else args[0]
        print(f"Executing Query: {query}")
        return func(*args, **kwargs)
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


# fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
