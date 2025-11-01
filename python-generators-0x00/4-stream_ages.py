
seed = __import__('seed')

def stream_user_ages():
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']
    connection.close()


def average_age():
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    avg = total / count if count > 0 else 0
    print(f"Average age of users: {avg}")


if __name__ == "__main__":
    average_age()
