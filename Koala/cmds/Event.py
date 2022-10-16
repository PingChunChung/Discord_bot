import discord
from discord.ext import commands
import pandas as pd
import random
class Event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        pd.set_option('display.max_columns', None)
        pd.set_option('display.max_rows', None)
        pd.set_option('max_colwidth', 100)

    # @commands.Cog.listener()
    # async def on_ready(self):
    #     print('Ready!')
    #     print('Logged in as ---->' , self.bot.user) # self.bot.user 回傳 機器人名稱#1234
    #     print('ID:', self.bot.user.id) # self.bot.user.id 回傳 機器人ID

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'{round(self.bot.latency*1000)}(ms)\n http://ehci.myselfnas.com:8081/')

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

    # 查看列表
    @commands.command(name='test')
    async def test(self, ctx, condition:str):
        df = pd.read_csv('Koala/Datas/CSV/Interview.csv', encoding='utf-8')  
        data = df[df[f'公司']==f'{condition}']
        await ctx.send(\
f"""公司:{data['公司']}
職位:{data['職位']}
是否筆試:{data['是否筆試']}
考古題:{data['考古題']}
心得:{data['心得']}
-------------------------------------------------------
""")


async def setup(bot):
    await bot.add_cog(Event(bot))
