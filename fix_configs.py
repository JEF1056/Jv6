import os, pickle, time
for path in os.listdir("hist"):
    try:
        t1, settings, history, user_version = pickle.load(open(os.path.join("hist",path),"rb"))
        print(settings)
        settings.top_p=0.75
        settings.temperature=0.7
        settings.model="gpt2"
        settings.model_checkpoint="run3"
        pickle.dump({"t1":t1,"settings":settings,"history":history,"user_version":1},open(os.path.join("hist",path),"wb"))
        print(os.path.join("hist",path))
    except Exception as e:
        print(e)
        print("ERR",os.path.join("hist",path))