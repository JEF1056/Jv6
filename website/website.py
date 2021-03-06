from flask import Flask, redirect, url_for, render_template, request
from flask_discord import DiscordOAuth2Session, requires_authorization
from waitress import serve
import json, dbl, discord
import pickle, random
import os
import plotly.express as px
import datetime

app = Flask(__name__)

with open('../config.json') as json_file:
    config_0=json.load(json_file)
    config = config_0["website"]    

app.secret_key = config["secret_key"]
global dbli, cached_history
client = discord.Client()
dbli=dbl.DBLClient(client, config_0["dbltoken"])
cached_history=pickle.load(open("../hist/user/users.p", "rb"))["message_rate"]

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise TypeError('Boolean value expected.')

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

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    # note that we set the 500 status explicitly
    return render_template('500.html'), 500

@app.route("/about/")
def about():
    return render_template('about.html')

@app.route("/submit/", methods=['POST'])
@requires_authorization
def submit():
    global dbli
    if request.method == 'POST':
        inp = request.json
        print(inp)
        try:
            user_status= dbli.get_user_vote(user_id=int(inp["user_id"]))
        except Exception as e:
            print(e)
            user_status=False
        server=["model", "model_checkpoint", "device"]
        client_side=["temperature","top_k","top_p"]
        privledged=["no_sample","seed", "auto_seed", "max_history", "max_length"]
        limiters={"temperature":{"max": 1, "type":float}, "top_k":{"max": float("inf"), "type":int}, "top_p":{"max": 1, "type":float},
        "no_sample":{"type":str2bool}, "seed":{"max": float("inf"), "type":int}, "auto_seed":{"type":str2bool}, 
        "max_history":{"max": 10, "type":int}, "max_length":{"max": 20, "type":int}}
        if int(inp["guild_id"]) != 0 and str(inp["guild_id"])+".p" in os.listdir("../hist"):
            if (inp["value"] == '' or inp["setting"] not in limiters) and inp["setting"] != "reset":
                return {"state":False, "message":"Cannot Input Null Value!!"}
            elif inp["setting"]=="reset":
                for key, value in pickle.load(open("../hist/"+str(inp["guild_id"])+".p", "rb")).items():
                    globals()[str(key)]=value
                alt_settings=vars(settings)
                alt_settings["temperature"], alt_settings["top_p"], alt_settings["top_k"], alt_settings["seed"]=0.85, 0.9, 40, random.randint(0,9999999999)
                alt_settings["auto_seed"], alt_settings["max_history"], alt_settings["max_length"], alt_settings["no_sample"]=True, 4, 10, False
                pickle.dump({"t1":t1, "settings":settings,"history":[], "user_version":user_version}, open("../hist/"+inp["guild_id"]+".p", "wb"))
                return {"state":False, "message":"Reset Save (refresh the page)"}
            else:
                for key, value in pickle.load(open("../hist/"+str(inp["guild_id"])+".p", "rb")).items():
                    globals()[str(key)]=value
                alt_settings=vars(settings)
                if inp["setting"] in server:
                    return {"state":False, "message":""+str(inp["setting"])+" is a server-side setting, and cannot be changed."}
                elif inp["setting"] in privledged and user_status==False:
                    return {"state":False, "message":""+str(inp["setting"])+" is a supporter-only setting. <a href=https://top.gg/bot/410253782828449802/vote>vote for Jade on top.gg</a>"}
                elif (inp["setting"] in client_side) or (inp["setting"] in privledged and user_status==True):
                    ch=limiters[inp["setting"]]["type"](inp["value"])
                    if limiters[inp["setting"]]["type"] == float or limiters[inp["setting"]]["type"] == int:
                        if limiters[inp["setting"]]["max"] >= ch and ch >= 0:
                            og=alt_settings[inp["setting"]]
                            alt_settings[inp["setting"]]=ch
                            pickle.dump({"t1":t1, "settings":settings,"history":history, "user_version":user_version}, open("../hist/"+inp["guild_id"]+".p", "wb"))
                            return {"state":True, "message":""+str(inp["setting"])+" changed from "+str(og)+" to "+str(inp["value"])+""}
                        else:
                            return {"state":False, "message":str(inp["setting"])+" could not be changed from "+str(alt_settings[inp["setting"]])+" to "+str(inp["value"])+" becasue it is <= 0 or >= "+str(limiters[inp["setting"]]["max"])+""}
                    else:
                        og=alt_settings[inp["setting"]]
                        alt_settings[inp["setting"]]=ch
                        pickle.dump({"t1":t1, "settings":settings,"history":history, "user_version":user_version}, open("../hist/"+inp["guild_id"]+".p", "wb"))
                        return {"state":True, "message":""+str(inp["setting"])+" changed from "+str(og)+" to "+str(ch)+""}
                else:
                    return {"state":False, "message":""+str(inp["setting"])+" is not a valid setting."}
        else:
            return {"state":False, "message":"No Guild Selected!"}
	
@app.route("/logout/")
@requires_authorization
def logout():
    discord.revoke()
    return redirect(url_for(".root"))
 
@app.route("/data/")
@requires_authorization

def data():
    global cached_history
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
    udata=pickle.load(open("../hist/user/users.p", "rb"))
    cached_history=udata["message_rate"]
    cached_total=udata["message_total"]
    x,y,z=[],[],[]
    for cache_data in cached_history:
        x.append(cache_data)
        y.append(cached_history[cache_data])
        z.append(cached_total[cache_data])
    try:
        return render_template("data.html", avatar_url=str(user.avatar_url)+"?size=512", totalmessages=udata["message_total"][str(datetime.date.today())],
                               todaymessages=udata["message_rate"][str(datetime.date.today())], u_profile=udata["users"][user.id], graph_x=x, graph_y=y, graph_z=z, user=user, guilds=guilds_data, num_guilds=len(guilds_data), guild_settings=guild_settings)
    except:
        return render_template("data.html", avatar_url="/static/images/fallbackpfp.png", totalmessages=udata["message_total"][str(datetime.date.today())],
                                todaymessages=udata["message_rate"][str(datetime.date.today())], u_profile=udata["users"][user.id], graph_x=x, graph_y=y, graph_z=z, user=user, guilds=guilds_data, num_guilds=len(guilds_data), guild_settings=guild_settings)
        
if __name__ == "__main__":
  #app.run(ssl_context='adhoc')
  serve(app, host=config["host"], port=config["port"], url_scheme='https')