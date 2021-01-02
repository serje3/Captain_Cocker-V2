import asyncio
from settings import DATABASE_TYPE
import discord
from discord.ext import commands
from pafy import new
from fast_youtube_search import search_youtube
from utils import change_role_bot, add_role_to_bot, parse_duration
from dataQueries import ManageDB, ManagePostgreDB
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
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()


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
        emd=discord.Embed(title=video.title,colour=0x36faff).set_author(name=video.author).set_footer(text=f"Продолжительность - {video.duration}").set_image(url=video.bigthumbhd)

        await ctx.send(embed=emd)
        # change color and name
        # await change_role_bot(player_title, self.bot, ctx, 'play')
        return player_title

    @commands.command()
    async def spotify(self,ctx, member=None):
        if member is not None:
            spotify_song = discord.utils.get(member.activities,name='Spotify')
        else:
            spotify_song = discord.utils.get(ctx.author.activities,name='Spotify')

        if spotify_song is not None:
            await self.play(ctx=ctx,url=f"{spotify_song.title} - {spotify_song.artist}")
        else:
            await ctx.send("Вы ничего не слушаете в Spotify\n(Или нет интеграции Discord с Spotify)")



    # @commands.Cog.listener(name='on_member_update')
    # async def update_member(self,before,after):
    #     print('yes')

    @commands.command()
    async def volume(self, ctx, volume: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Не присоединено к голосовому чату")

        ctx.voice_client.source.volume = volume / 100

        await ctx.send("Громкость: {}%".format(volume))




    @commands.command()
    async def golosovanie(self, ctx):
        await self.play(self,ctx, url="https://www.youtube.com/watch?v=dhhTNEJbEQ4")
        time_code = [4,4.1,3.9,4,4,4,2.9,10.6,4,8,8,8,8,8,8]
        gif_urls = ["https://tenor.com/view/flick-esfand-esfandtv-ricardo-milos-ricardo-flick-gif-13730968",
                    "https://tenor.com/view/ponasenkov-%d0%bf%d0%be%d0%bd%d0%b0%d1%81%d0%b5%d0%bd%d0%ba%d0%be%d0%b2-%d1%82%d0%b0%d0%bd%d0%b5%d1%86-%d0%bc%d0%b0%d1%8d%d1%81%d1%82%d1%80%d0%be-dance-gif-15552318",
                    "https://tenor.com/view/gachi-gachimuchi-karate-gif-13510787",
                    "https://tenor.com/view/senjougahara-monogatari-series-anime-gif-gif-15534766",
                    "https://tenor.com/view/gabkini-twitchitalia-gif-14901405",
                    "https://tenor.com/view/im-gaxi-gaxi-the-real-im-gaxi-ethan-tremblay-ethan-gif-14071428",
                    "https://tenor.com/view/pepega-pls-xqc-dance-pepega-dance-pepe-pls-pepega-gif-16147647",
                    "https://tenor.com/view/gachi-gachi-hyper-gif-15959866",
                    "https://tenor.com/view/gachiw-gachi-gachibass-billy-herrington-gif-16079041",
                    "https://tenor.com/view/%d0%bf%d0%be%d0%bd%d0%b0%d1%81%d0%b5%d0%bd%d0%ba%d0%be%d0%b2-%d1%82%d0%b0%d0%bd%d0%b5%d1%86-%d0%b3%d0%b5%d0%bd%d0%b8%d0%b9-%d0%bc%d0%b0%d1%8d%d1%81%d1%82%d1%80%d0%be-punch-gif-15552297",
                    "https://tenor.com/bdp13.gif",
                    "https://tenor.com/view/ricardo-flick-dance-weekend-vibe-gif-13753340",
                    "https://tenor.com/view/gachi-gachimuchi-flex-lets-do-this-gif-16644616",
                    "https://tenor.com/view/knut-hips-shake-gachi-sexy-gif-15908380",
                    "https://media.discordapp.net/attachments/675762801049862206/715649594641350776/5yaH2Fl.gif",
                    "https://tenor.com/view/gachi-ricardo-milos-dance-gif-13294294",
                    ]
        for i in range(len(gif_urls)):
            await ctx.send(gif_urls[i])
            await asyncio.sleep(time_code[i])

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
        # await change_role_bot('Музыка', self.bot, ctx, 'stop')

    @staticmethod
    @spotify.before_invoke
    @golosovanie.before_invoke
    @play.before_invoke
    # @stop.before_invoke
    async def ensure_voice(ctx):
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
        if (DATABASE_TYPE):
            self.database = ManagePostgreDB()
        else:
            self.database = ManageDB()
        self.ensure_voice = Music(self.bot).ensure_voice

    @commands.command()
    async def showList(self, ctx):
        List = self.database.select(ctx.guild.id)
        msg = []
        if List:
            embed = discord.Embed(title="Список треков", description="Чтобы добавить в список - /add <название>",
                                  color=0xff0000)
            embed.set_author(name="Плейлист")
            for song in List:
                msg.append(f"{song[0]} - {song[1]}\n")
                embed.add_field(name=song[1], value=f"ID {song[0]}", inline=False)
            embed.set_footer(text=f"Количество: {len(List)} треков")
            await ctx.send(embed=embed)
            result = msg
        else:
            await ctx.send('Не найдено')
            result = ['Не найдено',]
        return '\n'.join(result)
    @commands.command()
    async def playlist(self, ctx, _id=1):
        song_list = self.database.select(ctx.guild.id)
        await ctx.send(embed=discord.Embed(title='Играет плейлист',color=0x94ffe4,description=f"Плейлист из {len(song_list)} треков"))
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

            # await change_role_bot(video.title, self.bot, ctx, type='play', playlist=True, playlist_id=id)
            await ctx.send(embed=discord.Embed(title=video.title,description=f"Плейлист ID {id}",color=0x00ffbf).set_image(url=video.bigthumbhd).set_author(name=video.author).set_footer(text=f"Продолжительность - {video.duration}"))
            await asyncio.sleep(parse_duration(video.duration))


        # await change_role_bot('Музыка', self.bot, ctx, type='stop')

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
        print(list)
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
        await self.ensure_voice(ctx)



class Main(commands.Bot):
    def __init__(self, command_prefix, token,intents):
        super().__init__(command_prefix=command_prefix, intents=intents)
        self.token = token
        self.__method_list = []
        self.__method_dict = {}


    def __get_function_mapping(self):
        if self.__method_list == []:
            class_method_list = [cog.get_commands() for cog in self.cogs.values()]
            for method_list in range(len(class_method_list)):
                self.__method_list += class_method_list.pop(0)
        if self.__method_dict == {}:
            for method in self.__method_list:
                self.__method_dict[method.name.lower()]=method
        return self.__method_dict

    def insert_cogs(self, *cogs):
        for cog in cogs:
            self.add_cog(cog)

    async def on_ready(self):
        print('[Python][Discord]Logged on as', self.user)
        print('-------------')
        # msg = await self.wait_for("INTERACTION_CREATE")
        # print(msg)


    async def on_interaction_create(self,member,channel,command):

        async def ensure_voice(ctx):
            if ctx.voice_client is None:
                if member.voice:
                    await member.voice.channel.connect()
                else:
                    await ctx.send("Вы не присоединены к голосовому чату.")
                    raise commands.CommandError("Пользователь не присоединён к голосовому чату.")
            elif ctx.voice_client.is_playing():
                ctx.voice_client.stop()

        ctx = await self.get_context(await channel.fetch_message(channel.last_message_id))
        method_map = self.__get_function_mapping()
        command_name = command['name']

        if command_name in ['play', 'playlist', 'spotify', 'next','golosovanie']:
            await ensure_voice(ctx)

        try:
            options = command['options'][0]

            if command_name=='join':
                await method_map[command_name](ctx,channel=channel.guild.get_channel(int(options['value'])))
            elif command_name=='play':
                await method_map[command_name](ctx,url=options['value'])
            elif command_name=='playlist':
                await method_map[command_name](ctx,_id=options['value'])
            else:
                await method_map[command_name](ctx,options['value'])
        except KeyError:
            if command_name == 'spotify':
                await method_map[command_name](ctx,member=member)
            else:
                await method_map[command_name](ctx)


    async def on_guild_join(self, guild):
        await guild.system_channel.send("Приветствую!\n Для информации напиши !info")
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
