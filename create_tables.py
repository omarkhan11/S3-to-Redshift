import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
    Drops tables in the database using queries from `drop_table_queries`.

    Args:
        cur (psycopg2.extensions.cursor): Database cursor.
        conn (psycopg2.extensions.connection): Database connection.

    Raises:
        Exception: If an error occurs during table deletion.
    """
    try:
        for query in drop_table_queries:
            cur.execute(query)
            conn.commit()
    except Exception as e:
        print(e)


def create_tables(cur, conn):
    """
    Creates tables in the database using queries from `create_table_queries`.

    Args:
        cur (psycopg2.extensions.cursor): Database cursor.
        conn (psycopg2.extensions.connection): Database connection.

    Raises:
        Exception: If an error occurs during table creation.
    """
    try:
        for query in create_table_queries:
            cur.execute(query)
            conn.commit()
    except Exception as e:
        print(e)   
        

def main():
    """
    Establishes database connection, drops existing tables, and creates new ones.

    Args:
        None

    Returns:
        None

    Raises:
        Exception: If an error occurs during connection or query execution.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
