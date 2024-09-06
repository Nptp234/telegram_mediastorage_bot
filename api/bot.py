import os
import requests
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
from telethon import TelegramClient, events
from telethon.tl.custom import dialog

# Load environment variables
load_dotenv()

# Replace with your bot's token
TOKEN = os.getenv('TELEGRAM_BOT')
API_HASH = os.getenv('API_HASH')
API_ID = os.getenv('API_ID')
CHAT_ID = os.getenv('CHAT_ID')

# Initialize the Telegram client
client = TelegramClient('bot_session', API_ID, API_HASH).start(bot_token=TOKEN)

# async def download_image_user(file_id, bot):
#     file_info = await bot.get_file(file_id)
#     file_path = file_info.file_path
#     file_url = f'https://api.telegram.org/file/bot{TOKEN}/{file_path}'
    
#     # Save the image to your local system
#     os.makedirs('./images', exist_ok=True)
#     local_file_path = f'./images/{file_id}.jpg'
#     response = requests.get(file_url)
#     with open(local_file_path, 'wb') as f:
#         f.write(response.content)
    
#     return file_url, local_file_path


async def get_file_info(file_id):
    # Fetch the file info from the message
    message = await client.get_messages('me', ids=file_id)
    if message.photo:
        file_path = message.photo[0].file_id
    elif message.document:
        file_path = message.document.file_name
    else:
        file_path = None
    return file_path


@client.on(events.NewMessage)
async def handle_image_user(event) -> None:
    # bot = context.bot
    # # Get file ID and process it
    file_id = event.photo.id
    # file_path = await get_file_info(file_id)
    
    file = await event.download_media()
    file_url, local_file_url = await download_image(file)
    
    # parts = file_path.split('/https://', 1)

    # if len(parts) == 2:
    #     part1 = f'{parts[0]}/'
    #     part2 = f'https://{parts[1]}'
        
    #     print(f'Part 1: {part1}')
    #     print(f'Part 2: {part2}')
    # else:
    #     print('URL format is unexpected.')
    
    await event.respond(f'Image saved: {local_file_url}')  # Await this call
    await event.respond(f'Public URL (no download): {file_url}')  # Await this call

# Function to download the image
async def download_image(file):
    # Save the image to your local system
    os.makedirs('./images', exist_ok=True)
    local_file_path = f'./images/{os.path.basename(file)}'
    os.rename(file, local_file_path)
    print(f"{file}")
    
    file_url = f'https://api.telegram.org/file/bot{TOKEN}/photos/{file}'
    
    response = requests.get(file_url)
    with open(local_file_path, 'wb') as f:
        f.write(response.content)
    
    return file_url, local_file_path
        

async def get_chat_id(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    await update.message.reply_text(f'Your Chat ID is: {chat_id}')

def main():
    # # Set up the Application to handle messages
    # application = Application.builder().token(TOKEN).build()

    # # Handle images sent to the bot
    # application.add_handler(MessageHandler(filters.PHOTO, handle_image_user))
    
    # application.add_handler(CommandHandler('getchatid', get_chat_id))

    # # Start the bot
    # application.run_polling()
    
    print("Bot is running...")
    client.add_event_handler(handle_image_user, events.NewMessage)
    client.run_until_disconnected()
    

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())