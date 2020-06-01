from flask import Flask, redirect, url_for, render_template, request
from flask_discord import DiscordOAuth2Session, requires_authorization
from waitress import serve
import json, dbl, discord
import pickle
import os

app = Flask(__name__)

with open('../config.json') as json_file:
    config_0=json.load(json_file)
    config = config_0["website"]    

app.secret_key = config["secret_key"]
global dbli
client = discord.Client()
dbli=dbl.DBLClient(client, config_0["dbltoken"])

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

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
    global dbli
    if request.method == 'POST':
        try:
            user_status= dbli.get_user_vote(user_id=message.author.id)
        except:
            user_status=False
        inp = request.json
        print(inp)
        print(type(inp))
        if int(inp["guild_id"]) != 0:
            for key, value in pickle.load(open("hist/"+str(inp["guild_id"])+".p", "rb")).items():
                globals()[str(key)]=value
            alt_settings=vars(settings)
            server=["model", "model_checkpoint", "device"]
            client_side=["temperature","top_k","top_p"]
            privledged=["no_sample","seed", "auto_seed", "max_history", "max_length"]
            limiters={"temperature":{"max": 1, "type":float}, "top_k":{"max": float("inf"), "type":int}, "top_p":{"max": 1, "type":float},
            "no_sample":{"type":str2bool}, "seed":{"max": float("inf"), "type":int}, "auto_seed":{"type":str2bool}, 
            "max_history":{"max": 10, "type":int}, "max_length":{"max": 20, "type":int}}
            if inp["Setting"] in server:
                return {"state":False, "message":"<code>"+str(inp["Setting"])+"</code> is a server-side setting, and cannot be changed."}
            elif inp["Setting"] in privledged and user_status==False:
                return {"state":False, "message":"<code>"+str(inp["Setting"])+"</code> is a supporter-only setting. <a href=https://top.gg/bot/410253782828449802/vote>vote for Jade on top.gg</a>"}
            elif (inp["Setting"] in client_side) or inp["Setting"] in privledged and user_status==True:
                ch=limiters[inp["Setting"]]["type"](inp["Value"])
                if limiters[inp["Setting"]]["type"] == float or limiters[inp["Setting"]]["type"] == int:
                    if limiters[inp["Setting"]]["max"] >= ch and ch >= 0:
                        return {"state":True, "message":"<code>"+str(inp["Setting"])+"</code> changed from <code>"+str(alt_settings[inp["Setting"]])+"</code> to <code>"+str(inp["Value"])+"</code>"}
                        alt_settings[inp["Setting"]]=ch
                    else:
                        return {"state":True, "message":str(inp["Setting"])+" could not be changed from <code>"+str(alt_settings[inp["Setting"]])+"</code> to <code>"+str(inp["Value"])+"</code> becasue it is <code><= 0</code> or <code>>= "+str(limiters[inp["Setting"]]["max"])+"</code>"}
                else:
                    return {"state":True, "message":"<code>"+str(inp["Setting"])+"<code> changed from <code>"+str(alt_settings[inp["Setting"]])+"<code> to <code>"+str(ch)+"<code>"}
                    alt_settings[inp["Setting"]]=ch
            else:
                return {"state":True, "message":"<code>"+str(inp["Setting"])+"<code> is not a valid setting."}
            pickle.dump({"t1":t1, "settings":settings,"history":history, "user_version":user_version}, open("hist/"+inp["guild_id"]+".p", "wb"))
        else:
            return {"state":False, "message":"No Guild Selected!"}
	
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