import psycopg2

mydb = psycopg2.connect(
    host="localhost",
    port=4321,
    database="location_service",
    user="thanhpv",
    password="22121992"
)
