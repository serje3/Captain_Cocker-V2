import asyncio

import discord
from discord.ext import commands
from pafy import new
from fast_youtube_search import search_youtube
from utils import change_role_bot, add_role_to_bot, parse_duration
from dataQueries import ManageDB
import youtube_dl

ffmpeg_opts = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'}

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, url):

        try:
            video = new(url,ydl_opts=ytdl_format_options)
        except ValueError:
            video_id = search_youtube(url.split(' '))[0]['id']
            video = new(video_id,ydl_opts=ytdl_format_options)

        async with ctx.typing():
            audio = video.getbestaudio().url
            ctx.voice_client.play(discord.FFmpegPCMAudio(audio, **ffmpeg_opts))
            ctx.voice_client.is_playing()
        player_title = video.title
        await ctx.send('Сейчас играет: ' + player_title)

        # change color and name
        await change_role_bot(player_title, self.bot, ctx, 'play')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Не присоединено к голосовому чату")

        ctx.voice_client.source.volume = volume / 100

        await ctx.send("Громкость: {}%".format(volume))


    @commands.command()
    async def stop(self, ctx):
        await ctx.voice_client.disconnect()
        await change_role_bot('Музыка', self.bot, ctx, 'stop')

    @staticmethod
    @play.before_invoke
    @stop.before_invoke
    async def ensure_voice(self,ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Вы не присоединены к голосовому чату.")
                raise commands.CommandError("Пользователь не присоединён к голосовому чату.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()


class SongList(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = ManageDB()
        self.ensure_voice = Music(self.bot).ensure_voice
        print('[SUCCESS] DATABASE CONNECTED')

    @commands.command()
    async def showList(self, ctx):
        List = self.database.select(ctx.guild.id)
        if List:
            await ctx.send('id\tНазвание')
            msg = []
            for song in List:
                msg.append(str(song[0]) + '   ' + song[1] + '\n')

            lenList = [len(value) for value in ['hello', ' world']]
            if sum(lenList) <= 2000:
                await ctx.send("".join(msg))
            else:

                a = [value + sum(lenList[:i]) for value, i in [[lenList[i], i] for i in range(len(lenList))] if i != 0]
                indexes = [0]
                for i in range(len(a)):
                    if a[i] - indexes[::-1][0] >= 2000:
                        indexes.append(i)
                for i in indexes:
                    if i == 0:
                        continue
                    await ctx.send("".join(msg[:i]))
                    del msg[:i]
        else:
            await ctx.send('Не найдено')

    @commands.command()
    async def playlist(self, ctx, _id=1):
        song_list = self.database.select(ctx.guild.id)
        await ctx.send("Играет плейлист")
        for id, song, guild in song_list:
            if id < _id:
                continue

            self.database.set_now_playing(id,guild)
            try:
                video_id = search_youtube(song.split(' '))[0]['id']
                video = new(video_id)
            except:
                continue

            async with ctx.typing():
                audio = video.getbestaudio().url
                ctx.voice_client.play(discord.FFmpegPCMAudio(audio, **ffmpeg_opts))
                ctx.voice_client.is_playing()

            await change_role_bot(video.title, self.bot, ctx, type='play', playlist=True, playlist_id=id)
            await ctx.send(f"Плейлист ID {id} - {video.title}")
            await asyncio.sleep(parse_duration(video.duration))


        await change_role_bot('Музыка', self.bot, ctx, type='stop')

    @commands.command()
    async def next(self,ctx):
       await self.playlist(ctx,self.database.get_now_playing(ctx.guild.id)[0][0] + 1)

    @commands.command()
    async def add(self, ctx, *songs):
        guild = ctx.guild.id
        songsList = []
        text = ""
        for song in songs:
            if song[::-1][0] == ',':
                text += song
                songsList.append(text.replace(',', ''))
                text = ""
            else:
                text += song + " "
        if text != "":
            songsList.append(text.replace(',', ''))
        list = [(song, guild) for song in songsList]
        self.database.insert(list)
        await ctx.send(f"Сохранены: {', '.join(songsList)}"[:2000])

    @commands.command()
    async def drop(self, ctx, *_id):
        if _id[0] == 'all':
            list = self.database.select(ctx.guild.id)
            index = list[::-1][0][0]
            toDelete = [i for i in range(1, index + 1)]
            self.database.drop(toDelete, ctx.guild.id)
            await ctx.send("Удалено всё")
        else:
            self.database.drop(_id, ctx.guild.id)
            await ctx.send("Удалено")

    @next.before_invoke
    @playlist.before_invoke
    async def ensure_voice(self,ctx):
        await self.ensure_voice(self,ctx)


class Main(commands.Bot):
    def __init__(self, command_prefix, token):
        super().__init__(command_prefix=command_prefix)
        self.token = token

    def insert_cogs(self, *cogs):
        for cog in cogs:
            self.add_cog(cog)

    async def on_ready(self):
        print('Logged on as', self.user)
        print('-------------')

    async def on_guild_join(self, guild):
        await guild.system_channel.send("Приветствую! Он\n Для информации напиши !info")
        await guild.system_channel.send("https://tenor.com/bhyep.gif")

        if discord.utils.get(guild.roles, name='Музыка') == None:
            await guild.create_role(
                name='Музыка',
                permissions=discord.Permissions().all(),
                colour=discord.Colour(0x3a989b),
                mentionable=True,
                reason="Нужна для отображения статуса бота"
            )

        await add_role_to_bot(guild, discord.utils.get(guild.roles, name='Музыка'))

    def run_bot(self):
        self.run(self.token)
