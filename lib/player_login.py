from operator import truediv
import os
from time import sleep
import discord
from discord.ext import tasks
import status
from mcstatus import MinecraftServer
from datetime import datetime
from datetime import timedelta
from shutil import copyfile

import difflib
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

global old_players
global old_players_online
global messageIDs
old_players = []
old_players_online = 0
messageIDs = {}

@tasks.loop()
async def players():
	while True:

		global old_players
		global old_players_online

		server = MinecraftServer(os.environ['SERVER'], int(os.environ['PORT']))

		msg = ""

		try:
			status = server.status()
			query = server.query()
			joinedPlayers = []
			leftPlayers = []
			if query.players.names != old_players:
				new_players = query.players.names
				for element in new_players:
					if element not in old_players:
						joinedPlayers.append(element)
				for element in old_players:
					if element not in new_players:
						leftPlayers.append(element)
				old_players = query.players.names
				print(joinedPlayers)
				print(leftPlayers)
		except KeyboardInterrupt:
			exit()
		channel = client.get_channel(1005838791451365506)
		print(channel)
		print(msg)
		for i in joinedPlayers:
			msg = i + " has joined the minecraft server\n"
			if msg != "":
				if i in messageIDs:
					delmsg = await channel.fetch_message(messageIDs[i])
					await delmsg.delete()
				sent_message = await channel.send(msg)
				messageIDs[i] = sent_message.id
		for i in leftPlayers:
			msg =  i + " has left the minecraft server\n"
			if msg != "":
				if i in messageIDs:
					delmsg = await channel.fetch_message(messageIDs[i])
					await delmsg.delete()
				sent_message = await channel.send(msg)
				messageIDs[i] = sent_message.id
		
			
		sleep(1)

@client.event
async def on_ready():
	if not players.is_running():
		players.start() #If the task is not already running, start it

client.run(token)

