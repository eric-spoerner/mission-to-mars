from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

#use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27107/mars_app"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars = mongo.db.mars.find_one()
    return render_template("index.html", mars=mars)

@app.route("/scrape")
def scrape():
    mars = mongo.db.mars
    mars_data = scraping.scrape_all()
    mars.update_one({}, {"$set":mars_data}, upsert=True) # first empty brackets = param with search criteria for data set
    return redirect('/', code=302) # what is code 302?

if __name__ == "__main__":
    app.run()