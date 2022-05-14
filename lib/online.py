import time
import discord
import status
import difflib
from mcstatus import MinecraftServer
from datetime import datetime
from datetime import timedelta
import os


server = MinecraftServer(os.environ['SERVER'], int(os.environ['PORT']))

status = server.status()
print("The server has {0} players and replied in {1} ms".format(status.players.online, status.latency))
query = server.query()
print("The server has the following players online: {0}".format(", ".join(query.players.names)))

token = os.environ['TOKEN']

client = discord.Client()

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord!')
	await players()

@client.event
async def players():
	currentPlayers = []
	server = MinecraftServer(os.environ['SERVER'], int(os.environ['PORT']))
	while True:
		try: 
			time.sleep(1)
			query = server.query()
			players = "-".join(query.players.names)
			players = players.split("-")

			if '' in players:
				players.remove('')


			print("CP = " + str(currentPlayers))
			print("P = " + str(players))
			print("LCP = " + str(len(currentPlayers)))
			print("LP = " + str(len(players)))
			if not currentPlayers == players:
				print("CP = " + str(currentPlayers))
				print("P = " + str(players))
				print("LCP = " + str(len(currentPlayers)))
				print("LP = " + str(len(players)))
				if len(currentPlayers) < len(players):
					print("NEW LOGIN")
					for i in players:
						if not i in currentPlayers:
							name = i
							endStr = " has logged in\n"
				elif len(currentPlayers) > len(players):
					print("NEW LOGOUT")
					for i in currentPlayers:
						if not i in players:
							name = i
							endStr = " has logged out\n"
				else:
					print("HELP")

				
				print(name)

				now = datetime.now()
				dateTimeCurrent = now.strftime("%d/%m/%Y %H:%M:%S")
				
				msg = ""
				
				path = "nicknames/" + name
				try:
					n = open(path, "r")
					nick = " [" + n.read() + "] "
					n.close()
				except:
					nick = ""




				if name is not '':
					msg = dateTimeCurrent + " - " + name + nick + endStr
				channel = client.get_channel(694572684566331473)
				if msg:
					await channel.send(msg)
				currentPlayers = players
				if '' in currentPlayers:
					currentPlayers.remove('')
				print("NCP = " + str(currentPlayers))
				print("NP = " + str(players))
		except KeyboardInterrupt:
			exit()

client.run(token)

