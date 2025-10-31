import streamlit
from pymongo import MongoClient

#ToDo: Wie schließe ich Verbindungen, ohne, dass es beim nächsten verbinden einen Fehler gibt?!


from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime

import parameters as par

uri = streamlit.secrets["URI_MONGODB"]

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Neuen Bot im Sandkasten teilen
def insert_bot_sandkasten(bot):
    try:
        bot_name = bot["bot_name"]
        test_existance = client.ErgoMaite.Sandkasten.find_one({"bot_name": bot_name})
        if test_existance == None:
            client.ErgoMaite.Sandkasten.insert_one(bot)
            return True
        else:
            return False
    except Exception as e:
        raise Exception("The following error occurred: ", e)

def add_bot(bot):
    try:
        client.ErgoMaite.Bots.insert_one(bot)
        return True
    except Exception as e:
        raise Exception(f"The following error occurred:", e)

def get_bot(bot_name):
    try:
        bot = client.ErgoMaite.Bots.find_one({"bot_name":bot_name})
        return bot
    except Exception as e:
        raise Exception(f"The following error occurred:", e)

def get_bot_spielplatz(bot_name):
    try:
        bot = client.ErgoMaite.Sandkasten.find_one({"bot_name":bot_name})
        return bot
    except Exception as e:
        raise Exception(f"The following error occurred:", e)

# Bot anhand des System-Prompts in der db suchen und Inhalt des Documents zurückgeben
def search_bot(bot_name):
    try:
        bot = client.ErgoMaite.Sandkasten.find_one({"bot_name":bot_name})
        return bot
    except Exception as e:
        raise Exception("The following error occurred: ", e)

# Alle Systemprompts auflisten (wird verwendet, um die Buttons im Sandkasten zu erstellen)
def get_all_bot_names():
    try:
        bot_names = client.ErgoMaite.Sandkasten.distinct("bot_name")
        return bot_names
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


def add_image(image):
    try:
        image_url = image["image_url"]
        test_existance = client.ErgoMaite.Images.find_one({"image_url": image_url})
        if test_existance == None:
            client.ErgoMaite.Images.insert_one(image)
            return True
        else:
            return False
    except Exception as e:
        raise Exception("The following error occurred: ", e)

def search_image(image_url):
    try:
        image = client.ErgoMaite.Images.find_one({"image_url":image_url})
        return image
    except Exception as e:
        raise Exception("The following error occurred: ", e)

def get_all_images():
    try:
        image_list = client.ErgoMaite.Images.distinct("image_url")
        return image_list
    except Exception as e:
        raise Exception("The following error occurred: ", e)