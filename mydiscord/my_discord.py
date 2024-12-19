from datetime import datetime, timezone, timedelta
import requests
import yaml

with open('',"r",encoding='UTF-8') as f:
    info = yaml.load(f, Loader=yaml.FullLoader)

# Discord
def send_message(bot_name, title, discription, exchange, symbol, time, color = 65280):
    now = datetime.now(timezone(timedelta(hours=9)))

    DISCORD_WEBHOOK_URL =info['discord_coin']
   
    embed = { 
        "title": f"{str(title)}", 
        "description": f"{str(discription)}", 
        "color": color, # 색상은 10진수로 입력
        "timestamp": now.isoformat(), 
        "footer": { "text": "www.ditia.com" }, 
        "fields": [ { "name": "거래소", "value": f"{str(exchange)}", "inline": False }, { "name": "Symbol", "value": f"{str(symbol)}", "inline": False }, 
                   { "name": "체결 시간", "value": f"{str(time)}", "inline": False } ] } 
    
    message = { "username": f"{str(bot_name)}", "embeds": [embed] } 
    headers = { "Content-Type": "application/json" } 
    response = requests.post(DISCORD_WEBHOOK_URL, json=message, headers=headers) 

    print(response.status_code,response.text)

# 현재 시간 가져오기 (시간대 포함) 
now = datetime.now(timezone(timedelta(hours=9)))

# 형식 지정 (초까지 포함) 
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

# color
color_standard = 5814783
color_red      = 16711680
color_green    = 65280
color_yellow   = 16776960
color_orange   = 16753920
