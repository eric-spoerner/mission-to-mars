from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping
# https://pyquestions.com/object-is-not-json-serializable
import json
from bson import json_util


import pymongo

app = Flask(__name__)

#use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://127.0.0.1:27107/mars_app"
mongo = PyMongo(app)

# https://stackoverflow.com/questions/34243707/pymongo-3-2-connectionfailure-not-working#59608596
# 
# def index():
#     # i still don't understand this syntax -- what is mongo.db.***mars***/
#     mars = mongo.db.mars.find_one()
#     try:
#         return mars
#     except TypeError as e:
#         print(e)        
#         return None
#     # except OperationFailure as f:
#     #     return f
#     return 'foo'

# source:
# diagnostic function for testing pymonsgo connection to mongo
@app.route("/")
def index():
    try:
        conn = pymongo.MongoClient("mongodb://localhost:27017/")
        try:
            mars_db = conn["mars_app"]
            mars_collection = mars_db.mars

            mars = mars_collection.find_one()
            # https://pyquestions.com/object-is-not-json-serializable
            print(mars)
            # json_doc = json.dumps(mars, default=json_util.default)

            return render_template("index.html", mars=mars)
        except OperationFailure as e:
            return e
    except Exception as e:
        return e


@app.route("/scrape")
def scrape():
    conn = pymongo.MongoClient("mongodb://localhost:27017/")
    mars = conn["mars_app"].mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set":mars_data}, upsert=True) # first empty brackets = param with search criteria for data set
    return redirect('/', code=302) # what is code 302?

if __name__ == "__main__":
    app.run()