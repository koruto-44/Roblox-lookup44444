from flask import Flask, request, render_template_string
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

{% if user %}
<div style="background:white; display:inline-block; padding:20px; border-radius:10px;">
    <img src="{{avatar}}" width="150"><br><br>

    <h2>{{user["name"]}}</h2>
    <p><b>Display:</b> {{user["displayName"]}}</p>
    <p><b>ID:</b> {{user["id"]}}</p>
    <p><b>Créé le:</b> {{user["created"]}}</p>

    <br>

    <a href="https://www.roblox.com/users/{{user['id']}}/profile" target="_blank">
        Voir profil Roblox
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

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/search")
def search():
    username = request.args.get("username")

    uid = get_user_id(username)
    if not uid:
        return render_template_string(HTML, user=None)

    user = get_user_info(uid)
    avatar = get_avatar(uid)

    return render_template_string(HTML, user=user, avatar=avatar)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
