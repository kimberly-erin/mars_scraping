# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app)

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():
    
    # Find data
    planet_mars = mongo.db.mars_collection.find()
    
    # return template and data
    return render_template("index.html", planet_mars=planet_mars)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():
    mongo.db.mars_collection.drop()
    # Run scraped functions
    nasa = scrape_mars.scrape_nasa()
    jpl = scrape_mars.scrape_jpl()
    twitter = scrape_mars.scrape_twitter()
    facts = scrape_mars.scrape_facts()
    hemis = scrape_mars.hemi()

    # Store results into a dictionary
    mars = {
        "NASA_Headline": nasa,
        "Featured_Pic": jpl['featured_pic_url'],
        "Mars_Weather": twitter['mars_weather'],
        "Mars_Facts": facts['mars_html_table'],
        "Hemispheres": hemis['hemi']
    }

    # Insert forecast into database
    mongo.db.mars_collection.insert_one(mars)

    # Redirect back to home page
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
