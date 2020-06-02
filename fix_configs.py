import os, pickle, time
import datetime
for path in os.listdir("hist"):
    try:
        data = pickle.load(open(os.path.join("hist",path),"rb"))
        t1, settings, history, user_version = data["t1"], data["settings"], data["history"], data["user_version"]
        settings.top_p=0.75
        settings.temperature=0.7
        settings.model="gpt2"
        settings.model_checkpoint="run3"
        pickle.dump({"t1":t1,"settings":settings,"history":history,"user_version":1},open(os.path.join("hist",path),"wb"))
        print(os.path.join("hist",path))
    except Exception as e:
        print(e)
        print("ERR",os.path.join("hist",path))
        
    try:
        data = pickle.load(open("hist/user/users.p", "rb"))
        message_total, message_rate, users = data["message_total"],data["message_rate"], data["users"]
        new_data={}
        for message in message_rate:
            try:
                new_data[str(datetime.datetime.fromtimestamp(round(message["timestamp"])))]+=message["message_count"]
            except:
                new_data[str(datetime.datetime.fromtimestamp(round(message["timestamp"])))]=message["message_count"]
        print({"message_total":message_total,"message_rate":new_data,"users":users})
        pickle.dump({"message_total":message_total,"message_rate":new_data,"users":users}, open("hist/user/users.p", "wb"))
        print(os.path.join("hist",path))
    except Exception as e:
        print(e)