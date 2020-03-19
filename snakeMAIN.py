#(C) JustAllexx

from snekINFO import *

client = commands.Bot(command_prefix = ['s/', 'S/'])
client.remove_command('help')

#===================================================== //Bot Commands\\ =============================================================

@client.command(aliases = ['s', 'Save'])
async def save(ctx):
    if str(ctx.author.id) in info.playerlist:
        info.playerlist[str(ctx.author.id)]['save'] = True
    else:
        await ctx.send("`You must be in a game to save`")   

@client.command(aliases = ['p', 'Pause'])
async def pause(ctx):
    try:
        if not info.playerlist[str(ctx.author.id)]['paused']:
            info.playerlist[str(ctx.author.id)]['pause'], info.playerlist[str(ctx.author.id)]['paused']  = True, True
        else:
            await ctx.send("`You have already paused, you're only allowed to pause the game once`")
    except KeyError:
        await ctx.send("`You must be in a game to pause`")

@client.command(aliases = ['exit', 'stop', 'leave', 'end', 'Quit'])
async def quit(ctx):
    if str(ctx.author.id) in info.playerlist:
        await ctx.send('Quitting game!')
        info.playerlist.pop(str(ctx.author.id))
        info.serverlist.remove(str(ctx.guild.id))
    else:
        ctx.send(ctx.author.mention + ', You are not in a game')

@client.command(aliases = ['info', '?', 'h', 'commands', 'help', 'Help', 'HELP'])
async def cmd(ctx):
    if ctx.message.author == ctx.guild.owner:
        await ctx.channel.send(embed=info.HELP)
    else:
        await ctx.author.send(embed=info.HELP)
        await ctx.channel.send('Sending you info now!')

@client.command(aliases = ['vte', 'support', 'Vote'])
async def vote(ctx):
    if ctx.message.author == ctx.guild.owner:
        await ctx.channel.send('https://discordbots.org/bot/556266236472983562/vote')
    else:
        await ctx.author.send('https://discordbots.org/bot/556266236472983562/vote')
        await ctx.channel.send('Sending you link now!')

@client.command(aliases = ['inv', 'Inv', 'Invite'])
async def invite(ctx):
    await ctx.author.send('https://discordapp.com/oauth2/authorize?client_id=556266236472983562&scope=bot&permissions=1073835200')
    await ctx.channel.send('Sending you invite now!')
    
@client.command(aliases = ['v', 'ver', 'Version'])
async def version(ctx):
    await ctx.channel.send('The version is {}'.format(info.version))

@client.command(aliases = ['c', 'Creator'])
async def creator(ctx):
    await ctx.channel.send('<@296188825624117248> is the creator')

@client.command(aliases = ['hs', 'pb', 'personalbest', 'best', 'HS', 'PB', 'Highscore', 'PersonalBest'])
async def highscore(ctx):
    if str(ctx.author.id) in info.highscores:
        await ctx.channel.send('`' + ctx.author.name +"'s Highscore: " + info.highscores[str(ctx.author.id)] + '`')
    else:
        await ctx.channel.send('You do not yet have a highscore')

@client.command(aliases = ['snake', 'Start', 'Snake'])
async def start(ctx, *args):
    if ctx.channel.type.name == 'private':
        await ctx.send('You cannot start a game in private messages')
        return
    elif str(ctx.guild.id) in info.serverlist:
        await ctx.send("```Only one game at a time per server, however if you'd like to add Snake to your server, use s/inv for the invite```")
        return
    elif str(ctx.author.id) in playerlist:
        await ctx.send("```You're already playing snake on another server, If you'd like to stop the game and begin a new one, use 's/quit' on any server to stop the game```")
        return
    if str(ctx.author.id) in info.savedgames:
        playerpos, playerlen, appleloc, playerid, loop = info.savedgames[str(ctx.author.id)]['playerpos'], info.savedgames[str(ctx.author.id)]['playerlen'], info.savedgames[str(ctx.author.id)]['appleloc'], str(ctx.author.id), info.savedgames[str(ctx.author.id)]['loop']
        BOTmessage = await ctx.channel.send(await get_print(playerpos[len(playerpos)-playerlen:], appleloc))
        info.playerlist.update({playerid: {'BOTmessage': BOTmessage, 'direction': info.savedgames[str(ctx.author.id)]['direction'], 'pause': False, 'paused': False, 'save': False}})
        info.savedgames.pop(str(ctx.author.id))
    else:
        playerpos,playerlen,playerid, appleloc = [(1,0)],1, str(ctx.author.id), (7,5)
        BOTmessage = await ctx.channel.send(await get_print(playerpos, appleloc))
        info.playerlist.update({playerid: {'BOTmessage': BOTmessage, 'direction': '➡', 'pause': False, 'paused': False, 'save': False}})
        loop = False
        if args != ():
            if args[0].lower() == 'loop':
                loop = True
    info.serverlist.append(str(ctx.guild.id))
    for emoji in ['⬅', '⬆','⬇','➡']:
        await BOTmessage.add_reaction(emoji)
    while True:
        await asyncio.sleep(len(info.serverlist))
        direction = info.playerlist[playerid]['direction']
        x,y = playerpos[len(playerpos)-1]
        if direction ==   '⬅':
            if loop and not y-1 in range(10):
                playerpos.append( (x, y+9) )
            else:
                playerpos.append( (x, y-1) )
        elif direction == '⬆':
            if loop and not x+1 in range(10):
                playerpos.append( (x-9, y) )
            else:
                playerpos.append( (x+1, y) )
        elif direction == '⬇':
            if loop and not x-1 in range(10):
                playerpos.append( (x+9, y) )
            else:
                playerpos.append( (x-1, y) )
        elif direction == '➡':
            if loop and not y+1 in range(10):
                playerpos.append( (x, y-9) )
            else:
                playerpos.append( (x, y+1) )

        if info.playerlist[str(ctx.author.id)]['pause']:
            temp = BOTmessage.content
            await BOTmessage.edit(content = info.PAUSED)
            try:
                await client.wait_for('message', check = lambda message: str(message.author.id) == str(ctx.author.id) and message.content in ['s/unpause','s/unp','s/up'] , timeout = 60)
            except:
                pass
            info.playerlist[str(ctx.author.id)]['pause'] = False
            await BOTmessage.edit(content = temp)
            await asyncio.sleep(3)

        if info.playerlist[str(ctx.author.id)]['save']:
            info.savedgames[str(ctx.author.id)] = {'playerpos': playerpos, 'appleloc': appleloc, 'playerlen': playerlen, 'direction': info.playerlist[playerid]['direction'], 'loop': loop}
            await BOTmessage.delete()
            await ctx.send('`Game sucessfully saved`')
            info.playerlist.pop(playerid)
            info.serverlist.remove(str(ctx.guild.id))

        if await is_dead(playerpos, playerlen):
            await ctx.channel.send("{}, `You were killed with a score of {}`".format(ctx.author.mention, playerlen))
            info.playerlist.pop(playerid)
            info.serverlist.remove(str(ctx.guild.id))
            if loop:
                return
            if not (str(ctx.author.id) in info.highscores):
                info.highscores[str(ctx.author.id)] = playerlen
            elif playerlen > int(info.highscores[str(ctx.author.id)]):
                info.highscores[str(ctx.author.id)] = playerlen
            await ctx.channel.send("`Highscore: {}`".format(info.highscores[str(ctx.author.id)]))                                   
            return

        if playerpos[len(playerpos)-1] == appleloc:
            playerlen+=1
            appleloc = await new_appleloc(appleloc, playerpos, playerlen)
            
        temp = await get_print(playerpos[len(playerpos)-playerlen:], appleloc)
        await BOTmessage.edit(content=temp)

#=============================================== //In-Game Commands (snake)\\ =====================================================

async def get_print(playerpos, appleloc):
    temp = ''
    for x in range(10):
        for y in range(10):
            if (9-x,y) in playerpos:
                temp+= chr(11036)
            elif (9-x,y) == appleloc:
                temp+= '\U0001f34e' #Apple unicode
            else:
                temp+=chr(11035)
        temp+='\n'
    return str(temp)

async def new_appleloc(appleloc, playerpos, playerlen):
    while appleloc in playerpos[len(playerpos)-playerlen:]:
        appleloc = (randint(0, 9), randint(0,9))
    return appleloc

async def is_dead(playerpos, playerlen):
    locx,locy = playerpos[len(playerpos)-1]
    if locx in range(10) and locy in range(10) and playerpos[len(playerpos)-playerlen:].count(playerpos[len(playerpos)-1]) < 2:
        return False
    return True

async def update_status():
    while True:
        await client.change_presence(activity = discord.Game(name = "Snake on {} servers! Use s/help for help".format(len(client.guilds)), type=1))
        await asyncio.sleep(300)
        hs = open('highscores.txt', mode='w')
        hs.write(str(info.highscores))
        hs.close()
        sg = open('savedgames.txt', mode='w')
        sg.write(str(info.savedgames))
        sg.close()

#================================================ //ON_COMMANDS\\ ==================================================================

@client.event
async def on_ready():
    print('SnakeBot online')
    await update_status()

@client.event
async def on_command_error(ctx, exception):
    if ctx.command == None:
        commandname= 'UNKNOWN COMMAND'
    elif ctx.command != None:
        commandname = ctx.command.name
    elif ctx.command.name == 'start' and exception.args[0] == 'Command raised an exception: NotFound: 404 NOT FOUND (error code: 10008): Unknown Message':
        await ctx.send('Sorry ' + ctx.author.mention + "```Your game was deleted by a member of your server with the 'MANAGE_MESSAGES' role``` Thus your game could not be continued")
        info.playerlist.pop(str(ctx.author.id))
        info.serverlist.remove(str(ctx.guild.id))
        return
    elif ctx.command.name == 'start' and exception.args[0].startswith("Command raised an exception: KeyError:"):
        return
    print(exception.args[0], 'in', commandname)

@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    if str(reaction.message.author.id) == str(client.user.id) and str(user.id) in info.playerlist:
        if reaction.message.id == info.playerlist[str(user.id)]['BOTmessage'].id:
            if reaction.emoji in ['⬅', '⬆','⬇','➡']:
                info.playerlist[str(user.id)]['direction'] = reaction.emoji
            else:
                await user.send('`Only React With The Directions Provided`')
        try:
            await reaction.remove(user)
        except discord.errors.Forbidden:
            return
        
client.run("YOUR TOKEN")
