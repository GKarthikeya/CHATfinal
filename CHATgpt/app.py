from flask import Flask, render_template, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from tabulate import tabulate
import time
import re
import os

app = Flask(__name__)

COLLEGE_LOGIN_URL = "https://samvidha.iare.ac.in/"
ATTENDANCE_URL = "https://samvidha.iare.ac.in/home?action=course_content"

def calculate_attendance_percentage(rows):
    result = {"subjects": {}, "overall": {"present": 0, "absent": 0, "percentage": 0.0, "success": False}}
    current_course = None
    total_present = 0
    total_absent = 0
    for row in rows:
        text = row.text.strip().upper()
        if not text or text.startswith("S.NO") or "TOPICS COVERED" in text:
            continue
        course_match = re.match(r"^(A[A-Z]+\d+)\s*[-:\s]+\s*(.+)$", text)
        if course_match:
            current_course = course_match.group(1)
            course_name = course_match.group(2).strip()
            result["subjects"][current_course] = {
                "name": course_name, "present": 0, "absent": 0, "percentage": 0.0
            }
            continue
        if current_course:
            present_count = text.count("PRESENT")
            absent_count = text.count("ABSENT")
            result["subjects"][current_course]["present"] += present_count
            result["subjects"][current_course]["absent"] += absent_count
            total_present += present_count
            total_absent += absent_count
    for sub in result["subjects"].values():
        total = sub["present"] + sub["absent"]
        if total > 0:
            sub["percentage"] = round((sub["present"] / total) * 100, 2)
    overall_total = total_present + total_absent
    if overall_total > 0:
        result["overall"] = {
            "present": total_present,
            "absent": total_absent,
            "percentage": round((total_present / overall_total) * 100, 2),
            "success": True
        }
    return result

def get_attendance_data(username, password):
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    import os, time
    from selenium.webdriver.common.by import By

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    chrome_bin = os.environ.get("GOOGLE_CHROME_BIN", "/usr/bin/chromium")
    if not os.path.exists(chrome_bin):
        raise RuntimeError("Chrome binary not found at GOOGLE_CHROME_BIN or /usr/bin/chromium")
    options.binary_location = chrome_bin

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # login and scraping logic
        ...
    finally:
        driver.quit()


@app.route("/", methods=["GET"])
def login_page():
    return render_template("login.html")

@app.route("/attendance", methods=["POST"])
def show_attendance():
    username = request.form["username"]
    password = request.form["password"]
    try:
        data = get_attendance_data(username, password)
    except Exception as e:
        return f"<h3>Error: {str(e)}</h3><p>Check your credentials or Chrome setup.</p>"
    subjects = data["subjects"]
    table_data = []
    for i, (code, sub) in enumerate(subjects.items(), start=1):
        table_data.append([i, code, sub["name"], sub["present"], sub["absent"], f"{sub['percentage']}%"])
    table_html = tabulate(table_data, headers=["S.No", "Course Code", "Course Name", "Present", "Absent", "Percentage"], tablefmt="html")
    return render_template("attendance.html", table_html=table_html, overall=data["overall"])

@app.route("/ping", methods=["GET"])
def ping():
    return "pong", 200

if __name__ == "__main__":
    app.run(debug=True)
