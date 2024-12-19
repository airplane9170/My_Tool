import discord
from discord.ext import commands
import yaml

with open('C:\\Users\\airpl\\zoo\\strategy_coin\\info_API.yaml',"r",encoding='UTF-8') as f:
    info = yaml.load(f, Loader=yaml.FullLoader)

# intents 객체 생성 
intents = discord.Intents.all()
intents.messages = True 
intents.guilds =True

# 명령어 접두사 설정
bot = commands.Bot(command_prefix='!', intents=intents)

# 봇이 준비되었을 때 출력
# @: 데코레이터
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

# 청소 명령어
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clean(ctx, limit: int = 100):
    await ctx.channel.purge(limit=limit)
    await ctx.send(f'{limit}개의 메시지를 삭제했습니다.', delete_after=5)

# 봇 실행: Discord 창에 !clean 삭제할 메시지 갯수   (반드시 띄워쓰기 해야 됨)
bot.run(info['discord_bot'])
