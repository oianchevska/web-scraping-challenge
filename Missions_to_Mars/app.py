from flask import Flask,render_template,redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


@app.route("/")
def home():
    mars_mission = mongo.db.collection.find_one()
    return render_template("index.html", info_m=mars_mission)



@app.route("/scrape")
def scrape():
    mars_data_app = scrape_mars.scrape()
    # Update the Mongo database using update and upsert=True
    mongo.db.collection.update({},mars_data_app, upsert=True)
    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)