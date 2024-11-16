import datetime
import requests

# Discord
def send_message(msg):
    now = datetime.datetime.now()

    DISCORD_WEBHOOK_URL =""
   
    embed = { 
        "title": "Your Title", 
        "description": f"{str(msg)}", 
        "color": 5814783, # 색상은 10진수로 입력 (여기서는 초록색) 
        "timestamp": now.isoformat(), 
        "footer": { "text": "Your Footer Text" }, 
        "fields": [ { "name": "Field1", "value": "Field1 Value", "inline": False }, { "name": "Field2", "value": "Field2 Value", "inline": True } ] } 
    
    message = { "username": "Your Bot Name", "embeds": [embed] } 
    headers = { "Content-Type": "application/json" } 
    response = requests.post(DISCORD_WEBHOOK_URL, json=message, headers=headers) 

    print(response.status_code,response.text)

send_message("This is a test message")


import telegram
# Telegram Message
# When calling a function, use 'asyncio.run()'!
async def send_tel_message(message):

    # API
    token_tel_coin = ""

    # Make Group and Post Group Chat id
    chat_id_tel = ""
    
    bot = telegram.Bot(token = token_tel_coin)

    return await bot.send_message(chat_id_tel, message)
