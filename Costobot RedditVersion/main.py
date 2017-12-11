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
        try:
            self.guilds.load()
        except:
            print("No save data")


bot = botclass()

@bot.discord.event
async def on_ready():
    try:
        await src.commands.add_commands(bot.discord,bot.guilds)
    except:
        print("Tried to re-setup commands")
    print('Bot Activated with following information')
    print(bot.discord.user.name)
    print(bot.discord.user.id)
    print('------')

async def save_guilds():
    await bot.discord.wait_until_ready()
    while bot.running is True:
        bot.guilds.save()
        print("Guild Data saved")
        await asyncio.sleep(60)

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
        loop = asyncio.get_event_loop()
        loop.create_task(save_guilds())
        bot.discord.loop.run_until_complete(bot.discord.start(bot.token))

if __name__ == "__main__":
    run()