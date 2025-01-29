from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os

app = Flask(__name__)

VOTERS_FILE = "voters.json"
VOTES_FILE = "votes.json"

# Ensure files exist
if not os.path.exists(VOTERS_FILE):
    with open(VOTERS_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(VOTES_FILE):
    with open(VOTES_FILE, "w") as f:
        json.dump({"الف": 0, "ب": 0, "پ": 0, "ت": 0}, f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        national_id = request.form["national_id"]

        with open(VOTERS_FILE, "r") as f:
            voters = json.load(f)

        if national_id in voters:
            return "⚠️ شما در انتخابات شرکت کرده‌اید!"


        voters[national_id] = {"name": name, "voted": False}

        with open(VOTERS_FILE, "w") as f:
            json.dump(voters, f)

        return redirect(url_for("vote"))

    return render_template("register.html")

@app.route("/vote", methods=["GET", "POST"])
def vote():
    if request.method == "POST":
        candidate = request.form["candidate"]

        with open(VOTES_FILE, "r") as f:
            votes = json.load(f)

        votes[candidate] = votes.get(candidate, 0) + 1

        with open(VOTES_FILE, "w") as f:
            json.dump(votes, f)

        return redirect(url_for("results"))

    return render_template("vote.html")

@app.route("/results")
def results():
    with open(VOTES_FILE, "r") as f:
        votes = json.load(f)
    return render_template("results.html", results=votes)

if __name__ == "__main__":
    app.run(debug=True)
