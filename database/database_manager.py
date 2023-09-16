import time

from database_connection_pool import DatabaseConnectionPoolManager


class AirportDatabase:
    def __init__(self, time_limit=None):
        # Initialize the AirportDatabase object

        # Create a DatabaseConnectionPoolManager object with the specified time limit
        self.db_conn_pool = DatabaseConnectionPoolManager(time_limit)

        # Create DB if it doesn't exist
        self.create_db_if_not_exist()

    def close_connections(self):
        # Method for closing all connections in the connection pool
        self.db_conn_pool.close_all_connections()

    def db_query(self, sql_query, params=None):
        # Database query handler, responsible for managing connections and executing queries
        conn = None
        try:
            conn = self.db_conn_pool.start_new_connection()
            if conn is None:
                # If no available connections, wait and retry
                time.sleep(2)
                return self.db_query(sql_query, params)
        except Exception as e:
            print(f'Exception during getting connection: {e}')
            if conn:
                self.db_conn_pool.return_connection_to_pool(conn)
        else:
            try:
                cursor = conn.cursor()

                cursor.execute(sql_query, params)
                if sql_query.split()[0] == 'SELECT':
                    data = cursor.fetchall()
                else:
                    data = None
                cursor.close()
                self.db_conn_pool.return_connection_to_pool(conn)
            except Exception as e:
                print(f'Exception during making query: {e}')
                self.db_conn_pool.return_connection_to_pool(conn)
            else:
                return data

    def create_db_if_not_exist(self):
        # Create database tables if they don't exist
        queries = ["None"]

        for query in queries:
            self.db_query(query)
