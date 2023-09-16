import threading
import time

from database_connection import DatabaseConnection


# Define a class for managing a pool of database connections
class DatabaseConnectionPoolManager:
    # Constructor for initializing the connection pool manager
    def __init__(self, time_limit):
        # Number of initial connections to create
        self.starting_conns = 5
        # Maximum number of connections allowed in the pool
        self.max_connections = 50

        # Create a list of initial connections
        self.connections = [DatabaseConnection().conn_info() for _ in range(self.starting_conns)]

        # Record the time of initialization
        self.initialization_time = time.time()
        # Record the current working time
        self.working_time = self.initialization_time
        # Set a time limit for running the connection manager
        self.time_limit = time_limit

        # Number of connections realized (acquired from the pool)
        self.connections_realised = 0

        # Boolean flag to control the main loop
        self.run = True

        # Semaphore to limit the number of concurrent connections
        self.semaphore = threading.Semaphore(self.max_connections)

        # Create a thread for managing connections
        self.thread = threading.Thread(target=self._connection_loop)
        self.thread.daemon = True
        self.thread.start()

    # Method for acquiring a new connection from the pool
    def start_new_connection(self):
        inactive_conn = None
        with self.semaphore:
            for conn in self.connections:
                if not conn.active:
                    inactive_conn = conn
                    break
            if not inactive_conn and len(self.connections) >= self.max_connections:
                return None

            if not inactive_conn:
                new_conn = DatabaseConnection().conn_info()
                new_conn.active = True
                self.connections.append(new_conn)
                return new_conn.connection

            new_conn = inactive_conn
            new_conn.active = True

            return new_conn.connection

    # Method for returning a connection back to the pool
    def return_connection_to_pool(self, connection):
        conn = None
        with self.semaphore:
            for conn_info in self.connections:
                if conn_info.connection is connection:
                    conn = conn_info
                    break
            if conn:
                conn.active = False
                self.connections_realised += 1

    # Method for closing all connections in the pool
    def close_all_connections(self):
        with self.semaphore:
            self.run = False
            for conn in self.connections:
                conn.connection.close()
            self.connections.clear()

    # Private method running in a separate thread to manage connections
    def _connection_loop(self):
        while self.run:
            with self.semaphore:
                # Find inactive connections and remove excess ones
                inactive_conns = [conn for conn in self.connections if not conn.active]
                connections_to_remove = inactive_conns[5:]
                for conn in connections_to_remove:
                    conn.connection.close()
                    self.connections.remove(conn)

                # Print connection pool information
                print(f"""Time from start: {round(time.time() - self.initialization_time, 2)}
Realized connections: {self.connections_realised}
Active connections: {len(self.connections)}
""")

            # Sleep for 60 seconds before checking again
            time.sleep(60)

            # Check if the time limit has been reached and stop if needed
            if self.time_limit:
                self.working_time = time.time() - self.initialization_time
                if self.time_limit < self.working_time:
                    self.run = False
