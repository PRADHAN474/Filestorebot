from telethon.sync import TelegramClient, events
from telethon.tl.custom import Button
import os

# Replace 'your_api_id' and 'your_api_hash' with your actual API ID and API Hash
api_id = 'your_api_id'
api_hash = 'your_api_hash'

# Replace 'your_bot_token' with your actual bot token
bot_token = 'your_bot_token'

# Replace 'your_channel_username' with the username of your channel
channel_username = 'your_channel_username'

# Replace 'owner_id' with the user ID of the bot owner
owner_id = owner_id

# Create a TelegramClient
client = TelegramClient('file_store_bot', api_id, api_hash).start(bot_token=bot_token)

# Define the folder where you want to store the files
storage_folder = 'file_storage'

# Create an inline keyboard with buttons
def create_inline_keyboard():
    store_button = Button.inline('Store File', b'store')
    get_button = Button.inline('Get File', b'get')
    list_button = Button.inline('List Files', b'list')
    settings_button = Button.inline('Settings', b'settings')
    broadcast_button = Button.inline('Broadcast', b'broadcast')
    return Button.grid([store_button, get_button, list_button, settings_button, broadcast_button], cols=2)

# Start command to check channel membership and provide instructions
@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    user = await client.get_entity(event.sender_id)
    if not await client.is_participant(channel_username, user=user):
        await event.respond('You must join the channel to use this bot.')
    else:
        await event.respond('Welcome to the File Store Bot!', buttons=create_inline_keyboard())

# Storing files command
@client.on(events.NewMessage(pattern='/store'))
async def store_file(event):
    try:
        if event.message.media:
            # Download and store the file in the specified folder
            file = await event.message.download(file=f'{storage_folder}/{event.message.id}_{event.message.file.name}')
            await event.respond('File stored successfully!')
    except Exception as e:
        await event.respond(f'Error storing the file: {e}')

# Retrieving files command
@client.on(events.NewMessage(pattern='/get'))
async def get_file(event):
    try:
        requested_file_name = event.text.split('/get ')[1]
        requested_file_path = f'{storage_folder}/{requested_file_name}'
        if os.path.exists(requested_file_path):
            await event.respond(file=requested_file_path)
        else:
            await event.respond('File not found.')
    except Exception as e:
        await event.respond(f'Error retrieving the file: {e}')

# List stored files command
@client.on(events.NewMessage(pattern='/list'))
async def list_files(event):
    try:
        file_list = [f for f in os.listdir(storage_folder) if os.path.isfile(os.path.join(storage_folder, f)]
        if file_list:
            file_list_text = '\n'.join(file_list)
            await event.respond(f'Stored files:\n{file_list_text}')
        else:
            await event.respond('No files stored yet.')
    except Exception as e:
        await event.respond(f'Error listing files: {e}')

# Custom bot settings command (for the owner)
@client.on(events.NewMessage(pattern='/settings'))
async def bot_settings(event):
    if event.sender_id == owner_id:
        # Implement customization options here for the bot owner
        await event.respond('Customize the bot settings here.')
    else:
        await event.respond('You are not authorized to customize the bot.')

# Send a broadcast message (for the owner)
@client.on(events.NewMessage(pattern='/broadcast'))
async def broadcast(event):
    if event.sender_id == owner_id:
        try:
            message = event.text.split('/broadcast ')[1]
            await client.send_message(channel_username, message)
            await event.respond('Broadcast sent successfully.')
        except Exception as e:
            await event.respond(f'Error sending the broadcast: {e}')
    else:
        await event.respond('You are not authorized to send broadcasts.')

if name == 'main':
    client.run_until_disconnected()
