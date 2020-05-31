from flask import Flask, redirect, url_for, render_template, request
from flask_discord import DiscordOAuth2Session, requires_authorization
from waitress import serve
import json
import pickle
import os

app = Flask(__name__)

with open('../config.json') as json_file:
  config = json.load(json_file)["website"]

app.secret_key = config["secret_key"]

app.config["DISCORD_CLIENT_ID"] = config["DISCORD_CLIENT_ID"]  # Discord client ID.
app.config["DISCORD_CLIENT_SECRET"] = config["DISCORD_CLIENT_SECRET"]  # Discord client secret.
app.config["DISCORD_REDIRECT_URI"] = config["DISCORD_REDIRECT_URI"]   # Redirect URI.

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

@app.route("/submit/", methods=['POST'])
@requires_authorization
def submit():
    if request.method == 'POST':
        print(request)
        print(request.fomr)
        inp = request.form['Setting']
        print(inp)
        return "hi"
	
@app.route("/data/")
@requires_authorization

def data():
    user = discord.fetch_user()
    guilds=discord.fetch_guilds()
    guilds_data=[]
    guild_settings={}
    for guild in guilds:
        if str(guild.id)+".p" in os.listdir("../hist"):
            guilds_data.append(guild)
            guild_settings[int(guild.id)]=(pickle.load(open("../hist/"+str(guild.id)+".p", "rb")))
            guild_settings[int(guild.id)]["settings"]=vars(guild_settings[int(guild.id)]["settings"])
    guild_settings=json.dumps(guild_settings)
    
    return render_template("data.html", avatar_url=str(user.avatar_url)+"?size=512", name=user.name, guilds=guilds_data, guild_settings=guild_settings)


if __name__ == "__main__":
  #app.run(ssl_context='adhoc')
  serve(app, host=config["host"], port=config["port"], url_scheme='https')