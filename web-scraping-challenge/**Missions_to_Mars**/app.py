from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_stuff")


@app.route("/")
def home():
    voyage_data = mongo.db.voyage_data.find_one()
    return render_template("index.html", voyage_data=voyage_data)


@app.route("/scrape")
def scrape():
    mars_mongo = mongo.db.voyage_data
     # Run the scrape function
    mars_data = scrape_mars.final_info()

    # Update the Mongo database using update and upsert=True
    mars_mongo.replace_one({}, mars_data, upsert=True)

    # In testing
    return "It worked"

if __name__ == "__main__":
    app.run(debug=True)
