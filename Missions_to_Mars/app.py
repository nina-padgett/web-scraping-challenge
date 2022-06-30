from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_db"
mongo = PyMongo(app)

# Create route that renders index.html template
@app.route("/")
def index():
    mars = mongo.db.mars_collection.find_one()
    return render_template("index.html", mars=mars)


# set our path to /scrape
@app.route("/scrape")
def scraper():
    # Create a mars database
    mars = mongo.db.mars_collection
    # Call the scrape function in our scrape_mars file. This will scrape and save to mongo.
    mars_database_data = scrape_mars.scrape_all()
    # Update mars_database with the data that is being scraped.
    mars.update_one({}, {"$set": mars_database_data}, upsert=True)

    # return a message to our page so we know it was successful.
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)