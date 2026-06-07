from flask import Flask, request
import requests
import os

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Roblox Lookup</title>
</head>
<body style="font-family: Arial; text-align:center; background:#f2f2f2;">

<h1>🔎 Roblox Lookup</h1>

<form action="/search">
    <input name="username" placeholder="Pseudo Roblox">
    <button>Rechercher</button>
</form>

<br>

{% if data %}
<div style="background:white; display:inline-block; padding:20px; border-radius:10px; width:320px;">
    <img src="{{avatar}}" width="150"><br><br>

    <h2>{{data["name"]}}</h2>

    <p><b>Display Name:</b> {{data["displayName"]}}</p>
    <p><b>ID:</b> {{data["id"]}}</p>
    <p><b>Créé le:</b> {{data["created"]}}</p>

    <p><b>Statut:</b> {{status}}</p>
    <p><b>Friends (approx):</b> {{friends}}</p>
    <p><b>Followers:</b> {{followers}}</p>
    <p><b>Following:</b> {{following}}</p>

    <br>

    <a href="https://www.roblox.com/users/{{data['id']}}/profile" target="_blank">
        🔗 Voir profil Roblox
    </a>
</div>
{% endif %}

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

def get_social(uid):
    followers = requests.get(f"https://friends.roblox.com/v1/users/{uid}/followers/count").json().get("count", "N/A")
    following = requests.get(f"https://friends.roblox.com/v1/users/{uid}/followings/count").json().get("count", "N/A")

    return followers, following

def get_status(uid):
    r = requests.get(f"https://users.roblox.com/v1/users/{uid}")
    data = r.json()
    return data.get("description", "Aucun statut")

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
    followers, following = get_social(uid)
    status = get_status(uid)

    return HTML.replace("{% if data %}", "").replace("{% endif %}", "")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
