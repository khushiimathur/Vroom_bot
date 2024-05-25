from telethon.sync import TelegramClient, events
from telethon.sessions import StringSession

api_id = 26864957
api_hash = '0148f496077b4d88053cfc6e20ce0903'
bot_token = '7162081466:AAEyI9UeOmAxKQh_pC2hkiPBz94PcZf_28k'

# We have to manually call "start" if we want an explicit bot token
bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

@bot.on(events.NewMessage(pattern='/start'))
async def handleStart(event):
    await event.respond('Hi, I am a bot!')

# This is for every other message which doesn't match the above patterns
@bot.on(events.NewMessage())
async def handleMessage(event):
    if event.message.message[0] == '/':
        return # IF this is a Telegram command, then ignore the processing

    # Change this with whatever processing you like.
    await event.respond('Here is what you sent to me.\n\n' + str(event.message.message))

bot.run_until_disconnected()
