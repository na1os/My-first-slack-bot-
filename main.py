import json
import os
from slack_bolt import App
app= App(token=" ")
file = "data.json"

if os.path.exists(file) and os.path.getsize(file) > 0:
    with open(file, "r") as f:
        data = json.load(f)
else:
    data={"users": {}}
    with open(file, "w") as f:
        json.dump(data, f)

def save():
    f=open(file, "w")
    json.dump(data,f )
    f.close()

def get_user(uid):
    if uid not in data["users"]:
        data["users"][uid]={"tasks":[]}
    return data["users"][uid]

@app.message("add ")
def add(message, say):
    uid=message["user"]
    text=message["text"].replace("add ","")
    user=get_user(uid)
    user["tasks"].append({"text": text, "done": False})
    save()
    say("task added")

@app.message("list")
def list_tasks(message, say):
    uid=message["user"]
    user=get_user(uid)

    if len(user["tasks"])==0:
        say("Nothing to warry about")
        return
    msg=""
    i=0
    for t in user["tasks"]:
        msg += str(i) + " " + t["text"] + "\n"
        i+=1
        say(msg)

@app.message("done ")
def done(message, say):
    uid=message["user"]
    user=get_user(uid)

    try:
        i = int(message["text"].split(" ")[1])
        user["tasks"][i]["done"]= True
        save()
        say("ok, done")
    except:
        say("error")

@app.message("delete ")
def delete(message, say):
    uid=message["user"]
    user=get_user(uid)

    try:
        i=int(message["text"].split(" ")[1])
        user["tasks"].pop(i)
        save()
        say("deleted")
    except:
        say("error")

@app.message("stats")
def stats(message, say):
    uid=message["user"]
    user=get_user(uid)

    total=len(user["tasks"])
    done=0

    for t in user["tasks"]:
        if t["done"]:
            done+=1

    say("total: " + str(total) + " done: " + str(done))

if __name__ == "__main__":
    app.start(port=12712)