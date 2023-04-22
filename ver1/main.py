# 모듈 설치
import json
import requests
from bs4 import BeautifulSoup
from datetime import date

import discord
from discord.ext import commands

# 봇 설정하기
with open('config.json') as f:
    config = json.load(f)
    
client = commands.Bot(command_prefix='!', intents=discord.Intents.all())
version = 1

# 실행
@client.event
async def on_ready():
    print(f'동명대학교 학식 알리미 봇\nVer: {version}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="공부"))
    

@client.command()
async def 학식(ctx):
    # 검색 설정
    today = date.today()
    url = "https://www.tu.ac.kr/tuhome/diet.do?schDate="+str(today)
    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser')

    # 예외처리
    try:
        # 데이터 가져오기
        data1 = soup.select("#cms-content > div > div > div.table-wrap > table > tbody > tr:nth-child(1) > td")[0].get_text()
        data2 = soup.select("#cms-content > div > div > div.table-wrap > table > tbody > tr:nth-child(5) > td")[0].get_text()
        data3 = soup.select("#cms-content > div > div > div.table-wrap > table > tbody > tr:nth-child(6) > td")[0].get_text()

        # 학식 출력하기
        embed = discord.Embed(title="**오늘의 학식**", description=today, color=0xf0f8ff)
        embed.add_field(name="**양식**", value=">>> " + data1, inline=False)
        embed.add_field(name="**뚝배기**", value=">>> " + data2, inline=False)
        embed.add_field(name="**일품**", value=">>> " + data3, inline=False)
            
    except IndexError:
        embed = discord.Embed(title="**오늘의 학식이 없습니다.**", description=today, color=0xe86100)

    # 메시지 전송하기
    await ctx.send(embed=embed)

client.run(config['Token'])
