from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars as sp


app = Flask(__name__)


mongo = PyMongo(app)


@app.route('/')
def index():
    test_row = mongo.db.test.find_one()
    hemi_info=test_row['hemi_info']
    return render_template('index.html', test=test_row,hemi=hemi_info)


@app.route('/scrape')
def scrape():
    test_row = mongo.db.test
    data = sp.scrape()
    test_row.update(
        {},
        data,
        upsert=True
    )
    return redirect("http://localhost:5000/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
