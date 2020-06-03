import os, pickle, time
import datetime
for path in os.listdir("hist"):
    try:
        data = pickle.load(open(os.path.join("hist",path),"rb"))
        t1, settings, history, user_version = data["t1"], data["settings"], data["history"], data["user_version"]
        settings.top_p=0.9
        settings.temperature=0.85
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
    new_data={'2020-06-02': message_total}
    new_total={str(datetime.date.today()): message_total}
    print({"message_total":new_total,"message_rate":new_data,"users":users})
    pickle.dump({"message_total":new_total,"message_rate":new_data,"users":users}, open("hist/user/users.p", "wb"))
    print(os.path.join("hist",path))
except Exception as e:
    print(e)