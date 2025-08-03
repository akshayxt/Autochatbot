# === Imports ===
from pyrogram import Client, filters  # Pyrogram for Telegram API interaction
from pyrogram.types import Message  # Telegram message object
from pymongo import MongoClient  # MongoDB client
from urllib.parse import quote_plus  # For safe username/password encoding in Mongo URI
import random  # For random selection of chatbot responses
from pyrogram.enums import ChatMembersFilter
from urllib.parse import quote_plus

# Telegram API credentials
API_ID = 24509589
API_HASH = "717cf21d94c4934bcbe1eaa1ad86ae75"

# Your Pyrogram String Session
STRING_SESSION = "BQF1_JUAljjwnBI8HgK2Gsou-C0VWnRux5-II61A6aezFvV9yddrZJRdEuevVvDv-t6So_UID2dkdWNnaUN_8CST6wo73ZpwySiJ2eoA2GqMLWsH-Qkiyl3frcxtaDO1ihWNOABCq5PoWwAKnRdHFKECy_-xGCPTaN_v3M8J7spK7mIdlxn7oW43OKYtphLyXbWe7pe2rUbduSeqgNfZW2NdSWfgljgCqFflAJilBnzHbbS5kGdkbsuQqbS1ABlYxbWuujAnPwC4P_6hHmgfzXGI1mFKPpCbt67G610_S_RWoqz33FOTKIsAEqiGQc-uI5tSvwn0MlBOphN23Ig_jITFqE1-MQAAAAHd44U9AA"

# MongoDB credentials
MONGO_USERNAME = quote_plus("Autochat")
MONGO_PASSWORD = quote_plus("Raxx@123")

# MongoDB Connection URI
MONGO_URL = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@cluster0.unruazx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

