import asyncio
import os
import time
from telethon.sync import TelegramClient
from telethon import events

# Replace with your API credentials
API_ID = 20075117
API_HASH = "e1753986de434132c0eb407b552a9d0d"
PHONE_NUMBER = "+"
SESSION_NAME = "PYROGRAMSESSION"

# Pre-inputted Chat IDs
GROUP_CHATS = [
    -1001989302520,
    -1001838544499,
    -4061785075,
  
]

last_message_time = {}
# Initialize the ad message and default posting interval (3600 seconds = 1 hour)
ad_message = 'Default ad message. Use /changead to update it'
post_interval = 3600

# Define the lock file path (change it to a suitable location)
LOCK_FILE = 'bot_lock.lock'

async def main():
    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        # Check if the user ID is the desired one (6198670602)
        desired_user_id = 6198670602
        if (user := await client.get_me()).id != desired_user_id:
            print("Bot is not authorized for this user ID. Exiting.")
            return

    # Check if the lock file exists
    if os.path.exists(LOCK_FILE):
        print("Another instance of the bot is already running. Exiting.")
        return

    # Create the lock file to prevent other instances
    with open(LOCK_FILE, 'w') as lockfile:
        lockfile.write(str(os.getpid()))

    async with TelegramClient(SESSION_NAME, API_ID, API_HASH) as client:
        try:
            await client.start()
            print("Bot started.")

            @client.on(events.NewMessage(pattern='/addgroup'))
            async def add_group(event):
                chat_id = event.chat_id

                # Check if the chat has slow mode enabled and if a delay is required
                if chat_id in last_message_time:
                    elapsed_time = time.time() - last_message_time[chat_id]
                    if elapsed_time < 3599:
                        return  # Do not respond if in cooldown

                last_message_time[chat_id] = time.time()  # Update the last message time

                # Proceed with adding the group logic
                if chat_id not in GROUP_CHATS:
                    GROUP_CHATS.append(chat_id)
                    await event.respond("Group added successfully.")  # Respond to the command
                else:
                    await event.respond("Group already in the list.")  # Respond to the command

            @client.on(events.NewMessage(pattern='/listgroups'))
            async def list_groups(event):
                if GROUP_CHATS:
                    response = "List of groups where ads will be posted:\n"
                    for chat_id in GROUP_CHATS:
                        response += f"- Chat ID: {chat_id}\n"
                else:
                    response = "No groups added yet."
                await event.respond(response)

            @client.on(events.NewMessage())
            async def auto_sender(event):
                await asyncio.sleep(60)
                await client.send_message("me", "/postad")
                for chat_id in GROUP_CHATS:
                    try:
                        await client.send_message(chat_id, ad_message)
                    except Exception as e:
                        pass  # Ignore errors

            @client.on(events.NewMessage(pattern='/changead'))
            async def change_ad(event):
                global ad_message
                ad_message = event.text.replace('/changead ', '')
                await event.respond('Ad message updated successfully.')

            @client.on(events.NewMessage(pattern='/changeinterval'))
            async def change_interval(event):
                global post_interval
                try:
                    new_interval = event.text.split(' ')[1]
                    post_interval = int(new_interval)
                    await event.respond(f"Interval set to {post_interval} seconds.")
                except (IndexError, ValueError):
                    await event.respond("Invalid interval. Please provide a valid number of seconds.")

            await client.run_until_disconnected()

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        finally:
            # Remove the lock file to release the lock
            os.remove(LOCK_FILE)

if __name__ == '__main__':
    asyncio.run(main())
