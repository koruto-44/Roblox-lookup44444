from flask import Flask, request
import requests
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Roblox Lookup Pro</title>
    <style>
        body {
            font-family: Arial;
            background: #f2f2f2;
            text-align: center;
        }

        .box {
            margin-top: 70px;
        }

        input {
            width: 300px;
            padding: 12px;
            border-radius: 20px;
            border: 1px solid #ccc;
        }

        button {
            padding: 12px 18px;
            border-radius: 20px;
            border: none;
            background: #4285F4;
            color: white;
        }

        .card {
            margin-top: 20px;
            display: inline-block;
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            width: 350px;
        }

        img {
            border-radius: 10px;
        }

        .small {
            font-size: 14px;
            color: gray;
        }

        a {
            color: #4285F4;
        }
    </style>
</head>
<body>

<div class="box">
    <h1>🔎 Roblox Lookup Pro</h1>

    <form action="/search">
        <input name="username" placeholder="Pseudo Roblox">
        <button>Rechercher</button>
    </form>

    {% if data %}
    <div class="card">
        <img src="{{avatar}}" width="150"><br><br>

        <h2>{{data["name"]}}</h2>
        <p class="small">Display: {{data["displayName"]}}</p>
        <p>ID: {{data["id"]}}</p>
        <p>Créé le: {{data["created"]}}</p>

        <hr>

        <p><b>🏷 Groupes:</b> {{groups}}</p>
        <p><b>🎖 Badges:</b> {{badges}}</p>

        <hr>

        <a href="https://www.roblox.com/users/{{data['id']}}/profile" target="_blank">
            Voir profil Roblox
        </a>
    </div>
    {% endif %}
</div>

</body>
</html>
"""

def get_user_id(username):
    r = requests.post(
        "https://users.roblox.com/v1/usernames/users",
        json={"usernames": [username], "excludeBannedUsers": True}
    )
    data = r.json()
    if not data["data"]:
        return None
    return data["data"][0]["id"]

def get_user_info(uid):
    return requests.get(f"https://users.roblox.com/v1/users/{uid}").json()

def get_avatar(uid):
    r = requests.get(
        f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={uid}&size=420x420&format=Png"
    )
    return r.json()["data"][0]["imageUrl"]

def get_groups(uid):
    r = requests.get(f"https://groups.roblox.com/v2/users/{uid}/groups/roles")
    data = r.json()
    if "data" not in data:
        return "Privé / Aucun"
    return len(data["data"])

def get_badges(uid):
    r = requests.get(f"https://badges.roblox.com/v1/users/{uid}/badges?limit=10")
    data = r.json()
    if "data" not in data:
        return "0"
    return len(data["data"])

@app.route("/")
def home():
    return HTML

@app.route("/search")
def search():
    username = request.args.get("username")

    uid = get_user_id(username)
    if not uid:
        return HTML.replace("{% if data %}", "").replace("{% endif %}", "")

    info = get_user_info(uid)
    avatar = get_avatar(uid)
    groups = get_groups(uid)
    badges = get_badges(uid)

    return HTML.replace("{% if data %}", "").replace("{% endif %}", "")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
