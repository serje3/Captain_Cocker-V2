import discord
from discord.ext.commands.errors import MissingPermissions


databases = {
    'postgres':1,
    'sqlite':0
}

def get_bot(bot, ctx):
    return bot.get_guild(ctx.message.guild.id).get_member(716041669384077343)


def get_color(type):
    if type == 'play':
        return discord.Colour(0x36faff)
    elif type == 'stop':
        return discord.Colour(0x3a989b)

def get_hoist(type):
    if type == 'play':
        return True
    elif type == 'stop':
        return False

async def change_role_bot(player_title,bot, ctx, type,playlist=False, playlist_id=-1):
    Bot = get_bot(bot, ctx)
    if len(Bot.roles)>1:
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


async def add_role_to_bot(guild,role):
    bot = guild.get_member(716041669384077343)
    await bot.add_roles(role)


def parse_duration(duration):
    hours,minutes,seconds=map(int,duration.split(':'))
    return (hours*60*60)+(minutes*60)+seconds

