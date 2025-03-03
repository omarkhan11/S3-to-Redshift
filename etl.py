import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


def load_staging_tables(cur, conn):
    """
    Loads data into staging tables using queries from `copy_table_queries`.

    Args:
        cur (psycopg2.extensions.cursor): Database cursor.
        conn (psycopg2.extensions.connection): Database connection.

    Raises:
        Exception: If an error occurs during data loading.
    """
    try:
        for query in copy_table_queries:
            cur.execute(query)
            conn.commit()
    except Exception as e:
        print(e)


def insert_tables(cur, conn):
    """
    Inserts data into tables using queries from `insert_table_queries`.

    Args:
        cur (psycopg2.extensions.cursor): Database cursor.
        conn (psycopg2.extensions.connection): Database connection.

    Raises:
        Exception: If an error occurs during data insertion.
    """
    try:
        for query in insert_table_queries:
            cur.execute(query)
            conn.commit()
    except Exception as e:
        print(e)


def main():
    """
    Establishes database connection, loads staging tables, and inserts data.

    Args:
        None

    Returns:
        None

    Raises:
        Exception: If an error occurs during connection or query execution.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port    {}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
