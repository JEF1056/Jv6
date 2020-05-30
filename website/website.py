from flask import Flask, redirect, url_for, render_template
from flask_discord import DiscordOAuth2Session, requires_authorization
from waitress import serve
import json
import os

app = Flask(__name__)

with open('../config.json') as json_file:
    config = json.load(json_file)["website"]

app.secret_key = config["secret_key"]

app.config["DISCORD_CLIENT_ID"] = config["DISCORD_CLIENT_ID"]    # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = config["DISCORD_CLIENT_SECRET"]    # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = config["DISCORD_REDIRECT_URI"]     # Redirect URI.

discord = DiscordOAuth2Session(app)

@app.route("/login/")
def login():
    return discord.create_session(scope=["identify", "guilds"])

@app.route("/")
def root():
    return render_template('index.html')
	
@app.route("/auth/")
def callback():
    discord.callback()
    return redirect(url_for(".data"))
	
@app.route("/data/")
@requires_authorization

def data():
    user = discord.fetch_user()
    guilds=discord.fetch_guilds()
    guilds_data=[]
    for guild in guilds:
        if str(guild.id)+".p" in os.listdir("../hist"):
            guilds_data.append(guild)
    print(guilds_data)
    return render_template("data.html", avatar_url=str(user.avatar_url)+"?size=300", name=user.name, guilds=guilds_data)


if __name__ == "__main__":
    #app.run(ssl_context='adhoc')
    serve(app, host=config["host"], port=config["port"], url_scheme='https')