import psycopg2
import psycopg2.extras
def connect():
    conn = psycopg2.connect(
        host="localhost",             # PostgreSQL server (localhost for local machine)
        dbname="project_bdd",         # Your database name
        user="walid",              # Use the 'postgres' superuser
        password="abcd",                  # No password needed (leave empty)
        port=5432,
        cursor_factory = psycopg2.extras.NamedTupleCursor,
    )
    conn.autocommit = True
    return conn