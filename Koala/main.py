import asyncio
from logging import exception
from discord.ext import commands
import discord
import os
import json
from index import index
# from cmds.user import user

CommandPrefix = '!'
# intents = discord.Intents.default()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=CommandPrefix,
                   intents=intents,
                   case_insensitive=True)


# ==========讀設定檔=============#
# 之後改成用dotenv設定環境變數
with open("Koala/Datas/JSON/Setting.json", 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)


# @bot.command()
# async def load(ctx, extension: str):
#     await bot.load_extension(f"cmds.{extension}", package="/data/Koala")
#     await ctx.send(f'Loaded {extension} done.')

# @bot.command()
# async def unload(ctx, extension: str):
#     await bot.unload_extension(f"cmds.{extension}", package="/data/Koala")
#     await ctx.send(f'UnLoaded {extension} done.')

# @bot.command()
# async def reload(ctx, extension: str):
#     await bot.reload_extension(f"cmds.{extension}", package="/data/Koala")
#     await ctx.send(f'ReLoaded {extension} done.')    



async def load_extensions():
    for filename in os.listdir("./Koala/cmds"):
        if filename.endswith('.py'):
            await bot.load_extension(f"cmds.{filename[:-3]}", package="/data/Koala")

async def main():
    await load_extensions()
    await bot.start(jdata['TOKEN'])

index()

if __name__ == "__main__":
    bot.remove_command('help')
    asyncio.run(main())
    # bot.run(jdata['TOKEN'])
