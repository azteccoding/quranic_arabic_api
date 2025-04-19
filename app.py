from flask import Flask
from pymongo import MongoClient
import pyarabic.araby as araby
from dotenv import dotenv_values

# Env variables (passwords)
config = dotenv_values(".env")

# Flask and MongoDB setup
app = Flask(__name__)
client = MongoClient(config["MONGO_URI_LOCAL"])
db = client.quranic_arabic
dictionary = db.dictionary


@app.route("/", methods=["GET"])
def index():
    return "search_result"


@app.route("/test/<test>", methods=["GET"])
def testing_alternatives(test):
    after_filter = araby.strip_diacritics(test)
    d = dictionary.find_one({"spanish": after_filter})
    manual_json = {
        "arabic_sg": d["arabic_sg"],
        "spanish": d["spanish"],
        "array": [1, 2, 3, 4],
        "object": {
            "love": True
        }
    }
    return manual_json


@app.route("/arabic/<kalam>", methods=["GET"])
def find_arabic_word(kalam):
    after_filter = araby.strip_diacritics(kalam)
    d = dictionary.find_one({"arabic_sg": after_filter})
    json_response = f"""
    {{
        "spanish": "{d["spanish"]}",
        "english": "{d['english']}",
        "arabic_sg": "{d['arabic_sg']}",
        "arabic_pl": "{d['arabic_pl']}",
        "translit_sg": "{d['translit_sg']}",
        "translit_pl": "{d['translit_pl']}",
        "quranic_appear": {{
            "appearance": "{d['quranic_appear']['appearance']}",
            "sentence": "{d['quranic_appear']['sentence']}",
            "translation": "{d['quranic_appear']['translation']}"
        }},
        "root": "[{d['root']}]",
        "hadith_appear": {{
            "collection": "{d['hadith_appear']['collection']}",
            "collection_name": "{d['hadith_appear']['collection_name']}",
            "number": "{d['hadith_appear']['number']}",
            "sentence": "{d['hadith_appear']['sentence']}",
            "translation": "{d['hadith_appear']['translation']}"
        }},
        "phrase": {{
            "arabic": "{d['phrase']['arabic']}",
            "meaning": "{d['phrase']['meaning']}",
            "translit": "{d['phrase']['translit']}"
        }},
        "dipote": "{d['dipote']}",
        "foreign": "{d['foreign']}",
        "pl_diptote": "{d['pl_diptote']}",
        "synonim": "{d['synonim']}",
        "antonym": "{d['antonym']}",
        "noun": "{d['noun']}",
        "verb": "{d['verb']}",
        "form": "{d['form']}",
        "masculine": "{d['masculine']}"
    }}
"""
    return json_response


@app.route("/spanish/<word>", methods=["GET"])
def find_spanish_word(word):
    d = dictionary.find_one({"spanish": word})
    json_response = f"""
{{
    "spanish": "{d["spanish"]}",
    "arabic_sg": "{d['arabic_sg']}",
    "arabic_pl": "{d['arabic_pl']}",
    "translit_sg": "{d['translit_sg']}",
    "translit_pl": "{d['translit_pl']}",
    "dipote": "{d['dipote']}",
    "foreign": "{d['foreign']}",
    "pl_diptote": "{d['pl_diptote']}",
    "synonim": "{d['synonim']}",
    "antonym": "{d['antonym']}",
    "noun": "{d['noun']}",
    "verb": "{d['verb']}",
    "form": "{d['form']}",
    "masculine": "{d['masculine']}"
}}
"""
    return json_response


if __name__ == "__main__":
    app.run()
