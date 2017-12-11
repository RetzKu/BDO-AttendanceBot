from discord.ext.commands import *
import discord
from src.guilds import guilds
import json

def correct_assert(ctx) -> Context:
    assert isinstance(ctx, Context)
    return ctx

async def get_errors(result, author):
    if len(result) != 0:
        msg = ""
        for errorsmsg in result:
            msg = msg + "\n" + errorsmsg
        await author.send("```Following errors raised! {0}```".format(msg))

async def add_commands(bot, guilds):

    @bot.command(pass_context = True)
    async def save(ctx):
        guilds.save()
        print("Saved")

    @bot.command(pass_context = True)
    async def load(ctx):
        guilds.load()
        print("Loaded")

    @bot.command(pass_context = True)
    async def hello(ctx):
        ctx = correct_assert(ctx) #Just fancy way to get visualstudio show insides of ctx
        await ctx.channel.send("hi you :3")

    @bot.group(pass_context = True)
    async def group(ctx):
        ctx = correct_assert(ctx)
        if ctx.invoked_subcommand is None:
            ctx.author.send("Available group commands: register, disband")

    @group.command(pass_context = True)
    async def register(ctx, group_name, group_password):
        guilds.register_group(ctx.author.id, ctx.author.display_name, group_name,group_password)
        result = guilds.fetch_errors()
        if len(result) == 0:
            ctx.author.send("Guild created Successfully")
        else:
            await get_errors(result, ctx.author)

    #MODERATOR TREE START
    @bot.group(pass_context = True)
    async def moderator(ctx):
        ctx = correct_assert(ctx)
        if ctx.invoked_subcommand is None:
            ctx.author.send("Available commands: Add, List, Remove")

    @moderator.command(pass_context = True)
    async def add(ctx, group_name, group_id, moderator_name, moderator_id):
        ctx = correct_assert(ctx)

        if guilds.add_moderator(ctx.author.id,group_name,group_id,moderator_name,moderator_id) is False:
            result = guilds.fetch_errors()
            if len(result) != 0:
                msg = ""
                for errorsmsg in result:
                    msg = msg + "\n" + errorsmsg
                await ctx.author.send("```Could not add moderator cause of following errors!{0}```".format(msg))
                return False

        await ctx.author.send("New moderator added successfully")
        return True

    @moderator.command(pass_context = True)
    async def list(ctx, group, password):
        list = guilds.get_moderatorlist(group, password)
        msg = ""
        chunk = []
        new_list = []
        n = 0
        for i in range(0, len(list)):
            msg = msg + '\n' + list[i].Name + 'ID: ' + str(list[i].ID)
            if i == 19+n:
               n = n + 19
               await ctx.author.send(msg)
               msg = ""
        await ctx.author.send(msg)
                 
            
    #MODERATOR TREE END
    
    #MEMBER TREE START
    @bot.group(pass_context = True)
    async def members(ctx):
        if ctx.invoked_subcommand is None:
            ctx.author.send("Available command: Add, List, Remove")

    @members.command(pass_context = True)
    async def add(ctx, group, password):
        guilds.add_member(group, password, ctx.author.display_name, ctx.author.id)

        result = guilds.fetch_errors()
        if len(result) == 0:
            ctx.author.send("You joined group" + group + " successfully")
        else:
            await get_errors(result, ctx.author)

    @members.command(pass_context = True)
    async def list(ctx, group, password):
        list = guilds.get_memberlist(group, password)
        msg = ""
        chunk = []
        new_list = []
        n = 0
        for i in range(0, len(list)):
            msg = msg + '\n' + list[i].Name + 'ID: ' + str(list[i].ID)
            if i == 19+n:
               n = n + 19
               await ctx.author.send(msg)
               msg = ""
        await ctx.author.send(msg)
                 
    #MEMBER TREE END
        
        