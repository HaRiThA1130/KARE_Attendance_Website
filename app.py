
from flask import Flask, render_template, request, redirect, url_for, session, flash
import csv
import os
from datetime import date

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "kare_secure_key"

STUDENT_FILE = "students.csv"
ATT_FILE = "attendance.csv"

# Ensure CSV files exist
if not os.path.exists(STUDENT_FILE):
    with open(STUDENT_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["name","regno","email","password","dept","year"])

if not os.path.exists(ATT_FILE):
    with open(ATT_FILE, "w", newline="") as f:
        csv.writer(f).writerow(["regno","date"])


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        data = [
            request.form["name"],
            request.form["regno"],
            request.form["email"],
            request.form["password"],
            request.form["dept"],
            request.form["year"]
        ]
        with open(STUDENT_FILE, "a", newline="") as f:
            csv.writer(f).writerow(data)

        flash("Registration Successful")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        with open(STUDENT_FILE) as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row[2] == email and row[3] == password:
                    session["user"] = row[0]
                    session["regno"] = row[1]
                    return redirect(url_for("dashboard"))

        flash("Invalid Credentials")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "regno" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", name=session["user"])


@app.route("/mark")
def mark():
    if "regno" not in session:
        return redirect(url_for("login"))

    today = str(date.today())
    regno = session["regno"]

    with open(ATT_FILE) as f:
        reader = csv.reader(f)
        for row in reader:
            if row == [regno, today]:
                flash("Attendance already marked today")
                return redirect(url_for("dashboard"))

    with open(ATT_FILE, "a", newline="") as f:
        csv.writer(f).writerow([regno, today])

    flash("Attendance Marked Successfully")
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
