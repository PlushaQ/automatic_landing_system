import time

from database_connection_pool import DatabaseConnectionPoolManager


class AirportDatabase:
    def __init__(self, database, time_limit=None):
        # Initialize the ClientServerDatabase object

        self.db_conn_pool = DatabaseConnectionPoolManager(time_limit)
        # Create a DatabaseConnection object with the specified database

        # Create DB if it's empty
        self.create_db_if_not_exist()

    def close_connections(self):
        # Function closing all connections in pool
        self.db_conn_pool.close_all_connections()

    def db_query(self, sql_query, params=None):
        # Query handler, main purpose of this function is starting connections and returning data from DB
        conn = None
        try:
            conn = self.db_conn_pool.start_new_connection()
            if conn is None:
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
                print(f'Exception during getting making query: {e}')
                self.db_conn_pool.return_connection_to_pool(conn)
            else:
                return data

    def create_db_if_not_exist(self):
        # Create the 'users' table if it doesn't exist
        queries = ["None"]

        for query in queries:
            self.db_query(query)
