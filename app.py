from flask import Flask, request
import requests
import os

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Roblox Lookup</h1>
    <form action="/search">
        <input name="username" placeholder="Pseudo Roblox">
        <button type="submit">Rechercher</button>
    </form>
    """

@app.route("/search")
def search():
    username = request.args.get("username")

    # 1. Trouver l'ID Roblox
    r = requests.post(
        "https://users.roblox.com/v1/usernames/users",
        json={"usernames": [username], "excludeBannedUsers": True}
    )

    data = r.json()

    if not data["data"]:
        return "Utilisateur introuvable"

    user_id = data["data"][0]["id"]

    # 2. Infos utilisateur
    info = requests.get(f"https://users.roblox.com/v1/users/{user_id}").json()

    # 3. Avatar
    avatar = requests.get(
        f"https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=420x420&format=Png"
    ).json()["data"][0]["imageUrl"]

    return f"""
    <h2>{info['name']}</h2>
    <p>ID: {info['id']}</p>
    <p>Display Name: {info['displayName']}</p>
    <img src="{avatar}">
    <br><br>
    <a href="/">Retour</a>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
