# Python Generators - Project 0x00

This project introduces the concept of Python generators and how they can be used to handle large datasets efficiently. Generators allow data to be loaded lazily rather than all at once, which helps improve performance and memory usage especially in data intensive applications.

## Task 0 - Getting Started with Python Generators

In this task, a MySQL database named **ALX_prodev** is created. A table `user_data` is defined with the fields:

- user_id (UUID, Primary Key)
- name (VARCHAR, NOT NULL)
- email (VARCHAR, NOT NULL)
- age (DECIMAL, NOT NULL)

The database is then seeded with sample data from `user_data.csv`.

### Files

- `seed.py` - Contains all required database functions.
- `0-main.py` - Tests creation of DB, table and data loading.

### Requirements

- Python 3.x
- MySQL
- mysql-connector-python

### How to run

```bash
./0-main.py
