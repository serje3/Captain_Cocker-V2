from dataQueries import ManageDB

data = ManageDB()

print(data.get_now_playing(123456))

data.close_connection()