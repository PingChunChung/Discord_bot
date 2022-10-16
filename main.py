from logging import exception
from keep_alive import keep_alive
from keep_alive import setUsers, setRows, setDatas, setAosUser
# discord
from discord.ext import commands
import discord
import re  # 過濾法則
# yt play
#import youtube_dl
import os
# json
import json
# googleshhe
# 時間
import time
# 異端同步
import asyncio
# 亂數
import random

# CSV
import csv

CommandPrefix = '!!'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=CommandPrefix,
                   intents=intents,
                   case_insensitive=True)
'''
print(driver.find_element_by_class_name("example") # 抓取第一個)
print(driver.find_element_by_id("mcmap"))
'''

with open("./Datas/JSON/Setting.json", 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
    print(jdata)

aos = []  # aos列表
aosUser = []  # 隨機aos加入給users用

######備註#####
#EVT==事件====#
#CMD==指令====#
######備註#####


#EVT==Bot開機====#
@bot.event
async def on_ready():
    data = []
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print(bot.users)  # 所有用戶資料

    for i in bot.users:
        if i.avatar:
            print(i.avatar.url)
    # 設定使用者至網頁

    for line in open('./Datas/CSV/data-aos.csv', 'r'):
        aos.append(line.strip())
    for i in range(len(bot.users)-1):
        print(i)
        aosUser.append(aos[random.randint(0, len(aos)-1)])

    with open("./Datas/CSV/Developer.csv", "r", encoding="utf-8") as file:
        csv_file = csv.reader(file)
        for row in csv_file:
            data.append(row)
        data.remove(['id', 'date', 'log','editor'])

    setUsers(bot.users)
    setAosUser(aosUser)
    setDatas(data)
    print('------------')


#EVT==當有人加入群組====#
@bot.event
async def on_member_join(member: discord.Member):
    with open("./Datas/JSON/Setting.json", 'r', encoding='utf8') as jfile:
        jdata = json.load(jfile)
    channel = bot.get_channel(int(jdata['Welcome_Channel_ID']))
    temp = jdata['Roles_Channel']
    colour = random.randint(0, 16777215)
    embed_One = discord.Embed(
        title=f"**{member.name}**",
        description=f"<@!{member.id}>\n加入伺服器時間為 : {member.joined_at.__format__('%Y-%m-%d  %H:%M:%S')}\n",
        color=discord.Colour(colour))
    pfp = member.avatar.url
    print(pfp)
    embed_One.set_thumbnail(url=f"{pfp}")

    await channel.send(embed=embed_One)

    await channel.send(
        content=f'歡迎新人 **{member.name}** 平安著陸~ヽ(✿ﾟ▽ﾟ)ノ\n 記得去這個地方認領身分證喔~(點擊表情即可獲得身分組)!!<#{temp}>\n\n'
    )

    role = discord.utils.get(member.guild.roles,
                             name=jdata['Join_Server_Role'])
    await member.add_roles(role)

    print(f'id:{member.id}')
    print(f'name:{member.name}Join!!')


#EVT==當有人離開群組====#
@bot.event
async def on_member_remove(member):
    with open("./Datas/JSON/Setting.json", 'r', encoding='utf8') as jfile:
        jdata = json.load(jfile)
    channel = bot.get_channel(int(jdata['Leave_Channel_ID']))
    print(f'id:{member.id}')
    print(f'name:{member.name}Leave..')
    await channel.send(
        f'用戶名稱:{member.name}\n用戶ID:{member.id}\n**離開了{member.guild.name}。･ﾟ･(つд`ﾟ)･ﾟ･**'
    )


#EVT==新增回應====#
@bot.event
async def on_raw_reaction_add(payload):
    # CODE HERE
    role = None
    if payload.message_id == int(jdata['Roles_Msg']):
        print("---add_roles---")
        print(payload.emoji.name)
        print(payload.message_id)
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        print(member)
        print("------------------")
        channel = bot.get_channel(payload.channel_id)
        with open("./Datas/CSV/Roles.csv", newline='',
                  encoding='utf8') as csvfile:
            # 讀取 CSV 檔案內容
            rows = csv.DictReader(csvfile)
            # 以迴圈輸出每一列
            for row in rows:
                if payload.emoji.name == row['emoji']:
                    role = discord.utils.get(payload.member.guild.roles,
                                             name=row['role'])
                    print(row['role'])
                    break
                else:
                    role = None
                    continue
        if role != None:
            await member.add_roles(role)
        elif role == None:
            channel = bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            user = bot.get_user(payload.user_id)
            emoji = payload.emoji
            await message.remove_reaction(emoji, user)
        else:
            pass
    else:
        pass


#EVT==移除回應====#
@bot.event
async def on_raw_reaction_remove(payload):
    # CODE HERE
    role = None
    if payload.message_id == int(jdata['Roles_Msg']):
        print("---remove_roles---")
        print(payload.emoji.name)
        print(payload.message_id)
        guild = bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        print(member)
        print("------------------")

        channel = bot.get_channel(payload.channel_id)

        # <RawReactionActionEvent message_id=805232709676957747 user_id=162107631811428352 channel_id=805191071620399146 guild_id=804690309405605918 emoji=<PartialEmoji animated=False name='🎮' id=None> event_type='REACTION_REMOVE' member=None>

        with open("./Datas/CSV/Roles.csv", newline='',
                  encoding='utf8') as csvfile:
            # 讀取 CSV 檔案內容
            rows = csv.DictReader(csvfile)
            # 以迴圈輸出每一列
            for row in rows:
                if (payload.emoji.name == row['emoji']):
                    role = discord.utils.get(member.guild.roles,
                                             name=row['role'])
                    print(row['role'])
                    break
                else:
                    role = None
                    continue
        if role != None:
            await member.remove_roles(role)
        else:
            pass
    else:
        pass


# 名字顏色
NameInColor = ''
# 身分令牌 Roles
s_BotLicense = '戰地工程師執照'
dict = {}
json_path = "./Datas/JSON/Setting.json"


# 用来存储数据
def get_json_data(json_path, col: str, value: str):
    # 获取json里面数据
    with open(json_path, 'rb', encoding='utf8') as f:
        # 定义为只读模型，并定义名称为f
        params = json.load(f)
        # 加载json文件中的内容给params
        params[col] = value
        # 修改内容
        print("params", params)
        # 打印
        dict = params
        # 将修改后的内容保存在dict中
    f.close()
    # 关闭json读模式
    return dict
    # 返回dict字典内容


def write_json_data(dict):
    # 写入json文件
    with open(json_path, 'w', encoding='utf8') as r:
        # 定义为写模式，名称定义为r
        json.dump(dict, r)
        # 将dict写入名称为r的文件中

    r.close()
    # 关闭json写模式


# 讀取Json檔案
with open("./Datas/JSON/Setting.json", 'r', encoding='utf8') as jfile:
    jdata = json.load(jfile)
'''
Role機器人執照 指令(以下)
'''


#CMD==更改歡迎頻道跟離開頻道====#
# 需要有頻道ID
# CC 進入 540192435918340116
# CC 離開 767437706006626326
# ChangeChannel 進入 540192435918340116
# ChangeChannel 離開 767437706006626326
@bot.command(name='ChangeChannel',
             description='The ChangeChannel command',
             aliases=['CC'])
async def change_welcome_id_chanel(ctx, welcome_and_leave, id):
    if '戰地工程師執照' not in [y.name.lower() for y in ctx.message.author.roles]:
        await ctx.send(f'<@!{ctx.author.id}> 你沒有戰地工程師執照，無法使用指令。')
    else:
        if welcome_and_leave == "進入":
            write_json_data(
                get_json_data("./Datas/JSON/Setting.json",
                              "Welcome_Channel_ID", id))
        elif welcome_and_leave == "離開":
            write_json_data(
                get_json_data("./Datas/JSON/Setting.json", "Leave_Channel_ID",
                              id))
        await ctx.send(f"<#{id}>已成功變成**{welcome_and_leave}**訊息頻道")


#CMD==更改進入自動添加的身分組====#
# 需要先新增身分組 才能使用此指令否則會有BUG，沒有自動判別是否有身分組的程式碼
# 需要先有二等兵的身分組
# CJR 二等兵
# ChangeJoinRole 二等兵
@bot.command(name='ChangeJoinRole',
             descriptin='The ChangeJoinRole command',
             aliases=['CJR'])
async def change_join_role(ctx, join_role: str = ""):
    if '戰地工程師執照' not in [y.name.lower() for y in ctx.message.author.roles]:
        await ctx.send(f'<@!{ctx.author.id}> 你沒有戰地工程師執照，無法使用指令。')
    else:
        if join_role != "":
            write_json_data(
                get_json_data("./Datas/JSON/Setting.json", "Join_Server_Role",
                              join_role))
            with open("./Datas/JSON/Setting.json", 'r',
                      encoding='utf8') as jfile:
                jdata = json.load(jfile)
            print(jdata['Join_Server_Role'])
            await ctx.send(f"已成功修改為，用戶進入伺服器， 自動添加身分組**{join_role}**")
        else:
            await ctx.send("請指定用戶進入伺服器自動添加的身分組")


#CMD==需要權限不然那樣太危險====#
# 刪文字 行數
# C 1
# Clear 1
@bot.command(name='Clear', description='The Clear command', aliases=['C'])
async def Clear(ctx, a: int = 1):
    if '戰地工程師執照' not in [y.name.lower() for y in ctx.message.author.roles]:
        await ctx.send(f'<@!{ctx.author.id}> 你沒有戰地工程師執照，無法使用指令。')
    else:
        if a < 0:
            a = 1
        a += 1
        await ctx.channel.purge(limit=a)


#CMD==調用使用者加入伺服器的時間====#
#JT @阿暴
#Joint @阿暴
@bot.command(name='JoinTime',
             description='The JoinTime command',
             aliases=['JT'])
async def JoinTime(ctx, member: discord.Member):
    #channel = bot.get_channel(int(jdata['WelcomeAndLeave_Channel']))
    if '戰地工程師執照' not in [y.name.lower() for y in ctx.message.author.roles]:
        await ctx.send(f'<@!{ctx.author.id}> 你沒有戰地工程師執照，無法使用指令。')
    else:
        tempDate = member.joined_at.__format__('%Y-%m-%d   %H:%M:%S')
        colour = random.randint(0, 16777215)
        embed_One = discord.Embed(
            title=f"**{member.name}**",
            description=f"\n\n加入伺服器時間為 : __{tempDate}__\n",
            color=discord.Colour(colour))
        pfp = member.avatar.url
        print(pfp)
        embed_One.set_thumbnail(url=f"{pfp}")
        await ctx.send(embed=embed_One)
        # .__format__('%A %d %B %Y at %H:%M')} 新版時間 Tuesday 09 July 2019 at 14:26
        # await ctx.send(pytz.utc.localize(member.joined_at)) 舊版時間 2019-07-09 14:26:15.085000+00:00


# https://stackoverflow.com/questions/47733376/how-do-i-make-a-list-of-all-members-in-a-discord-server-using-discord-py


#CMD==印出所有用戶====#
# UL
# UserList
@bot.command(name='UserList',
             description='The UserList command',
             aliases=['UL'])
async def UserList(ctx):
    x = ctx.guild.members

    print(ctx.guild.members)

    y = [[[[]]]]
    y.clear()
    for member in x:
        y.append([
            member.id, member.name,
            member.joined_at.__format__('%Y-%m-%d  %H:%M:%S'),
            member.avatar.url
        ])

    y.sort(key=takeSecond)
    # print(y)
    tempMsg = ""
    for a in y:
        colour = random.randint(0, 16777215)
        embed_One = discord.Embed(
            title=f"**{a[1]}**",
            description=f"<@!{a[0]}>\n加入伺服器時間為 : {a[2]}\n",
            color=discord.Colour(colour))
        pfp = a[3]
        print(pfp)
        embed_One.set_thumbnail(url=f"{pfp}")
        await asyncio.sleep(1.0)
        await ctx.send(embed=embed_One)
        # tempMsg+=a[3]+"\n"

    # print(tempMsg)
    # await ctx.send(tempMsg)


def takeSecond(elem):
    return elem[2]


# https://stackoverflow.com/questions/48216914/how-to-add-and-create-roles-in-discord-py
# 改顏色 行數
#!!ㄍchangecolor @湮🥀  419ead 之類的
@bot.command(name='CreateRole',
             description='The CreateRole command',
             aliases=['CR'])
async def CreateRole(ctx, member: discord.Member, rolnname: str, color: str):
    if '戰地工程師執照' not in [y.name.lower() for y in ctx.message.author.roles]:
        await ctx.send(f'<@!{ctx.author.id}> 你沒有戰地工程師執照，無法使用指令。')
    else:
        colour = random.randint(0, 16777215)
        colour = int(color, 16)
        clr = discord.Colour(colour)
        print(clr)
        # server no = guild
        # https://cloud.tencent.com/developer/ask/131691
        #server = ctx.message.guild.id

        # https://stackoverflow.com/questions/48216914/how-to-add-and-create-roles-in-discord-py
        # ctx.guild
        # color字串轉為16進制
        role = await ctx.guild.create_role(name=rolnname)
        await member.add_roles(role)
        await role.edit(role=rolnname, colour=clr)
        await ctx.send(
            f':heart::heart:已成功新增身分組:heart::heart:\n新增的用戶：<@!{member.id}>\n身分組：{rolnname}\n色碼：{color}'
        )


'''
//新增某個令牌給誰
role = discord.utils.get(ctx.guild.roles,name='玩家')
await ctx.author.add_roles(role)
'''


# 查看跟機器人的網路連線速度
@bot.command(name='Ping', description='The Ping command', aliases=['P'])
async def Ping(ctx):
    await ctx.send(
        f'機器人目前延遲(毫秒)：{round(bot.latency*1000)} ms\n http://ehci.myselfnas.com:8087/'
    )


@bot.command(name='Info', description='The Info command', aliases=['i'])
async def Info(ctx):
    embed = discord.Embed(title="nice bot",
                          description="Nicest bot there is ever.",
                          color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="<YOUR-USERNAME>")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite thsi bot to their server
    embed.add_field(
        name="Invite",
        value="[Invite link](<insert your OAuth invitation link here>)")

    await ctx.send(embed=embed)


bot.remove_command('help')


@bot.command(name='Discord', description='The Discord command', aliases=['DC'])
async def Discord(ctx):
    # 0x1afd9c 0x00ffff 0x2894ff 0x6a6aff 0xc07ab8 0xa6a6d2 '0x6fb7b7' 0x00caca
    # https://home.gamer.com.tw/creationDetail.php?sn=3409319 巴哈DC教學連結
    embed_One = discord.Embed(
        title="**Discord特殊訊息教學**",
        url='https://home.gamer.com.tw/creationDetail.php?sn=3409319',
        description="DC文本教學\n",
        color=0x6fb7b7)
    embed_One.set_thumbnail(url=jdata['Server_Icon'])
    embed_One.add_field(name="斜體", value="*斜體*", inline=True)
    embed_One.add_field(name="粗體", value="**粗體**", inline=True)
    embed_One.add_field(name="粗斜體", value="***粗斜體***", inline=True)
    embed_One.add_field(name="刪除線", value="~~刪除線~~", inline=True)
    embed_One.add_field(name="底線", value="__底線__", inline=True)
    embed_One.add_field(name="底線斜體", value="__*底線斜體*__", inline=True)
    embed_One.add_field(name="底線粗體", value="__**底線粗體**__", inline=True)
    embed_One.add_field(name="底線粗斜體", value="___***底線粗斜體***___", inline=True)
    embed_One.add_field(name="引言", value="`引言`", inline=True)
    embed_One.add_field(name="區塊引言", value="```區塊引言```", inline=True)
    embed_One.add_field(name="暗黑密語", value="||黑暗密語||", inline=True)

    # 0x1afd9c 0x00ffff 0x2894ff 0x6a6aff 0xc07ab8 0xa6a6d2 0x6fb7b7 '0x00caca'
    embed_Two = discord.Embed(title="**Discord特殊訊息教學**",
                              description="DC文本教學\n",
                              color=0x00caca)
    embed_Two.add_field(name="斜體", value="\*斜體\*", inline=True)
    embed_Two.add_field(name="粗體", value="\*\*粗體\*\*", inline=False)
    embed_Two.add_field(name="粗斜體", value="\*\*\*粗斜體\*\*\*", inline=False)
    embed_Two.add_field(name="刪除線", value="\~\~刪除線\~\~", inline=False)
    embed_Two.add_field(name="底線", value="\_\_底線\_\_", inline=False)
    embed_Two.add_field(name="底線斜體", value="\_\_\*底線斜體\*\_\_", inline=False)
    embed_Two.add_field(name="底線粗體",
                        value="\_\_\*\*底線粗體\*\*\_\_",
                        inline=False)
    embed_Two.add_field(name="底線粗斜體",
                        value="\_\_\_\*\*\*底線粗斜體\*\*\*\_\_\_",
                        inline=False)
    embed_Two.add_field(name="引言", value="\`引言\`", inline=False)
    embed_Two.add_field(name="區塊引言", value="\`\`\`區塊引言\`\`\`", inline=False)
    embed_Two.add_field(name="暗黑密語", value="\|\|黑暗密語\|\|", inline=False)
    embed_Two.set_footer(
        text="教學網址 ： https://home.gamer.com.tw/creationDetail.php?sn=3409319")
    '''
    1.字體格式
    斜體 = *斜體*
    粗體  = **粗體**
    粗斜體 = ***粗斜體***
    刪除線 = ~~刪除線~~
    底線 = __底線__
    底線斜體 = __*底線斜體*__
    底線粗體 = __**底線粗體**__
    底線粗斜體 = ___***底線粗斜體***___
    引言 = `引言`
    區塊引言 = ```區塊引言```
    暗黑密語 = ||黑暗密語||
    '''
    await ctx.send(embed=embed_One)
    await ctx.send(embed=embed_Two)


@bot.command(name='Help', description='The Help command', aliases=['h'])
async def Help(ctx, Mode: str = ''):
    # 樣式頁面py產生器
    # https://cog-creators.github.io/discord-embed-sandbox/
    # ALL
    pattern_Zero = re.compile("^[Aa][Ll][Ll]+$")
    pattern_Zero_t = re.compile("^[Aa]$")

    # Admin
    pattern_Two = re.compile("^[Aa][Dd][Mm][Ii][Nn]+$")
    pattern_Two_t = re.compile("^[Aa][Dd]+$")
    # Player
    pattern_Three = re.compile("^[Pp][Ll][Aa][Yy][Ee][Rr]+$")
    pattern_Three_t = re.compile("^[Pp]+$")
    # Normal
    pattern_Four = re.compile("^[Nn][Oo][Rr][Mm][Aa][Ll]+$")
    pattern_Four_t = re.compile("^[nN]$")

    def embed_Admin_Cmd():
        embed_Two = discord.Embed(title="**管理員指令**",
                                  description="管理員指令:",
                                  color=0x1afd9c)
        embed_Two.add_field(name=CommandPrefix + "Clear n" + "\n" +
                            CommandPrefix + "C n",
                            value="向上清除n則訊息",
                            inline=True)
        embed_Two.add_field(name=CommandPrefix + "CreateRole @用戶 身分組名稱 色碼" +
                            "\n" + CommandPrefix + "CR @用戶 身分組名稱 色碼",
                            value="新增身分組給用戶",
                            inline=False)
        embed_Two.add_field(name=CommandPrefix + "JoinTime @用戶" + "\n" +
                            CommandPrefix + "JT @用戶",
                            value="調出用戶加入時間",
                            inline=False)
        embed_Two.add_field(name=CommandPrefix +
                            "ChangeChannel 進入/離開 Channel_ID" + "\n" +
                            CommandPrefix + "CC 進入/離開 Channel_ID",
                            value=f"更改進入或離開的頻道",
                            inline=False)
        embed_Two.add_field(name=CommandPrefix + "ChangeJoinRole 身分組" + "\n" +
                            CommandPrefix + "CJR 身分組",
                            value=f"更改進入伺服器自動添加的身分組",
                            inline=False)
        return embed_Two

    def embed_Normal_Cmd():
        embed_Four = discord.Embed(title="**一般指令**",
                                   description="一般指令:",
                                   color=0x00FFFF)
        embed_Four.add_field(name=CommandPrefix + "Ping" + "\n" +
                             CommandPrefix + "P",
                             value="查看機器人連線Ping值",
                             inline=False)
        return embed_Four

    def embed_Help_Cmd():
        embed_Five = discord.Embed(title="**指令教學**",
                                   description="指令教學:",
                                   color=0x2894FF)
        embed_Five.add_field(name=CommandPrefix + "Help Admin" + "\n" +
                             CommandPrefix + "H AD",
                             value="管理員指令簡介",
                             inline=False)
        embed_Five.add_field(name=CommandPrefix + "Help Normal" + "\n" +
                             CommandPrefix + "H N",
                             value="一般指令簡介",
                             inline=False)
        embed_Five.add_field(name=CommandPrefix + "Help All" + "\n" +
                             CommandPrefix + "H A",
                             value="印出所有指令",
                             inline=False)
        return embed_Five

    # All_Cmd
    if pattern_Zero.match(Mode) or pattern_Zero_t.match(Mode):
        # https://www.ifreesite.com/color/
        await ctx.send(embed=embed_Admin_Cmd())
        await ctx.send(embed=embed_Normal_Cmd())
        await ctx.send(embed=embed_Help_Cmd())
        return
    # NiceBot_Cmd

    # Admin_Cmd
    if pattern_Two.match(Mode) or pattern_Two_t.match(Mode):
        await ctx.send(embed=embed_Admin_Cmd())
        return

    # Normal_Cmd
    if pattern_Four.match(Mode) or pattern_Four_t.match(Mode):
        await ctx.send(embed=embed_Normal_Cmd())
        return
    # Help_Cmd
    else:
        await ctx.send(embed=embed_Help_Cmd())
        return

########################
#########考拉區##########
########################
Koala_path = "./Koala/{}"

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

keep_alive()
'''
guild.members
bot.get_all_members():
bot.users
'''
bot.run(jdata['TOKEN'])
