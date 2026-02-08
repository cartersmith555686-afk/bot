from flask import Flask, redirect, request, session
import sqlite3
from oauth import oauth_url, exchange, guilds

app = Flask(__name__)
app.secret_key = "free-dashboard"

def db():
    return sqlite3.connect("data.db")

@app.route("/")
def home():
    if "token" not in session:
        return redirect("/login")
    gs = guilds(session["token"])
    return f"""
    <script src="https://cdn.tailwindcss.com"></script>
    <div class="bg-gray-900 text-white p-6">
    <h1 class="text-3xl">Dashboard</h1>
    {''.join(f"<a class='block text-blue-400' href='/guild/{g['id']}'>{g['name']}</a>" for g in gs)}
    </div>
    """

@app.route("/guild/<int:gid>")
def guild(gid):
    con = db()
    cur = con.cursor()
    cur.execute("SELECT * FROM audit_logs WHERE guild_id=? ORDER BY id DESC LIMIT 10", (gid,))
    logs = cur.fetchall()
    return f"""
    <script src="https://cdn.tailwindcss.com"></script>
    <div class="bg-gray-900 text-white p-6">
    <h2 class="text-2xl">Audit Logs</h2>
    {''.join(f"<p>{l[6]} | {l[2]} | {l[5]}</p>" for l in logs)}
    </div>
    """

@app.route("/login")
def login():
    return redirect(oauth_url())

@app.route("/callback")
def callback():
    code = request.args.get("code")
    data = exchange(code)
    session["token"] = data["access_token"]
    return redirect("/")
