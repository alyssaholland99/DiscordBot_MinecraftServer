import os
import discord
import status
from mcstatus import MinecraftServer
from datetime import datetime
from datetime import timedelta
from shutil import copyfile
copyfile(".env", "lib/.env")

from dotenv import load_dotenv
load_dotenv()

server = MinecraftServer(os.environ['SERVER'], int(os.environ['PORT']))

if os.environ['CUSTOM'] == "TRUE":
	copyfile("Custom.py", "lib/custom.py")
	import custom

status = server.status()
print("The server has {0} players and replied in {1} ms".format(status.players.online, round(status.latency, 3)))
query = server.query()
print("The server has the following players online: {0}".format(", ".join(query.players.names)))

token = os.environ['TOKEN']

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

global oldauthor
global oldcommand
global oldmsg
global messagetime
oldcommand = ""
oldauthor = ""
oldmsg = ""
messagetime = datetime.now().time()

@client.event
async def on_message(message):
	server = MinecraftServer(os.environ['SERVER'], int(os.environ['PORT']))
	print(message.content)

	'''Anti Spam Variables'''
	global oldauthor
	global oldcommand
	global oldmsg
	global messagetime
	msg = ""

	prefix = os.environ['PREFIX']

	commandList = ["map", "server", "help", "download", "status", "minecraftNickname"]
	commandList2 = []
	for command in commandList:
		commandList2.append(prefix + command)
	commandList = commandList2

	'''Checking which command has been issued'''
	if message.author == client.user: #Make sure that the bot doesn't reply to itself
		return
	elif message.content.startswith(prefix + 'source'):
		msg = "https://github.coventry.ac.uk/hollan84/MinecraftDiscord"
	elif message.content.startswith(prefix + 'map'):
		msg = os.environ['MAP']
	elif message.content.startswith(prefix + 'server'):
		msg = os.environ['EXTSERVER']
	elif message.content.startswith(prefix + 'help'):
		msg = "Commands:\n"
		for command in commandList:
			msg = "{} - {}\n".format(msg, command)
	elif message.content.startswith(prefix + 'download'):
		msg = os.environ['DOWNLOAD']
	elif message.content.startswith(prefix + 'status'):
		try:
			status = server.status()
			query = server.query()
			if status.players.online > 0:
				msg = str("The server has {0} players and replied in {1} ms\nPlayers:\n - {2}".format(status.players.online, round(status.latency, 3), "\n - ".join(query.players.names)))
			else:
				msg = str("The server has {0} players and replied in {1} ms".format(status.players.online, round(status.latency, 3)))
		except:
			msg = "Server doesn't seem to be repsonding; please message {} for help".format(os.environ["ADMINNAME"])
		checkNicknames = msg.split("\n - ")
		for i in checkNicknames:
			path = "nicknames/" + i
			try:
				n = open(path, "r")
				nick = i + " [" + n.read() + "]"
				msg = msg.replace(i, nick)
				n.close()
			except:
				msg = msg
	elif message.content.startswith(prefix + 'minecraftNickname'):
		splitMessage = message.content
		splitMessage = splitMessage.split()
		path = "nicknames/" + splitMessage[1]
		f = open(path, "w")
		f.write(splitMessage[2])
		f.close()
		msg = "Set " + splitMessage[1] + "'s nickname to " + splitMessage[2]
	elif message.content.startswith(prefix):
		if os.environ['CUSTOM'] == "TRUE":
			msg = custom.customCode(message.content, msg)
		if msg == "":
			msg = "That is not a valid command, use ?help for help"
	else:
		return
	if (message.content == oldcommand) and (message.author == oldauthor):
		if os.environ['ANTISPAM'] == "TRUE":
			s1 = str(messagetime)
			s2 =str(datetime.now().time())
			FMT = '%H:%M:%S.%f'
			tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
			if tdelta.seconds < 60:
				if "Please don't spam commands" in oldmsg:
					return
				else:
					msg = "Please don't spam commands\nWait " + str(round(60-tdelta.seconds, 0)) + " seconds to use this command"
	messagetime = datetime.now().time()
	oldauthor = message.author
	oldcommand = message.content
	oldmsg = msg
	channel = message.channel
	await channel.send(msg)

client.run(token)

