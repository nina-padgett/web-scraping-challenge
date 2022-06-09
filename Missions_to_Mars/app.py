from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# app.config["MONGO_URI"] = "mongodb://localhost:27017/phone_app"
# mongo = PyMongo(app)

# Or set inline
mongo = pymongo(app, uri="mongodb://localhost:27017")

# create a listings collection, lazy loading
mars_collection = mongo.db.mars

@app.route("/")
def index():
    # find one document from our mongo db and return it.
    mars_results = mars_collection.find_one()
    # pass that listing to render_template
    return render_template("index.html", mars=mars_results)

# set our path to /scrape
@app.route("/scrape")
def scraper():
    # call the scrape function in our scrape_phone file. This will scrape and save to mongo.
    mars_data = scrape_mars.scrape()
    # update our listings with the data that is being scraped or create&insert if collection doesn't exist
    mars_collection.update_one({}, {"$set": mars_data}, upsert=True)
    # return a message to our page so we know it was successful.
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)