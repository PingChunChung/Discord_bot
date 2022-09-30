import discord
from discord.ext import commands
import pandas as pd
import random
class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print('Ready!')
    #     print('Logged in as ---->' , self.bot.user) # self.bot.user 回傳 機器人名稱#1234
    #     print('ID:', self.bot.user.id) # self.bot.user.id 回傳 機器人ID

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)}(ms)')

    @commands.command()
    async def hello(self,ctx):
        await ctx.send('Hi')

    @commands.command(name="找工作")
    async def foo(self, ctx):
        await ctx.send("台北車站很空")

    @commands.command(name="找地方睡")
    async def sleep(self, ctx):
        sleep_list = ['北車', '公園', '天橋下']
        await ctx.send(random.choice(sleep_list))

async def setup(bot):
    await bot.add_cog(Event(bot))
