from flask import Flask, render_template, redirect

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
from flask_pymongo import PyMongo

from flask import jsonify

# Import Scrape.py
import scrape

# Create an instance of our Flask app.
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/jobs_data"


# Use flask_pymongo to set up mongo connection

mongo = PyMongo(app)

@app.route("/")
def index():
    jobs = mongo.db.collection.find_one()
    return render_template("index.html")

@app.route("/scrape")
def scrape1():
    #jobss = mongo.db.jobs 
    jobs_data = scrape.scrape()
    mongo.db.collection.update({}, jobs_data, upsert=True)
    return jsonify(jobs_data)

if __name__ == "__main__":
    app.run(debug=True)