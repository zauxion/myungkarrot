import imp
from tkinter import Menu
import discord
from captcha.image import ImageCaptcha
import random
import time
import asyncio
import json
import sys
import urllib
import requests
import os
from bs4 import BeautifulSoup
from gtts import gTTS
import discord
import asyncio
import random
import openpyxl
from discord import Member
from discord.ext import commands
import youtube_dl
from urllib.request import urlopen, Request
import urllib
import urllib.request
import bs4
import os
import sys
import json
from selenium import webdriver
import time
import datetime


client = discord.Client()
token = 'OTQ1OTA1MTUzMzEwMDg5MjE2.YhW80g.iHzVDbkiCyRfpu6wi3O2EGN9138'
_channel = '946806716576714793'

@client.event
async def on_ready():
    print(client.user)

@client.event
async def on_message(message):
    if message.content.startswith("!인증"):    #명령어 !인증
        if not message.channel.id == int(_channel):
            return
        a = ""
        Captcha_img = ImageCaptcha()
        for i in range(6):
            a += str(random.randint(0, 9))

        name = str(message.author. id) + ".png"
        Captcha_img.write(a, name)

        nummsg = await message.channel.send(f"{message.author.mention} 아래 숫자를 10초 내에 입력해주세요.", file=discord.File(name))

        def check(msg):
            return msg.author == message.author and msg.channel == message.channel

        try:
            msg = await client.wait_for("message", timeout=10, check=check) # 제한시간 
        except:
            await nummsg.delete()
            await message.delete()
            chrhkEmbed = discord.Embed(title='❌ 인증실패', color=0xFF0000)
            chrhkEmbed.add_field(name='닉네임', value=message.author, inline=False)
            chrhkEmbed.add_field(name='이유', value='시간초과', inline=False)
            await message.channel.send(embed=chrhkEmbed)
            print(f'{message.author} 님이 시간초과로 인해 인증을 실패함.')
            return

        if msg.content == a:
            role = discord.utils.get(message.guild.roles, name="귀요미")

            await nummsg.delete()
            await message.delete()
            await msg.delete()
            tjdrhdEmbed = discord.Embed(title='인증성공', color=0x04FF00)
            tjdrhdEmbed.add_field(name='닉네임', value=message.author, inline=False)
            tjdrhdEmbed.add_field(name='3초후 인증역할이 부여됩니다.', value='** **', inline=False)
            tjdrhdEmbed.set_thumbnail(url=message.author.avatar_url)
            await message.channel.send(embed=tjdrhdEmbed)
            await asyncio.sleep(3)
            await message.author.add_roles(role)
        else:
            await nummsg.delete()
            await message.delete()
            await msg.delete()
            tlfvoEmbed = discord.Embed(title='❌ 인증실패', color=0xFF0000)
            tlfvoEmbed.add_field(name='닉네임', value=message.author, inline=False)
            tlfvoEmbed.add_field(name='이유', value='잘못된 숫자', inline=False)
            await message.channel.send(embed=tlfvoEmbed)
            print(f'{message.author} 님이 잘못된 숫자로 인해 인증을 실패함.')

    if message.content.startswith('!폭파'):
        if message.author.guild_permissions.manage_messages:
            aposition = message.channel.position
            new = await message.channel.clone()
            await message.channel.delete()
            await new.edit(position=aposition)

            embed = discord.Embed(title='채널 폭파됨', colour=discord.Colour.red())
            embed.set_image(url='https://media.giphy.com/media/HhTXt43pk1I1W/giphy.gif')
            await new.send(embed=embed)

    if message.content.startswith('!청소'):
        try:
            # 메시지 관리 권한 있을시 사용가능
            if message.author.guild_permissions.manage_messages:
                amount = message.content[4:]
                await message.delete()
                await message.channel.purge(limit=int(amount))
                message = await message.channel.send(embed=discord.Embed(title='🧹 메시지 ' + str(amount) + '개 삭제됨', colour=discord.Colour.green()))
                await asyncio.sleep(2)
                await message.delete()
            else:
                await message.channel.send('``명령어 사용권한이 없습니다.``')
        except:
            pass

    if message.guild is None:
        if message.author.bot:
            return
        else:
            embed = discord.Embed(colour=discord.Colour.blue(), timestamp=message.created_at)
            embed.add_field(name='전송자', value=message.author, inline=False)
            embed.add_field(name='내용', value=message.content, inline=False)
            embed.set_footer(text=f'!디엠 <@{message.author.id}> [할말] 을 통해 답장을 보내주세요!')
            await client.get_channel(946807282224734218).send(f"`{message.author.name}({message.author.id})`", embed=embed)

    if message.content.startswith('!디엠'):
        if message.author.guild_permissions.manage_messages:
            msg = message.content[26:]
            await message.mentions[0].send(f"**{message.author.name}** 님의 답장: {msg}")
            await message.channel.send(f'`{message.mentions[0]}`에게 DM을 보냈습니다')
        else:
            return

    with open('./setting.json', 'r') as boo:
        data = json.load(boo)
    setting = data['percent']

    if not setting.isdecimal() or int(setting) > 100:
        print(f'수수료 퍼센트({setting})가 잘못되었습니다\nsetting.json을 수정해주세요')
        time.sleep(3)
        await client.logout()
        sys.exit()
    print(f"수수료봇 온라인\n설정된 수수료: {setting}%")


    if message.content.startswith("!수수료") and not message.content.startswith("!수수료수정"):
        with open('./setting.json', 'r') as boo:
            data = json.load(boo)
        setting = data['percent']

        try:
            amount = message.content.split(" ")[1]
        except IndexError:
            await message.channel.send(f'{message.author.mention} 값이 설정되지 않았습니다')
            return

        if not amount.isdecimal():
            await message.channel.send(f'{message.author.mention} 값이 숫자가 아닙니다')
            return

        result = int(amount) * (100-int(setting)) / 100
        result = round(result)
        await message.channel.send(f'{message.author.mention},\n**`{amount}`원의 수수료({setting}%)를 제외한 값은 `{result}`원입니다**')

    if message.content.startswith('!수수료수정') or message.content.startswith('!수정'):
        if message.author.guild_permissions.manage_messages:
            try:
                edit_amount = message.content.split(" ")[1]
            except:
                embed = discord.Embed(title='!수수료수정 [숫자]', description='')
                await message.channel.send(embed=embed)
                return

            if not edit_amount.isdecimal() or int(edit_amount) > 100:
                embed = discord.Embed(title='!수수료수정 [숫자]', description='')
                await message.channel.send(embed=embed)
                return

            with open('./setting.json', 'r') as boo:
                data = json.load(boo)
            data['percent'] = edit_amount
            with open('./setting.json', 'w', encoding='utf-8') as making:
                json.dump(data, making, indent="\t")
            s = data['percent']
            await message.channel.send(f'수수료가 `{s}`%로 수정되었습니다')

    if message.content.startswith("/출근"):
        try:
            # 메시지 관리 권한 있을시 사용가능
            if message.author.guild_permissions.manage_messages:
                embed = discord.Embed(color=0x80E12A)
                channel = 946812246523260938
                embed.set_author(name=message.author, icon_url=message.author.avatar_url)
                embed.add_field(name='관리자 출퇴근 알림', value='관리자가 출근하였습니다.')
                #embed.set_image(url="")
                await client.get_channel(int(channel)).send(embed=embed)
        except:
            pass

    if message.content.startswith("/퇴근"):
        try:
            if message.author.guild_permissions.manage_messages:
                embed = discord.Embed(color=0xFF0000)
                channel = 946812246523260938
                embed.set_author(name=message.author, icon_url=message.author.avatar_url)
                embed.add_field(name='관리자 출퇴근 알림', value='관리자가 퇴근하였습니다.')
                #embed.set_image(url="")
                await client.get_channel(int(channel)).send(embed=embed)
        except:
            pass

    if message.content.startswith('!주사위'):
        randomNum = random.randrange(1, 7)
        if randomNum == 1:
            await message.channel.send(embed=discord.Embed(description=':one:', color=0x7C40E5))
        if randomNum == 2:
            await message.channel.send(embed=discord.Embed(description=':two:', color=0x7C40E5))
        if randomNum == 3:
            await message.channel.send(embed=discord.Embed(description=':three:', color=0x7C40E5))
        if randomNum == 4:
            await message.channel.send(embed=discord.Embed(description=':four:', color=0x7C40E5))
        if randomNum == 5:
            await message.channel.send(embed=discord.Embed(description=':five:', color=0x7C40E5))
        if randomNum == 6:
            await message.channel.send(embed=discord.Embed(description=':six: ', color=0x7C40E5))

    if message.content.startswith('!문상') or message.content.startswith('!문화상품권'):
        a = random.randint(2000, 4900)
        b = random.randint(1000, 9999)
        b2 = random.randint(1000, 9999)
        c = random.randint(100000,999999)
        TICKETembed = discord.Embed(title='문상 생성기', description=str(a) + '-' + str(b) + '-' + str(b2) + '-' + str(c))
        await message.channel.send(embed=TICKETembed)

    if message.content == '!unban':
        if not message.author.guild_permissions.administrator:
            return
        bans = await message.guild.bans()
        lists = ["{0.id}".format(entry.user) for entry in bans]

        for i in lists:
            a = await client.fetch_user(i)
            await message.guild.unban(a)
            print(f'{a} was unbanned')
            await message.channel.send(f'{a} was unbanned')


client.run('OTQ1OTA1MTUzMzEwMDg5MjE2.YhW80g.iHzVDbkiCyRfpu6wi3O2EGN9138')