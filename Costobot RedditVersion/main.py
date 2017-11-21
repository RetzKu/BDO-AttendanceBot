import json
import websockets
import asyncio
import discord
import discord.ext.commands as discordbot
import datetime

#Own modules
import src.commands


class botclass:
    def __init__(self):
        with open('Keys.json') as fp:
            keys = json.load(fp)
        self.running = True
        self.token = keys['Token']
        self.discord = discordbot.Bot(command_prefix = '!')
        self.excel = "exceli"
        self.data_handler = "handlaaja"

bot = botclass()

@bot.discord.event
async def on_ready():
    await src.commands.add_commands(bot.discord,bot.excel,bot.data_handler)
    print('Logged in as')
    print(bot.discord.user.name)
    print(bot.discord.user.id)
    print('------')

@bot.discord.event
async def on_message(msg):
    if isinstance(msg.channel, discord.abc.PrivateChannel):
        print('private message received')
    else:
        await bot.discord.process_commands(msg)

def run():
   while bot.running is True:
      bot.discord.loop.run_until_complete(bot.discord.start(bot.token))

if __name__ == "__main__":
    run()