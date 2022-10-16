from logging import exception
from discord.ext import commands
import discord
import os
import json

CommandPrefix = '!'
# intents = discord.Intents.default()
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=CommandPrefix,
                   intents=intents,
                   case_insensitive=True)

with open("Backup/Datas/JSON/Setting.json", 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)

# ==========關閉機器人=============#


@bot.command(name='stop', description="The command of stop the sub_bot")
async def stop(ctx, sub_bot_name: str = ""):
    sub_bot_path = sub_bot_name+"/main.py" if sub_bot_name else "main.py"
    if sub_bot_path != "main.py":  # 暫時把關閉主控的功能關掉
        await ctx.send(f'開始關閉: {sub_bot_path} 檔案')
        os.system(
            f"ps aux|grep {sub_bot_path}|grep -v grep|cut -c 9-15|xargs kill -15")
        await ctx.send('關閉完成')

# ==========重新啟動機器人=============#
# 之後要新增確認功能


@bot.command(name='rerun', description="The command of Rerun Koala/main.py", aliases=['re'])
async def ReRun(ctx, sub_bot_name: str = ""):
    sub_bot_path = sub_bot_name+"/main.py" if sub_bot_name else "main.py"
    if sub_bot_path != "main.py":  # 暫時把關閉主控的功能關掉
        try:
            if os.path.exists(sub_bot_path):
                await ctx.send(f'開始關閉: {sub_bot_path} 檔案')
                os.system(
                    f"ps aux|grep {sub_bot_path}|grep -v grep|cut -c 9-15|xargs kill -15")
                await ctx.send('關閉完成，重新開啟中')
                os.system(
                    f"nohup python3 -u {sub_bot_path}>./{sub_bot_name}/Logs/console.log 2>&1 &")
                await ctx.send('重新開啟完成')
            else:
                print('main.py 不存在')
                await ctx.send(f'沒有: {sub_bot_path} 檔案')
        except exception:
            await ctx.send(exception)

# ==========啟動內層機器人=============#
# 外層機器人不會執行


@bot.command(name='run', description="The command of run Koala/main.py", aliases=['r'])
async def Run(ctx, sub_bot_name: str = ""):
    sub_bot_path = sub_bot_name+"/main.py" if sub_bot_name else "main.py"
    # 排除外層機器人本身
    if sub_bot_path == 'main.py':
        await ctx.send("你不能重複執行此機器人")
    # 內層機器人存在就啟動
    elif sub_bot_name and os.path.exists(sub_bot_path):
        os.system(
            f"nohup python3 -u {sub_bot_path}>./{sub_bot_name}/Logs/console.log 2>&1 &")
        await ctx.send("啟動完成")
    # 不存在就告知不存在
    else:
        print(f'{sub_bot_path} 不存在')
        await ctx.send(f'沒有: {sub_bot_path} 檔案')

# ==========透過外層機器人下linux指令並傳回DC=============#


@bot.command(name='bash', description="Use the bash command from Discord_bot")
async def bash(ctx, *, linux_command: str):
    if '戰地工程師執照' not in [y.name.lower() for y in ctx.message.author.roles]:
        await ctx.send(f'<@!{ctx.author.id}> 你沒有戰地工程師執照，無法使用指令。')
    else:
        result = os.popen(linux_command)
        await ctx.send(result.read())


if __name__ == "__main__":
    bot.run(
        jdata['TOKEN']
    )
