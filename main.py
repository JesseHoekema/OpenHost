from flask import Flask, render_template, request, send_from_directory, redirect, url_for, session, flash
import os
import platform
import psutil
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Zorg ervoor dat je deze aanpast voor productie
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

CREDENTIALS_FILE = "credentials.txt"

# Laden van opgeslagen gebruikersgegevens
USER_CREDENTIALS = {}


def load_credentials():
    if os.path.exists(CREDENTIALS_FILE):
        with open(CREDENTIALS_FILE, "r") as file:
            for line in file:
                username, password = line.strip().split(",")
                USER_CREDENTIALS[username] = password


def save_credentials(username, password):
    with open(CREDENTIALS_FILE, "a") as file:
        file.write(f"{username},{password}\n")


load_credentials()

# Serve index.html op de rootpagina
@app.route("/")
def serve_index():
    index_path = os.path.join(UPLOAD_FOLDER, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(UPLOAD_FOLDER, "index.html")
    else:
        return "No index.html found in uploads directory."

# Bestanden uploaden
@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part", 400
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        flash(f"File {file.filename} uploaded successfully!", "success")
        return redirect(url_for("dashboard"))
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload File</title>
    </head>
    <body>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <input type="file" name="file">
            <button type="submit">Upload</button>
        </form>
    </body>
    </html>
    '''

# Dashboardpagina met loginvereiste
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    
    # Krijg alle bestanden in de uploads map
    uploaded_files = os.listdir(UPLOAD_FOLDER)
    
    # Verwijderen van een bestand
    if request.method == "POST":
        filename_to_delete = request.form.get("file_to_delete")
        if filename_to_delete and filename_to_delete in uploaded_files:
            file_path = os.path.join(UPLOAD_FOLDER, filename_to_delete)
            os.remove(file_path)
            flash(f"File {filename_to_delete} deleted successfully!", "danger")
            return redirect(url_for("dashboard"))
    
    host_info = {
        "system_name": platform.system(),
        "node_name": platform.node(),
        "release": platform.release(),
        "version": platform.version(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "uptime": str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())).split('.')[0],
        "cpu_usage": psutil.cpu_percent(interval=1),
        "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
    }
    return render_template("dashboard.html", host_info=host_info, uploaded_files=uploaded_files)

# Setup voor eerste login
@app.route("/setup", methods=["GET", "POST"])
def setup():
    if USER_CREDENTIALS:
        return redirect(url_for("login"))  # Als de gebruiker al bestaat, ga naar login
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            return "Username and password cannot be empty!", 400
        USER_CREDENTIALS[username] = password
        save_credentials(username, password)
        return redirect(url_for("login"))
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Setup Account</title>
    </head>
    <body>
        <h1>Setup Account</h1>
        <form method="post">
            <label for="username">Set Username:</label>
            <input type="text" id="username" name="username" required><br><br>
            <label for="password">Set Password:</label>
            <input type="password" id="password" name="password" required><br><br>
            <button type="submit">Set Account</button>
        </form>
    </body>
    </html>
    '''

# Loginpagina
@app.route("/login", methods=["GET", "POST"])
def login():
    if not USER_CREDENTIALS:
        return redirect(url_for("setup"))  # Als er geen gebruiker is, ga naar setup
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username in USER_CREDENTIALS and USER_CREDENTIALS[username] == password:
            session["user"] = username
            return redirect(url_for("dashboard"))
        else:
            return "Invalid credentials. Please try again.", 401
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login</title>
    </head>
    <body>
        <h1>Login</h1>
        <form method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required><br><br>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required><br><br>
            <button type="submit">Login</button>
        </form>
    </body>
    </html>
    '''

# Logoutpagina
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

# Bestanden serveren vanuit uploads
@app.route("/<path:filename>")
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4545)  # Zorg ervoor dat Flask luistert op poort 4545