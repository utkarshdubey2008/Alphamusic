import asyncio
import importlib
from pyrogram import idle
from pytgcalls.exceptions import NoActiveGroupCall
import config
from AnonXMusic import LOGGER, app, userbot
from AnonXMusic.core.call import Anony
from AnonXMusic.misc import sudo
from AnonXMusic.plugins import ALL_MODULES
from AnonXMusic.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# MongoDB URI from .env
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
if not MONGO_DB_URI:
    LOGGER(__name__).error("MongoDB URI not found in environment variables, exiting...")
    exit()

# MongoDB client initialization
client = AsyncIOMotorClient(MONGO_DB_URI)
db = client.get_database("your_database_name")  # Specify your database name

# Database initialization function
async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("Assistant client variables not defined, exiting...")
        exit()

    await sudo()

    # Fetch banned users and add to the BANNED_USERS set
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)

        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except Exception as e:
        LOGGER(__name__).error(f"Error fetching banned users: {e}")

    # Start the main bot and userbot
    await app.start()
    for all_module in ALL_MODULES:
        importlib.import_module("AnonXMusic.plugins" + all_module)
    
    LOGGER("AnonXMusic.plugins").info("Successfully Imported Modules...")
    await userbot.start()
    await Anony.start()

    # Attempt to start a video call
    try:
        await Anony.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
    except NoActiveGroupCall:
        LOGGER("AnonXMusic").error("Please turn on the videochat of your log group/channel.\n\nStopping Bot...")
        exit()
    except Exception as e:
        LOGGER("AnonXMusic").error(f"Error starting video call: {e}")
    
    await Anony.decorators()

    LOGGER("AnonXMusic").info("Bot successfully started and running...")
    
    # Keep the bot running
    await idle()

    # Stop the bot and userbot gracefully
    await app.stop()
    await userbot.stop()
    LOGGER("AnonXMusic").info("Stopping AnonX Music Bot...")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
