from flask import Flask
from pymongo import MongoClient
from bson.json_util import dumps
import pyarabic.araby as araby
from dotenv import dotenv_values


# Env variables (passwords)
config = dotenv_values(".env")

#Flask and MongoDB setup
app = Flask(__name__)
client = MongoClient(config["MONGO_URI"])
db = client.quranic_arabic
dictionary = db.dictionary


@app.route("/", methods=["GET"])
def index():
    return "search_result"


@app.route("/arabic/<kalam>", methods=["GET"])
def find_arabic_word(kalam):
    after_filter = araby.strip_diacritics(kalam)
    search_result = dictionary.find({"arabic_sg": after_filter})
    return dumps(search_result)


@app.route("/spanish/<word>", methods=["GET"])
def find_spanish_word(word):
    search_result = dictionary.find({"spanish": word})
    return dumps(search_result)


if __name__ == "__main__":
    app.run()
