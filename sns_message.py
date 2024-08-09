import datetime
import requests
# Discord
def send_message(msg):
    now = datetime.datetime.now()

    DISCORD_WEBHOOK_URL =""

    message = {"content": f"**{str(msg)}**\n Date: {now.strftime('%Y-%m-%d %H:%M:%S')}"}
    requests.post(DISCORD_WEBHOOK_URL, data=message)
    print(message)


import telegram
# Telegram Message
# When calling a function, use 'asyncio.run()'!
async def send_tel_message(message):

    token_tel_coin = ""

    chat_id_tel = ""
    
    bot = telegram.Bot(token = token_tel_coin)

    return await bot.send_message(chat_id_tel, message)