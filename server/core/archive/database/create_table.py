from numpy import dot
from math import sqrt

from db import conn

def calculate_cosine_similarity(vector1, vector2) -> float:
    numerator = dot(vector1, vector2)
    denominator = sqrt(dot(vector1, vector1)) * sqrt(dot(vector2, vector2))
    return numerator / denominator




# with conn.cursor() as cur:
#     # cur.execute(
#     #     "CREATE TABLE test (id serial PRIMARY KEY, num double precision, vector double precision[]);"
#     # )

#     # cur.execute(
#     #     "INSERT INTO test (num, vector) VALUES (%s, %s)",
#     #     (arr[0], arr)
#     # )
#     conn.commit()

# Execute a query
# Retrieve query results
with conn.cursor() as cur:
    cur.execute("SELECT num, vector FROM test;")
    records = cur.fetchall()

records = records[0]
print(records)

# cur.close()
conn.close()