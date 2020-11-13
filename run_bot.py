from app import Main, Music, SongList

bot = Main("!",'NzE2MDQxNjY5Mzg0MDc3MzQz.XtF_xQ.2GLCc2jiaY58iOCEfbp_zOgaz2s')
bot.insert_cogs(Music(bot))
bot.insert_cogs(SongList(bot))
bot.run_bot()
