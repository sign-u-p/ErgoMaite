import streamlit
from pymongo import MongoClient


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

import parameters as par

uri = streamlit.secrets["URI_MONGODB"]

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Neuen Bot im Sandkasten teilen
def insert_bot(new):
    try:
        client.ErgoMaite.Bots.insert_one(new)
    except Exception as e:
        raise Exception("The following error occurred: ", e)

def add_bot(bot):
    try:
        client.ErgoMaite.Bots.insert_one(bot)
        return True
    except Exception as e:
        raise Exception(f"The following error occurred: {feedback}", e)

def get_bot(bot_name):
    try:
        bot = client.ErgoMaite.Bots.find_one({"bot_name":bot_name})
        return bot
    except Exception as e:
        raise Exception(f"The following error occurred:", e)

# Bot anhand des System-Prompts in der db suchen und Inhalt des Documents zurückgeben
def search_bot(sys_prompt):
    try:
        bot = client.ErgoMaite.Bots.find_one({"sys_prompt":sys_prompt})
        return bot
    except Exception as e:
        raise Exception("The following error occurred: ", e)

# Alle Systemprompts auflisten (wird verwendet, um die Buttons im Sandkasten zu erstellen)
def get_all_sys_prompts():
    try:
        sys_prompts = client.ErgoMaite.Bots.distinct("sys_prompt")
        return sys_prompts
    except Exception as e:
        raise Exception("The following error occurred: ", e)

def get_choice():
    try:
        choice = []
        get = client.ErgoMaite.Bots.find({"active":True}, {"bot_name": 1})
        #choice_formated = []
        #for c in choice:
            #if c == "bot_name":
             #   choice.formated.append(choice["bot_name"])
        for result in get:
            choice.append(result["bot_name"])
        return choice
    except Exception as e:
        raise Exception("The following error occurred: ", e)

def get_fb_bot(bot_name):
    try:
        bot = client.Feedback.Bots.find_one({"bot_name":bot_name})
        return bot
    except Exception as e:
        raise Exception("The following error occurred: ", e)

def save_feedback(feedback):
    try:
        now = datetime.now()
        feedback_formated = ({"app":"ErgoMaite", "datetime":now,"conversation":None})
        feedback_formated["conversation"]=feedback
#        feedback_formated = []
#        feedback_formated = feedback_formated.append(feedback)
        client.Feedback.Messages.insert_one(feedback_formated)
        return True
    except Exception as e:
        raise Exception(f"The following error occurred: {feedback}", e)

def get_start():
    try:
        start = client.ErgoMaite.Settings.find_one({"usage":"start"})
        return start
    except Exception as e:
        raise Exception(f"The following error occurred:", e)
