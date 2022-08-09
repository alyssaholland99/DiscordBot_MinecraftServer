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

#status = server.status()
#print("The server has {0} players and replied in {1} ms".format(status.players.online, round(status.latency, 3)))
#query = server.query()
#print("The server has the following players online: {0}".format(", ".join(query.players.names)))

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
	channel = client.get_channel(1005838791451365506)
	logsChannel = client.get_channel(1006630834549313666)
	outagesChannel = client.get_channel(1005824369467064371)

	mgs = [] #Empty list to put all the messages in the log 
	async for x in channel.history(limit=100):
		await x.delete()
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
		except:
			
			await outagesChannel.send("The server appears to have gone down")
			working = False
			server = MinecraftServer(os.environ['SERVER'], int(os.environ['PORT']))
			while (working == False):
				try:
					if(status.latency > 0 and status.latency < 100):
						working = True
						await outagesChannel.send("The server appears to have be back up")
				except:
					pass
		 #CHANGE THE ID

		for i in joinedPlayers:
			msg = i + " **joined** the minecraft server\n"
			if msg != "":
				if i in messageIDs:
					delmsg = await channel.fetch_message(messageIDs[i])
					await delmsg.delete()
				sent_message = await channel.send(msg)
				await logsChannel.send(msg)
				messageIDs[i] = sent_message.id
		for i in leftPlayers:
			msg =  i + " **left** the minecraft server\n"
			if msg != "":
				if i in messageIDs:
					delmsg = await channel.fetch_message(messageIDs[i])
					await delmsg.delete()
				sent_message = await channel.send(msg)
				await logsChannel.send(msg)
				messageIDs[i] = sent_message.id
		
			
		sleep(1)

@client.event
async def on_ready():
	if not players.is_running():
		players.start() #If the task is not already running, start it

client.run(token)

