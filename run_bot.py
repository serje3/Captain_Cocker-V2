import asyncio
import settings
import discord
from discord.ext import commands
from app import Main, Music, SongList
from dataQueries import ManageDB
from aiohttp import web
import json

bot = Main("!", settings.TOKEN)
bot.insert_cogs(Music(bot))
bot.insert_cogs(SongList(bot))


class VkBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ctx = None
        self.database = ManageDB()
        self.music = Music(bot)
        self.music2 = Music(self.bot)
        self.play = self.music2.play
        self.songlist = SongList(bot)
        self.command_list = [
            'join',
            'play',
            'volume',
            'stop',
            'golosovanie',
            'playlist',
            'showList',
            'add',
            'drop',
        ]

    async def execute_command(self, args):

        await self.fetch_context()

        command = args[0]
        if command == 'join':
            room = " ".join(args[1:])

            await self.music.join(self, ctx=self.ctx,
                                  channel=discord.utils.get(self.bot.get_all_channels(), guild__id=727987809050165330,
                                                            name=room))
            return f"Подключён к голосовому каналу {' '.join(args[1:])}"
        elif command == 'play':
            player_title = await self.music.play(self, ctx=self.ctx, url=" ".join(args[1:]))
            return f"Сейчас играет: {player_title}"
        elif command == 'stop':
            await self.music.stop(self, self.ctx)
            return f"Отключён от голосового канала"
        elif command == 'volume':
            await self.music.volume(self, self.ctx, int(args[1]))
            return f"Изменена громкость на {args[1]}"
        elif command == 'golosovanie':
            await self.music.golosovanie(self, self.ctx)
            return "ГОЛОСОВАНИЕ"
        elif command == 'showList':
            result = await self.songlist.showList(self, self.ctx)
            return result
        elif command == 'playlist':
            if (len(args) == 1):
                await self.songlist.playlist(self, self.ctx)
                return "Играет плейлист"
            elif (len(args) >= 1):
                await self.songlist.playlist(self, self.ctx, _id=args[1])
        elif command == 'next':
            await self.songlist.next(self, self.ctx)
        elif command == 'add':
            print(args[1:])
            await self.songlist.add(self, self.ctx, args[1:])
            return "Аудиозаписи добавлены в базу"
        elif command == 'drop':
            if args[1] == 'all':
                await self.songlist.drop(self, self.ctx, ['all'])
                return "Удалено всё"
            elif len(args) > 1:
                await self.songlist.drop(self, self.ctx, args[1:])
                return f"Удалены {', '.join(args[1:])}"

    async def fetch_context(self):

        channel = self.bot.get_guild(727987809050165330).system_channel  # get_guild(guild_id)

        try:

            message = await channel.fetch_message(channel.last_message_id)  # fetch_message(message_id)
        except:
            message = await channel.fetch_message(778045147602092042)

        context = await self.bot.get_context(message)

        self.ctx = context

    async def webserver(self):
        async def handler(request):
            return web.Response(text="Hello, world")

        async def command(request):
            try:
                if (request.query['authkey'] == settings.AUTHKEY):
                    content = await request.json()
                    print(content)
                    msg = ""
                    if (content['command'][0] in self.command_list):
                        msg = await self.execute_command(content['command'])

                    response_obj = {'status': 'success', 'message': msg}

                    return web.Response(text=json.dumps(response_obj), status=200)
                else:
                    raise Exception
            except Exception as e:
                response_obj = {'status': 'failed', 'message': str(e)}
                return web.Response(text=json.dumps(response_obj), status=500)

        app = web.Application()
        app.router.add_get('/', handler)
        app.router.add_post('/event', command)
        runner = web.AppRunner(app)
        await runner.setup()
        self.site = web.TCPSite(runner, '0.0.0.0', 8999)
        await self.bot.wait_until_ready()
        await self.site.start()

    def __unload(self):
        asyncio.ensure_future(self.site.stop())


vkbot = VkBot(bot)

bot.insert_cogs(vkbot)

bot.loop.create_task(vkbot.webserver())

bot.run_bot()
