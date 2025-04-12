from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode
import config
from ..logging import LOGGER

class Anony(Client):
    def __init__(self):
        LOGGER(__name__).info("Starting Bot...")
        super().__init__(
            name="AnonXMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        # Debugging log to check the logger_id
        LOGGER(__name__).info(f"Attempting to send a message to chat_id: {config.LOGGER_ID}")

        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
            LOGGER(__name__).info("Message sent successfully to the log group/channel.")
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\nReason: {type(ex).__name__}, {str(ex)}"
            )
            exit()

        # Check if the bot is an admin in the log group/channel
        try:
            a = await self.get_chat_member(config.LOGGER_ID, self.id)
            if a.status != ChatMemberStatus.ADMINISTRATOR:
                LOGGER(__name__).error(
                    "Please promote your bot as an admin in your log group/channel."
                )
                exit()
            LOGGER(__name__).info(f"Music Bot Started as {self.name}")
        except Exception as ex:
            LOGGER(__name__).error(
                f"Error while checking admin status: {str(ex)}"
            )
            exit()

    async def stop(self):
        await super().stop()
