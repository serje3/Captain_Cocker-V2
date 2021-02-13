import discord
from discord.ext.commands.errors import MissingPermissions
import asyncio

databases = {
    'postgres': 1,
    'sqlite': 0
}


def get_bot(bot, ctx):
    return bot.get_guild(ctx.message.guild.id).get_member(716041669384077343)


def get_color(type):
    if type == 'play':
        return 0x36faff
    elif type == 'stop':
        return 0x3a989b


def get_hoist(type):
    if type == 'play':
        return True
    elif type == 'stop':
        return False


async def change_role_bot(player_title, bot, ctx, type, playlist=False, playlist_id=-1):
    Bot = get_bot(bot, ctx)
    if len(Bot.roles) > 1:
        color = get_color(type)
        hoist = get_hoist(type)

        try:
            if playlist:
                await Bot.roles[1].edit(name=f"Плейлист ID {playlist_id}", color=color, hoist=hoist)
                return
            await Bot.roles[1].edit(
                name=player_title,
                color=color,
                hoist=hoist,
                permissions=discord.Permissions.manage_roles)
        except MissingPermissions:
            return


async def add_role_to_bot(guild, role):
    bot = guild.get_member(716041669384077343)
    await bot.add_roles(role)


def parse_duration(duration):
    hours, minutes, seconds = map(int, duration.split(':'))
    return (hours * 60 * 60) + (minutes * 60) + seconds


class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set()  # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.ctx.voice_client
        return player.is_playing()

    @property
    def player(self): #верно
        return self.current.song

    async def skip(self):
        if self.voice is None or self.current is None:
            if not self.current is None:
                await self.current.ctx.author.send("Команда не выполнена, вы не подключены к голосовому чату")
            return False
        if self.current.ctx.voice_client.is_playing():
            self.current.ctx.voice_client.stop()

    def toggle_next(self,error=None):

        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            emd = self.current.get_emd()
            await self.current.ctx.send(embed=emd)
            self.current.ctx.voice_client.play(self.current.song,after=self.toggle_next)
            await self.play_next_song.wait()

