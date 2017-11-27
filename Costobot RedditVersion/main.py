import json
import websockets
import asyncio
import discord
import discord.ext.commands as discordbot

#Own modules
import src.commands
from src.guilds import guilds
import src.utils as utility

class botclass:
    def __init__(self):
        with open('Keys.json') as fp:
            keys = json.load(fp)
        self.running = True
        self.token = keys['Token']
        self.discord = discordbot.Bot(command_prefix = '!')
        self.guilds = guilds()

bot = botclass()

@bot.discord.event
async def on_ready():
    await src.commands.add_commands(bot.discord,bot.guilds)
    print('Bot Activated with following information')
    print(bot.discord.user.name)
    print(bot.discord.user.id)
    print('------')

@bot.discord.event
async def on_message(msg):
    if isinstance(msg.channel, discord.abc.PrivateChannel):
        if msg.author != bot.discord.user:
            print("Message received from user " + msg.author.display_name + utility.get_timespamp()) 
        else:
            print("I sent message to " + msg.channel.recipient.display_name + utility.get_timespamp())

    else:
        await bot.discord.process_commands(msg)

def run():
   while bot.running is True:
        bot.discord.loop.run_until_complete(bot.discord.start(bot.token))

if __name__ == "__main__":
    run()