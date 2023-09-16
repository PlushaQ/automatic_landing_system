import threading
import time

from database_connection import DatabaseConnection


class DatabaseConnectionPoolManager:
    def __init__(self, time_limit):
        self.starting_conns = 5
        self.max_connections = 50

        self.connections = [DatabaseConnection().conn_info() for _ in range(self.starting_conns)]

        self.initialization_time = time.time()
        self.working_time = self.initialization_time
        self.time_limit = time_limit

        self.connections_realised = 0

        self.run = True

        self.semaphore = threading.Semaphore(self.max_connections)

        self.thread = threading.Thread(target=self._connection_loop)
        self.thread.daemon = True
        self.thread.start()

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

    def close_all_connections(self):
        with self.semaphore:
            self.run = False
            for conn in self.connections:
                conn.connection.close()
            self.connections.clear()

    def _connection_loop(self):
        while self.run:
            with self.semaphore:
                inactive_conns = [conn for conn in self.connections if not conn.active]
                connections_to_remove = inactive_conns[5:]
                for conn in connections_to_remove:
                    conn.connection.close()
                    self.connections.remove(conn)

                print(f"""Time from start: {round(time.time() - self.initialization_time, 2)}
Realised connections: {self.connections_realised}
Active connections: {len(self.connections)}
""")

            time.sleep(60)

            if self.time_limit:
                self.working_time = time.time() - self.initialization_time
                if self.time_limit < self.working_time:
                    self.run = False
                    break
