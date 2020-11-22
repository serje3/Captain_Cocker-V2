import sqlite3


class ManageDB:
    def __init__(self):
        self.conn = sqlite3.connect('songsList.db')

        cursor = self.conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS songs(
                           id INTEGER PRIMARY KEY NOT NULL ,
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
        cursor.executemany("""INSERT INTO songs(song,guild) VALUES(?,?)""", arr)
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
        result = cursor.execute("""SELECT * FROM now_song WHERE guild=:guild""",{"guild":guild_id})
        fetch = result.fetchall()
        if len(fetch) == 0:
            cursor.execute("""INSERT INTO now_song(id,guild) VALUES (?,?)""",(song_id,guild_id))
        else:
            cursor.execute("""UPDATE now_song SET id = ?, guild= ? WHERE guild=?""", (song_id, guild_id,guild_id))
        self.conn.commit()
        cursor.close()

    def get_now_playing(self,guild_id):
        cursor = self.conn.cursor()
        cursor.execute("""SELECT * FROM now_song WHERE guild=:guild""",{"guild":guild_id})
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

# tests
# cursor = ManageDB()
# cursor.insert([('song',623452),('song2',623452),('song3',623452)])
# print(cursor.select(623452))
# [(1, 'song', 623452), (2, 'song2', 623452), (3, 'song3', 623452), (4, 'song4', 623452)]
# cursor.drop([3,4,5])
