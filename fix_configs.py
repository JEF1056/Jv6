import os, pickle, time
for path in os.listdir("hist"):
    try:
        t1, settings, history = pickle.load(open(os.path.join("hist",path),"rb"))
        pickle.dump({"t1":t1,"settings":settings,"history":history,"user_version":0},open(os.path.join("hist",path),"wb"))
        print(os.path.join("hist",path))
    except:
        print("ERR",os.path.join("hist",path))