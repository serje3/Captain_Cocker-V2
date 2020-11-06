from app import Main, Music, SongList

bot = Main("!",'TOKEN')
bot.insert_cogs(Music(bot))
bot.insert_cogs(SongList(bot))
bot.run_bot()
