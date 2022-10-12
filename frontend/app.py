import json

from flask import Flask, render_template, request
from dotenv import load_dotenv
from model import (get_employers)

load_dotenv("../.env")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    request_data = dict(request.form)
    query = ""
    if request_data and "data" in request_data:
        param = json.loads(request_data.get("data"))
        query = param.get("q", "")

    json_data = get_employers(query)

    return render_template("index.html", employers_data=json_data)


if __name__ == "__main__":
    app.run(debug=True, port=5000)