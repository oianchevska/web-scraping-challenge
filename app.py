from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars
import os

app = Flask(__name__)

uri=os.environ["MONGODB_URI"]

mongo = PyMongo(app, uri=uri, retryWrites=False)


@app.route("/")
def index():
    mars_mission = mongo.db.collection.find_one()
    return render_template("index.html", info_m=mars_mission)


@app.route("/scrape")
def scrape():
    mars_data_app = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({}, mars_data_app, upsert=True)
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)


