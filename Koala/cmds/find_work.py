import discord
from discord.ext import commands
import pandas as pd


class find_work(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='help', aliases=['h'])
    async def help(self, ctx):
        CommandPrefix = '!'
        def embed_Normal_Cmd():
            embed = discord.Embed(title="**指令**",
                                   description="指令:",
                                   color=0x00FFFF)
            embed.add_field(name=CommandPrefix + "example" + "\n" +
                        CommandPrefix + "ex",
                        value="查看upload的格式範例",
                        inline=False)
            embed.add_field(name=CommandPrefix + "upload" + "\n" +
                        CommandPrefix + "up",
                        value="上傳面試心得(請照格式填寫)",
                        inline=False)
            embed.add_field(name=CommandPrefix + "find (公司名稱)" + "\n",
                        value="尋找公司名稱(目前只提供公司搜尋)",
                        inline=False)
            embed.add_field
            embed.add_field(name=CommandPrefix + "list 空格 (欄位名稱 ex 公司,職位...或是只輸入前面的list會跑出所有資訊)" + "\n",
                        value="查看目前有人分享的xx",
                        inline=False)
            return embed
        await ctx.send(embed=embed_Normal_Cmd())

    # 文字格式
    @commands.command(name='example', aliases=['ex'])
    async def example(self, ctx):
        format_ = "大家都是工程師，我懶得針對格式做處理，分隔符號為兩個'\\n'\n\
!up\n\
'公司'(請填完整名稱，拜託):\n\
(請多空一行)\n\
'職位':\n\
(請多空一行)\n\
'是否筆試':\n\
(請多空一行)\n\
'考古題':\n\
(請多空一行)\n\
'心得':"
        await ctx.send(format_)

    @commands.command(name='upload', aliases=['up'])
    async def upload(self, ctx, *, content):
        df = pd.read_csv('Koala/Datas/CSV/Interview.csv', encoding='utf-8')
        try:
            content = content.split('\n\n')
            new = pd.DataFrame({
                '公司':content[0].split(':')[1],
                '職位':content[1].split(':')[1],
                '是否筆試':content[2].split(':')[1],
                '考古題':content[3].split(':')[1],
                '心得':content[4].split(':')[1]
            },index=[0])
            df = df.append(new, ignore_index=True)
            df.to_csv('Koala/Datas/CSV/Interview.csv', encoding='utf-8', index = False)
            await ctx.send('新增完成')

        except:
            await ctx.send('請檢查格式')
        
    # 查看列表
    @commands.command(name='list')
    async def list(self, ctx, columns:str = ""):
        df = pd.read_csv('Koala/Datas/CSV/Interview.csv', encoding='utf-8')  
        if columns == "":
            await ctx.send(df)
        else:
            await ctx.send("\n".join(set(df[f'{columns}'])))

    @commands.command()
    async def find(self, ctx, condition:str):
        df = pd.read_csv('Koala/Datas/CSV/Interview.csv', encoding='utf-8')  
        await ctx.send(df[df[f'公司']==f'{condition}'])
    
    
async def setup(bot):
    await bot.add_cog(find_work(bot))
