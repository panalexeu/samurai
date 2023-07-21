import sqlite3
import os


class SavesDatabase:
    DB_PATH = "saves.db"

    PLAYER_POSITION_TABLE = """
        CREATE TABLE player_position(
            pos_x INTEGER,
            pos_y INTEGER   
        )
    """

    GET_PLAYER_POSITION = "SELECT * FROM player_position"
    INIT_PLAYER_POSITION = "INSERT INTO player_position VALUES(100, 0)"
    SET_PLAYER_POSITION = "UPDATE player_position SET pos_x = ?, pos_y = ?"

    def get_player_position(self):
        return self.run_query(query=self.GET_PLAYER_POSITION, fetch=True)[0]

    def set_player_position(self, pos_x, pos_y):
        return self.run_query(query=self.SET_PLAYER_POSITION, args=(pos_x, pos_y), commit=True)

    def run_query(self, query, args=None, commit=False, fetch=False):
        args = args or ()
        fetched_data = None

        with self.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute(query, args)

            if commit:
                connection.commit()
            if fetch:
                fetched_data = cursor.fetchall()

        return fetched_data

    def db_exists(self):
        return os.path.exists(self.DB_PATH)

    def get_connection(self):
        return sqlite3.connect(self.DB_PATH)

    def initialize(self):
        if self.db_exists():
            return

        with self.get_connection() as connection:
            cursor = connection.cursor()

            cursor.execute(self.PLAYER_POSITION_TABLE)
            cursor.execute(self.INIT_PLAYER_POSITION)

            connection.commit()
