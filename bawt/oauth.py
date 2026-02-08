import os, requests

API = "https://discord.com/api"
CID = os.getenv("CLIENT_ID")
SECRET = os.getenv("CLIENT_SECRET")
REDIRECT = os.getenv("REDIRECT_URI")

def oauth_url():
    return f"{API}/oauth2/authorize?client_id={CID}&redirect_uri={REDIRECT}&response_type=code&scope=identify%20guilds"

def exchange(code):
    return requests.post(
        f"{API}/oauth2/token",
        data={
            "client_id": CID,
            "client_secret": SECRET,
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT
        }
    ).json()

def guilds(token):
    return requests.get(
        f"{API}/users/@me/guilds",
        headers={"Authorization": f"Bearer {token}"}
    ).json()
