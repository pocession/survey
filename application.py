import cs50
import csv
import re

from flask import Flask, jsonify, redirect, render_template, request

# Configure application
app = Flask(__name__)

# Reload templates when they are changed
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Disable caching"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
def get_index():
    return redirect("/form")


@app.route("/form", methods=["GET"])
def get_form():
    return render_template("form.html")


# Get user input
@app.route("/form", methods=["POST"])
def post_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        year = request.form['year']
        gender = request.form['gender']
        research = request.form['research']

        # Most user input can be checked on html side, here is some codes for checking if user enter a name with a correct format
        result = re.match("^[A-Z][a-z]{1,19}[\s][A-Z][a-z]{1,19}$", name)
        if result is None:
            return render_template("error.html", message="Be sure your name input follows this format: First Last (Initial letters of both names should be UPPER CASES and with a whitespace in between.)")

        # Write user input into a csv table
        fieldnames = ['name', 'email', 'year', 'gender', 'research']
        with open('survey.csv','a') as inFile:
            writer = csv.DictWriter(inFile, fieldnames=fieldnames, lineterminator='\n')
            writer.writerow({'name': name, 'email': email, 'year': year, 'gender': gender, 'research': research})
    return render_template("greeting.html", message="Thank you for your participation! (Click Sheet button to see how many people have regestered)")


@app.route("/sheet", methods=["GET"])
def get_sheet():
    with open("survey.csv", "r") as file:
        reader = csv.DictReader(file)
        fieldnames = list(reader)
    return render_template("survey.html", fieldnames=fieldnames)