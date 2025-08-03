# === Imports ===
from pyrogram import Client, filters  # Pyrogram for Telegram API interaction
from pyrogram.types import Message  # Telegram message object
from pymongo import MongoClient  # MongoDB client
from urllib.parse import quote_plus  # For safe username/password encoding in Mongo URI
import random  # For random selection of chatbot responses
from pyrogram.enums import ChatMembersFilter
import config

from config import API_ID, API_HASH, STRING_SESSION, MONGO_URL

# === Configuration ===

# === Initialization ===
bot = Client(
    name="autochat_session",  # session name is required
    session_string=STRING_SESSION,
    api_id=API_ID,
    api_hash=API_HASH
)

mongo_client = MongoClient(MONGO_URL)

# MongoDB collections
chatbot_db = mongo_client["Chats"]["ChatsDB"]
disable_db = mongo_client["RaxxDB"]["Raxx"]

# === Check Admin ===
async def is_admins(chat_id: int):
    admins = []
    async for member in bot.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        admins.append(member.user.id)
    return admins



# === Start Command ===
@bot.on_message(filters.command("start"))
async def start(client, message):
    try:
        await bot.join_chat("Teamxt_support")
    except Exception:
        pass
    await message.reply_text("🤖 ChatBot is Ready!")

# === Disable Chatbot ===
@bot.on_message(filters.command("chatbot off", prefixes=["/", ".", "?", "-"]) & ~filters.private)
async def chatbot_off(client, message):
    if message.from_user and message.from_user.id not in await is_admins(message.chat.id):
        return await message.reply_text("❌ You are not an admin.")
    if not disable_db.find_one({"chat_id": message.chat.id}):
        disable_db.insert_one({"chat_id": message.chat.id})
        await message.reply_text("🔕 Chatbot Disabled!")
    else:
        await message.reply_text("⚠️ Chatbot is already disabled.")

# === Enable Chatbot ===
@bot.on_message(filters.command("chatbot on", prefixes=["/", ".", "?", "-"]) & ~filters.private)
async def chatbot_on(client, message):
    if message.from_user and message.from_user.id not in await is_admins(message.chat.id):
        return await message.reply_text("❌ You are not an admin.")
    if disable_db.find_one({"chat_id": message.chat.id}):
        disable_db.delete_one({"chat_id": message.chat.id})
        await message.reply_text("✅ Chatbot Enabled!")
    else:
        await message.reply_text("⚠️ Chatbot is already enabled.")

# === Usage Help ===
@bot.on_message(filters.command("chatbot", prefixes=["/", ".", "?", "-"]) & ~filters.private)
async def chatbot_usage(client, message):
    await message.reply_text("📘 **Usage:**\n/chatbot [on|off] (Group Only)")

# === Core Chatbot Logic ===
@bot.on_message((filters.text | filters.sticker) & ~filters.bot)
async def chatbot_response(client: Client, message: Message):
    if message.chat.type != "private" and disable_db.find_one({"chat_id": message.chat.id}):
        return

    reply = message.reply_to_message
    bot_info = await bot.get_me()
    bot_id = bot_info.id

    if reply and reply.from_user and reply.from_user.id == bot_id:
        key = message.text if message.text else message.sticker.file_unique_id
        entries = list(chatbot_db.find({"word": key}))
        if entries:
            choice_data = random.choice(entries)
            if choice_data["check"] == "sticker":
                await message.reply_sticker(choice_data["text"])
            else:
                await message.reply_text(choice_data["text"])
        return

    if reply and reply.from_user.id != bot_id:
        key = reply.text if reply.text else reply.sticker.file_unique_id
        value = message.text if message.text else message.sticker.file_id
        check = "sticker" if message.sticker else "text"
        if not chatbot_db.find_one({"word": key, "text": value}):
            chatbot_db.insert_one({"word": key, "text": value, "check": check})
        return

    key = message.text if message.text else message.sticker.file_unique_id
    entries = list(chatbot_db.find({"word": key}))
    if entries:
        choice_data = random.choice(entries)
        if choice_data["check"] == "sticker":
            await message.reply_sticker(choice_data["text"])
        else:
            await message.reply_text(choice_data["text"])

# === Run Bot ===
print("✅ Chatbot is running! Join @We_Rfriends and @Devbotz")
bot.run()
