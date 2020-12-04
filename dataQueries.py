import sqlite3
import psycopg2
from urllib.parse import urlparse
from settings import DATABASE_TYPE, DATABASE_CONF
from utils import databases


class ManageDB:
    """Manager for sqlite3 db"""

    def __init__(self):

        self.conn = sqlite3.connect('songsList.db')
        print('[SQLITE3] DATABASE CONNECTED')
        cursor = self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS songs(
                           id INTEGER NOT NULL ,
                           song text NOT NULL,
                           guild INTEGER NOT NULL
        );""")
        self.conn.commit()
        cursor.execute("""CREATE TABLE IF NOT EXISTS now_song(
                                   id INTEGER NOT NULL,
                                   guild INTEGER PRIMARY KEY NOT NULL
                );""")
        self.conn.commit()
        cursor.close()

    def insert(self, arr):
        cursor = self.conn.cursor()
        if arr == []:
            return
        cursor.execute("""SELECT * FROM songs WHERE guild=:guild_id""", {'guild_id': arr[0][1]})
        result = cursor.fetchall()
        print(result)
        if result == []:
            lastId = 0
        else:
            lastId = result[::-1][0][0]
        print(lastId)
        values = []
        for k, v in arr:
            lastId += 1
            values.append((lastId, k, v))
        cursor.executemany("""INSERT INTO songs(id,song,guild) VALUES(?, ?,?)""", values)
        self.conn.commit()
        cursor.close()

    def select(self, guild_id):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * FROM songs WHERE guild=:guild_id""", {'guild_id': guild_id})
        result = cursor.fetchall()
        cursor.close()
        return result

    def set_now_playing(self, song_id, guild_id):
        cursor = self.conn.cursor()
        result = cursor.execute("""SELECT * FROM now_song WHERE guild=:guild""", {"guild": guild_id})
        fetch = result.fetchall()
        if len(fetch) == 0:
            cursor.execute("""INSERT INTO now_song(id,guild) VALUES (?,?)""", (song_id, guild_id))
        else:
            cursor.execute("""UPDATE now_song SET id = ?, guild= ? WHERE guild=?""", (song_id, guild_id, guild_id))
        self.conn.commit()
        cursor.close()

    def get_now_playing(self, guild_id):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * FROM now_song WHERE guild=:guild""", {"guild": guild_id})
        result = cursor.fetchall()
        cursor.close()
        return result

    def drop(self, id_arr, guild):
        cursor = self.conn.cursor()
        for _id in id_arr:
            cursor.execute("""DELETE FROM songs WHERE id=:id and guild=:guild_id""", {'id': _id, 'guild_id': guild})
            self.conn.commit()
        cursor.close()

    def close_connection(self):
        self.conn.close()


class ManagePostgreDB():
    """Manager for PostgreSql db"""

    def __init__(self):
        super().__init__()
        data = urlparse(DATABASE_CONF)
        self.conn = psycopg2.connect(database=data.path[1:],
                                     user=data.username,
                                     password=data.password,
                                     host=data.hostname, )
        print('[POSTGRESQL] DATABASE CONNECTED')

        cursor = self.conn.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS songs(
                                   id INTEGER NOT NULL ,
                                   song text NOT NULL,
                                   guild BIGINT NOT NULL
                );""")
        self.conn.commit()
        cursor.execute("""CREATE TABLE IF NOT EXISTS now_song(
                                           id INTEGER NOT NULL,
                                           guild BIGINT PRIMARY KEY NOT NULL
                        );""")
        self.conn.commit()
        cursor.close()


    def insert(self, arr):
        cursor = self.conn.cursor()
        if arr == []:
            return
        cursor.execute("""SELECT * FROM songs WHERE guild=%(guild_id)s""", {'guild_id': arr[0][1]})
        result = cursor.fetchall()
        if result == []:
            lastId = 0
        else:
            lastId = result[::-1][0][0]
        print(lastId)
        values = []
        for k, v in arr:
            lastId += 1
            values.append((lastId, k, v))
        cursor.executemany("""INSERT INTO songs(id,song,guild) VALUES(%s, %s,%s)""", values)
        self.conn.commit()
        cursor.close()

    def select(self, guild_id):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * FROM songs WHERE guild=%(guild_id)s""", {'guild_id': guild_id})
        result = cursor.fetchall()
        cursor.close()
        return result

    def set_now_playing(self, song_id, guild_id):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * FROM now_song WHERE guild=%(guild)s""", {"guild": guild_id})
        fetch = cursor.fetchall()
        if len(fetch) == 0:
            cursor.execute("""INSERT INTO now_song(id,guild) VALUES (%s,%s)""", (song_id, guild_id))
        else:
            cursor.execute("""UPDATE now_song SET id = %s, guild= %s WHERE guild=%s""", (song_id, guild_id, guild_id))
        self.conn.commit()
        cursor.close()

    def get_now_playing(self, guild_id):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * FROM now_song WHERE guild=%(guild)s""", {"guild": guild_id})
        result = cursor.fetchall()
        cursor.close()
        return result

    def drop(self, id_arr, guild):
        cursor = self.conn.cursor()
        for _id in id_arr:
            cursor.execute("""DELETE FROM songs WHERE id=%(id)s and guild=%(guild_id)s""", {'id': _id, 'guild_id': guild})
            self.conn.commit()
        cursor.close()

    def close_connection(self):
        self.conn.close()


# tests
# cursor = ManageDB()
# cursor.insert([('song',623452),('song2',623452),('song3',623452)])
# print(cursor.select(623452))
# [(1, 'song', 623452), (2, 'song2', 623452), (3, 'song3', 623452), (4, 'song4', 623452)]
# cursor.drop([3,4,5])
