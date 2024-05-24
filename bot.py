from telethon.sync import TelegramClient
from telethon.sessions import StringSession

api_id = 26864957
api_hash = '0148f496077b4d88053cfc6e20ce0903'
bot_token = '7162081466:AAEyI9UeOmAxKQh_pC2hkiPBz94PcZf_28k'

# We have to manually call "start" if we want an explicit bot token
bot = TelegramClient(StringSession(), api_id, api_hash).start(bot_token=bot_token)


async def main():
    if bot.is_client_authorized():
        print('Yes')

main()

# But then we can use the client instance as usual
#with bot:
