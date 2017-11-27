from discord.ext.commands import *
import discord
from src.guilds import guilds

def correct_assert(ctx) -> Context:
    assert isinstance(ctx, Context)
    return ctx

async def add_commands(bot, guilds):

    @bot.command(pass_context = True)
    async def hello(ctx):
        ctx = correct_assert(ctx) #Just fancy way to get visualstudio show insides of ctx
        await ctx.channel.send("hi you :3")

    @bot.command(pass_context = True)
    async def register(ctx, name, password):
        ctx = correct_assert(ctx)
        result = []

        if guilds.new_guild(name,ctx.guild.id,password,ctx.author.id,ctx.author.display_name) is False:
            result = guilds.fetch_errors()

        if len(result) != 0:
            msg = ""
            for errorsmsg in result:
                msg = msg + "\n" + errorsmsg
            await ctx.author.send("```Guild creation failed cause of following errors!{0}```".format(msg))
            return False
        await ctx.author.send("Guild Created successfully")
        return True

    @bot.command(pass_context = True)
    async def add_moderator(ctx, moderator_id, moderator_name):
        ctx = correct_assert(ctx)

        if guilds.add_moderator_to_guild(ctx.guild.id, moderator_name, moderator_id) is False:
            result = guilds.fetch_errors()
            if len(result) != 0:
                msg = ""
                for errorsmsg in result:
                    msg = msg + "\n" + errorsmsg
                await ctx.author.send("```Could not add moderator cause of following errors!{0}```".format(msg))
                return False

        await ctx.author.send("New moderator added successfully")
        return True


        
        