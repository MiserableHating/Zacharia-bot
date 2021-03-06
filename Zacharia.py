# Zacharia v.1.0.0

import discord, asyncio, logging, sys, datetime, os, json, urllib, youtube_dl
from discord.ext import commands
from itertools import cycle

client = commands.Bot(command_prefix = '.')
client.remove_command('help')
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename=('logsZacha\Zacha %s.log' % datetime.date.today()), encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# # # Variables # # #

LienInvitation = "https://discordapp.com/oauth2/authorize?client_id=L'ID DE VOTRE BOT&scope=bot&permissions=2012740695"
Token = 'Remplir avec votre token'
ownerid = '130313080545607680'
owneridint = 130313080545607680
status = ['by Atae Kurri#6302', 'NSFWing', '.help']
versionBot = "Zacharia v.1.0.0"
#extensions = ['help']
players = {}
queues = {}

# # # Defs # # #

def check_queue(id):
    if queues[id] != []:
        player = queues[id].pop(0)
        player[id] = player
        player.start()

async def change_status():
    await client.wait_until_ready()
    msgs = cycle(status)

    while not client.is_closed:
        current_status = next(msgs)
        await client.change_presence(game=discord.Game(name=current_status))
        await asyncio.sleep(10)

# # # Events # # #

@client.event
async def on_ready():
    print('------')
    print('Bot lancé sous')
    print(client.user.name)
    print(client.user.id)
    print('Discord version {}'.format(discord.__version__))
    print('Version actuelle du bot : {}'.format(versionBot))
    print('------')
    print('Systèmes en ligne : LogsHandler, Music Bot, AutoRole, Saying things')
    print('Command Prefix : .')
    print('------')
    print(' ')

@client.event
async def on_member_join(member):
    channel = '523905596332703757'
    await client.send_message(channel, "Bonjour {}, bienvenue ! N'oublie pas de faire un tour dans les #règles et te présenter".format(member.mention))

@client.event
async def on_member_join(member):
    role = discord.utils.get(member.server.roles, name='Nouvelle âme')
    await client.add_roles(member, role)
    print("Role 'Nouvelle âme' ajouté pour {}".format(member))
    date = datetime.date.today()

# # # Commandes # # #

@client.command(pass_context=True)
async def help(ctx):
    author = ctx.message.author
    embed = discord.Embed(colour = discord.Colour.orange())
    embed.set_author(name='Help')
    embed.add_field(name='.join', value="Le bot rejoins votre channel vocal.", inline=False)
    embed.add_field(name='.play [URL]', value="Jouer une musique ***sur Youtube***.", inline=False)
    embed.add_field(name='.stop', value="La musique va s'arrêter.", inline=False)
    embed.add_field(name='.pause', value="La musique se met sur pause.", inline=False)
    embed.add_field(name='.resume', value="La musique reprend.", inline=False)
    embed.add_field(name='.suggest', value="Envoyer une suggestion. (Ne marche que sur le serveur 'Purgatoire')", inline=False)
    embed.add_field(name='.priority', value="Envoyer une demande prioritaire aux admins. (Ne marche que sur le serveur 'Purgatoire')", inline=False)
    embed.add_field(name='.lienInvit', value="Lien d'invitation pour m'inviter sur votre serveur (Attention, certaines commandes ne marcheront pas sur votre serveur)", inline=False)

    await client.send_message(author, embed=embed)
    await client.send_message(ctx.message.channel, 'Help envoyé dans vos mp.')

@client.command(pass_context=True)
async def join(ctx):
    await client.join_voice_channel(ctx.message.author.voice.voice_channel)
    print("Commande join exécutée avec succès.")

@client.command(pass_context=True)
async def leave(ctx):
    voice_client = client.voice_client_in(ctx.message.server)
    await voice_client.disconnect()
    print("Commande leave exécutée avec succès.")

@client.command(pass_context=True)
async def play(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))
    players[server.id] = player
    player.start()
    print("Commande play exécutée avec succès.")

@client.command(pass_context=True)
async def pause(ctx):
    id = ctx.message.server.id
    players[id].pause()
    print("Commande pause exécutée avec succès.")

@client.command(pass_context=True)
async def stop(ctx):
    id = ctx.message.server.id
    players[id].stop()
    print("Commande stop exécutée avec succès.")

@client.command(pass_context=True)
async def resume(ctx):
    id = ctx.message.server.id
    players[id].resume()
    print("Commande resume exécutée avec succès.")

@client.command(pass_context=True)
async def queue(ctx, url):
    server = ctx.message.server
    voice_client = client.voice_client_in(server)
    player = await voice_client.create_ytdl_player(url, after=lambda: check_queue(server.id))

    if server.id in queues:
        queues[server.id].append(player)
    else:
        queues[server.id] = [player]
    await client.say('Vidéo mise dans la queue.')
    print("Commande queue exécutée avec succès.")

@client.command(pass_context=True)
async def kill(ctx):
    if ctx.message.author.id == ownerid:
        sys.exit()
    else:
        await client.say("Vous n'avez pas la permission de kill le bot.")

@client.command(pass_context=True)
@commands.has_role(name="Reine du Purgatoire")
async def say(ctx, *args):
    messagechannel = client.get_channel('523905596332703757')
    await client.send_message(messagechannel, "{}".format(' '.join(args)))

@client.command(pass_context=True)
async def suggest(ctx, *args):
    messageauthor = ctx.message.author.mention
    messagechannel = client.get_channel('523908012742803476')
    await client.send_message(messagechannel, "{} propose : {}".format(messageauthor, ' '.join(args)))

@client.command(pass_context=True)
async def priority(ctx, *args):
    messageauthor = ctx.message.author.mention
    messagechannel = client.get_channel('523908245425750026')
    await client.send_message(messagechannel, "{} vous envoie : {}".format(messageauthor, ' '.join(args)))

@client.command(pass_context=True)
@commands.has_role(name="Reine du Purgatoire")
async def mute(ctx, member: discord.Member, *args):
    role = discord.utils.get(member.server.roles, name='muted')
    client.add_roles(args, role)

@client.command(pass_context=True)
@commands.has_role(name="Reine du Purgatoire")
async def kick(ctx, user: discord.Member):
    await client.say(":boot: {} a été kick".format(user.name))
    await client.kick(user)

@client.command(pass_context=True)
async def lienInvit(ctx):
    await client.say("Utilisez ce lien pour m'ajouter à votre serveur (Attention, certaines commandes ne marchent que sur le serveur 'Purgatoire') {}".format(LienInvitation))

# # # Commandes annulées # # #

#@client.command()
#@commands.has_role(name="Princesse du Purgatoire")
#async def load(extension):
#    try:
#        client.load_extension(extension)
#        print('Loaded {}'.format(extension))
#    except Exception as error:
#        print('{} ne peut pas être loadé. [{}]'.format(extension, error))

#@client.command()
#@commands.has_role(name="Princesse du Purgatoire")
#async def unload(extension):
#    try:
#        client.unload_extension(extension)
#        print('Unloaded {}'.format(extension))
#    except Exception as error:
#        print('{} ne peut pas être unloadé. [{}]'.format(extension, error))

#if __name__ == '__main__':
#    for extension in extensions:
#        try:
#            client.load_extension(extension)
#            print('{} loadé avec succès.'.format(extension))
#        except Exception as error:
#            print('{} ne peut pas être loadé. [{}]'.format(extension, error))

client.loop.create_task(change_status())
client.run(Token)
