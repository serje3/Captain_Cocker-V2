from app import Main, Music, SongList

bot = Main("!",'NzE2MDQxNjY5Mzg0MDc3MzQz.XtF_xQ.7VIHSMyG0Cx8fQLLCQ9X5STKw8I')
bot.insert_cogs(Music(bot))
bot.insert_cogs(SongList(bot))
bot.run_bot()
