
from flask import Flask, render_template, request, redirect, url_for, session, flash
import csv
import os
from datetime import date

app = Flask(__name__)
app.secret_key = "kare_secret"

STUDENT_FILE = "students.csv"
ATTENDANCE_FILE = "attendance.csv"

# Ensure files exist
if not os.path.exists(STUDENT_FILE):
    with open(STUDENT_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "regno", "email", "password", "department", "year"])

if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["regno", "date"])


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        data = [
            request.form["name"],
            request.form["regno"],
            request.form["email"],
            request.form["password"],
            request.form["department"],
            request.form["year"]
        ]

        with open(STUDENT_FILE, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(data)

        flash("Registration Successful!")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        with open(STUDENT_FILE, "r") as f:
            reader = csv.reader(f)
            next(reader)
            for row in reader:
                if row[2] == email and row[3] == password:
                    session["regno"] = row[1]
                    session["name"] = row[0]
                    return redirect(url_for("dashboard"))

        flash("Invalid Login")

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "regno" not in session:
        return redirect(url_for("login"))

    return render_template("dashboard.html", name=session["name"])


@app.route("/mark_attendance")
def mark_attendance():
    if "regno" not in session:
        return redirect(url_for("login"))

    today = str(date.today())
    regno = session["regno"]

    with open(ATTENDANCE_FILE, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row == [regno, today]:
                flash("Attendance already marked today!")
                return redirect(url_for("dashboard"))

    with open(ATTENDANCE_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([regno, today])

    flash("Attendance Marked Successfully!")
    return redirect(url_for("dashboard"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
