import discord
from discord.ext import commands
import random
from datetime import datetime, date, time, timedelta
import sys
import traceback

# https://discordapp.com/oauth2/authorize?&client_id={bot-id}&scope=bot&permissions=3072&response_type=code
# bot id: get from discord apps website
# permissions (use https://discordapi.com/permissions.html) : Read Messages, Send Messages -> 3072
# scope: bot
# response type: code

description = """I am a simple looking-for-game bot for Soulsborne games.
    Version 1.0.2, released 2016-09-06
    By Gwyndolin-chan (hydra-chan @ github), 2016-08-30
    """
cmd_prefix = '~'
bot = commands.Bot(command_prefix=cmd_prefix, description=description)

# bot_token: substitute the text for the bot's token. DO NOT SHARE.
bot_token = 'text'
# EXAMPLE: bot_token = '01234.some.example.token.56789'

ADMIN_bot_enabled = True # Lock for public functions of the bot

# A Request has the Message used for the request command. Extended with details of the request
class Request:
    def __init__(self, message, game, platform, sl_sm, note=''):
        self.message = message
        self.game = game
        self.platform = platform
        self.sl_sm = sl_sm
        self.note = note

# Players are stored as a list.
RequestList = []
lock_RequestList = False
RequestList_max_size = 100

max_note_length = 100

# Possible games as shorthand and their full name
GameMap = {
            'des'       : 'Demon\'s Souls',
            'ds1'       : 'Dark Souls 1 PTDE',
            'ds1og'     : 'Dark Souls 1 OG',
            'ds2'       : 'Dark Souls 2 SOTFS',
            'ds2og'     : 'Dark Souls 2 OG',
            'ds3'       : 'Dark Souls 3',
            'bb'        : 'Bloodborne',
           }
            
# Possible platforms as shorthand and their full name
PlatformMap = {
               'pc'     : 'PC (Steam)',
               'ps3'    : 'PlayStation 3',
               'ps4'    : 'PlayStation 4',
               'xb360'  : 'XBox 360',
               'xb1'    : 'XBox One',
               'xbo'    : 'XBox One',
              }

@bot.event
async def on_ready():
    global lock_RequestList
    print('Logged in as')
    print('Name:', bot.user.name)
    print('ID:', bot.user.id)
    print('------')
    lock_RequestList = False
    # we should start a periodic background task to clear out old requests...

def ERROR_output_dm(f):
    def dm(c, s, prefix='ERROR: '): # direct message
        return bot.send_message(c.message.author, prefix + s)
    return dm
    
# comment out "@ERROR_output_dm" to make the bot reply to errors in the channel. uncomment for direct message.
#@ERROR_output_dm
def ERROR_output(c, s, prefix='ERROR: '):
    return bot.send_message(c.message.channel, prefix + s)
    
@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.NoPrivateMessage):
        await ERROR_output(ctx, 'This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await ERROR_output(ctx, 'This command is disabled and cannot be used.')
    elif isinstance(error, commands.CommandNotFound):
        await ERROR_output(ctx, 'That command was not found. Type ' + cmd_prefix + 'help if you need help.')
    elif isinstance(error, commands.CommandInvokeError):
        print('In {0.command.qualified_name}:'.format(ctx), file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print('{0.__class__.__name__}: {0}'.format(error.original), file=sys.stderr)
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ERROR_output(ctx, '{0.__name__}: {1} (try: ' + cmd_prefix + 'help {2})'.format(commands.errors.MissingRequiredArgument, error, ctx.message.content.split()[0][1:]))
    else:
        print('Ignoring exception in command "{}"'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

@bot.command(pass_context=True)
async def request(ctx, game : str, platform : str, sl_sm : str, note=''):
    """
    Add yourself to the game request list for one hour
    
    Valid words for <game>: des, ds1, ds1og, ds2, ds2og, ds3, bb
    Valid words for <platform>: pc, ps3, ps4, xb360, xb1, xbo
    For <sl_sm> type your Soul Level, Soul Memory, or one word: ex. '120' or '30mil'
    Optional: [note] that is limited in length. A good place to put 'coop' or 'pvp' or 'Gwyndolin #1 waifu'
    
    Please refrain from impossible combinations like Demon's Souls on XBox One.
    """
    if not ADMIN_bot_enabled:
        return
    global RequestList, lock_RequestList
    # Check for errors in arguments
    errors = 0
    s = ''
    if game not in GameMap.keys():
        errors = errors + 1
        s_k = ''
        for k, e in GameMap.items():
            s_k = s_k + str(k) + ', '
        s = s + '<game> must be one of: ' + s_k + '\n'
    if platform not in PlatformMap.keys():
        errors = errors + 1
        s_k = ''
        for k, e in PlatformMap.items():
            s_k = s_k + str(k) + ', '
        s = s + '<platform> must be one of: ' + s_k + '\n'
    if len(RequestList) >= RequestList_max_size:
        errors = errors + 1
        s = s + 'Request list is already at capacity (' + str(RequestList_max_size) + ')' + '\n'
    if errors > 0:
        s = s + 'Due to one or more errors, your request has not been posted.'
        await ERROR_output(ctx, s)
    else:
        # no errors, add a new request
        #while lock_RequestList:
        #    pass
        # remove dupes first
        RequestList_new = []
        for e in RequestList:
            if e.message.author.id != ctx.message.author.id:
                RequestList_new.append(e)
        RequestList = RequestList_new
        # add new request
        RequestList.append(Request(ctx.message, game, platform, sl_sm, note[:max_note_length]))
        name = str(ctx.message.author.name) + '#' + str(ctx.message.author.discriminator)
        s = name + ', your request has been added to the list.'
        await ERROR_output(ctx, s, prefix='')

@bot.command(pass_context=True)
async def list(ctx):
    """List players of the past hour (and remove older ones)"""
    if not ADMIN_bot_enabled:
        return
    global lock_RequestList, RequestList
    #while lock_RequestList:
    #    pass
    lock_RequestList = True
    tc = datetime.utcnow() # current time
    spaces = 18
    spaces_sl_sm = int(spaces / 2)
    spaces_timestamp = 16
    s = '--- Players seeking games in the last hour (current time: ' + str(tc)[:spaces_timestamp] + ' UTC) ---'
    s = s + '\n```'
    s = s + ' | '.join(('Player'.ljust(spaces)[:spaces], 'Time (UTC)'.ljust(spaces)[:spaces_timestamp], 'Game'.ljust(spaces)[:spaces], 'Platform'.ljust(spaces)[:spaces], 'SL/SM'.ljust(spaces_sl_sm)[:spaces_sl_sm], 'Note'.ljust(spaces)[:spaces]))
    tmp = []
    for i in range(6): # constant is number of columns
        tmp.append('-' * spaces)
    tmp[1] = '-' * spaces_timestamp
    tmp[4] = '-' * spaces_sl_sm
    s = s + '\n' + '-+-'.join(tmp)
    RequestList_new = []
    for e in RequestList:
        td = tc - e.message.timestamp # time difference
        # if time difference is within an hour the request will be preserved
        # otherwise it is skipped and excluded from the reformed list
        if td.total_seconds() <= 3600:
            s_note = e.note
            if len(s_note) > spaces:
                s_note = 'XL note: ' + s_note
            s_row = ' | '.join((e.message.author.name.ljust(spaces)[:spaces], str(e.message.timestamp).ljust(spaces)[:spaces_timestamp], GameMap[e.game].ljust(spaces)[:spaces], PlatformMap[e.platform].ljust(spaces)[:spaces], e.sl_sm.ljust(spaces_sl_sm)[:spaces_sl_sm], s_note.ljust(spaces)))
            s = s + '\n' + s_row
            RequestList_new.append(e)
    RequestList = RequestList_new
    lock_RequestList = False
    s = s + '```--- End of games list ---'
    if len(RequestList) == 0:
        s = '--- No players have sought games in the past hour ---'
    if len(RequestList) > 10:
        await bot.send_message(ctx.message.author, s)
    else:
        await bot.say(s)
    
@bot.command(pass_context=True)
async def clear(ctx):
    """Clears requests made by you. Also removes stale requests"""
    if not ADMIN_bot_enabled:
        return
    global RequestList
    RequestList_new = []
    for e in RequestList:
        to_add = True
        td = datetime.utcnow() - e.message.timestamp # time difference
        if (e.message.author.id == ctx.message.author.id
            or td.total_seconds() > 3600): # exclude stale requests
            to_add = False
        if to_add:
            RequestList_new.append(e)
    RequestList = RequestList_new
    s = ctx.message.author.name + ', your requests and all stale requests have been removed.'
    await bot.say(s)

@bot.command(pass_context=True)
async def status(ctx):
    """Reports if the bot is enabled or not and other info"""
    s = 'enabled'
    if not ADMIN_bot_enabled:
        s = 'disabled'
    await bot.say('--- My functions are currently ' + s + '. ' + str(len(RequestList)) + '/' + str(RequestList_max_size) + ' requests in use ---')

def test_admin(server, user):
    """Returns true if the user has Administration flag set on the server"""
    permissions = server.default_channel.permissions_for(user)
    return permissions.administrator or permissions.manage_server
    
# Commands prefixed with "ADMIN_" require that "test_admin()" returns True
    
@bot.command(pass_context=True)
async def ADMIN_logout(ctx):
    """Logs the bot out"""
    if test_admin(ctx.message.server, ctx.message.author):
        await bot.say('--- ADMIN: Logging out now. ---')
        await bot.logout()
        
@bot.command(pass_context=True)
async def ADMIN_enable(ctx):
    """Enables bot's public functions"""
    global ADMIN_bot_enabled
    if test_admin(ctx.message.server, ctx.message.author):
        ADMIN_bot_enabled = True
        await bot.say('--- ADMIN: My functions are now enabled. ---')
        
@bot.command(pass_context=True)
async def ADMIN_disable(ctx):
    """Disables bot's public functions"""
    global ADMIN_bot_enabled
    if test_admin(ctx.message.server, ctx.message.author):
        ADMIN_bot_enabled = False
        await bot.say('--- ADMIN: My functions are now disabled. ---')

bot.run(bot_token)