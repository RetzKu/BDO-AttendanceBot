from discord.ext.commands import *
import discord

def correct_assert(ctx) -> Context:
    assert isinstance(ctx, Context)
    return ctx

async def add_commands(bot, excel, data_handler):

    @bot.command(pass_context = True)
    async def hello(ctx):
        ctx = correct_assert(ctx) #Just fancy way to get visualstudio show insides of ctx
        await ctx.channel.send("hi you :3")