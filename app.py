import os
from flask import Flask, jsonify, request
import json
import getopt
import signal
from queue import Queue, PriorityQueue

users_file = "users.db"
pass_file = "pass.db"

# Number of projects
# TODO Allow projects to be added ad hoc
num_proj = 100

# number of judges
# TODO Allow judges to be added ad hoc
num_judges = 25

# Number of upcoming entries shown to judges
list_len = 2

app = Flask(__name__)

def writeToFile():
    u = open(users_file, "w+")
    p = open(pass_file, "w+")
    u.truncate()
    p.truncate()
    for key, val in users.items():
        u.write(key + "\n")
        p.write(val + "\n")

def interrupt(sig, frame):
    print("\nShutting Down...", end="\r")
    writeToFile()
    exit()

signal.signal(signal.SIGINT, interrupt)
users = {'def':'thepasswordisunicorns'}

# Dict of dicts with a 0 or 1 for ranking
matchups = {}

class Project:
    def __init__(self, name, members, tabl):
        assert type(name) is str
        assert type(members) is list
        self.name = name
        self.num = 0        # Number of times a project hass been judged
        self.members = members
        self.tabl = tabl
        self.score = 0

    def __lt__(self, other):
        return self.num < other.num

def addToQ(proj):
    proj.num += 1
    if(not wait.empty()):
        j = wait.get_nowait()
        j.list.append(proj)
    else:
        pq.put_nowait(proj)


class Judge:
    def __init__(self, name):
        assert type(name) is str
        self.name = name
        self.list = []
        self.set = set()
        self.prev = None


tables = [-1] * num_proj

judges = [None] * num_judges

pq = PriorityQueue()
wait = Queue()

# Current count of number of projects already added.
# Tables should be zero-indexed
ij = 0

# Function is called when a project is judged for feedback.
# Returns (list?) of next projects to judge.
def judge(js):
    if('judge' not in js or 'feedback' not in js):
        return 'Error, incorrect parameters'
    proj = self.list[0]
    self.list = self.list[1:]
    addToQ(proj)
    try:
        newp = pq.get_nowait()
    except Empty:
        wait.put(self)
        if(len(wait) == num_judges):
            return "Judging period is over!"
    # Check that project has not been judged before,
    # Check that this matchup has not happened before
    self.list.append(newp)
    return str(self.list[0])


def add_proj(proj):
    global ij
    assert type(proj) is Project
    assert ij < num_proj

    tables[ij] = proj
    judges[ij % num_judges].list.append(ij)
    ij += 1


def newProj(js):
    if('name' and 'members' in js):
        proj = Project(js['name'], js['members'], ij)
        add_proj(proj)
    else:
        return "Error, incorrect parameters"

def newUser(js):
    if('name' not in js and 'pass' not in js):
        return "Bad user parameters!"
    elif(users.get(js['name']) != None or js['name'] == 'def'):
        return "User already exists!"
    else:
        users[js['name']] = js['pass']
        users.pop('def', None)
        return "User added!"

def newJudge(js):
    if('name' not in js):
        return "Bad judge parameters!"
    else:
        judges.append(Judge(js['name']))
        return "Judge added successfully!"

@app.route("/", methods=['GET', 'POST'])
def main():
    if(request.method == 'POST'):
        if ('json' not in request.form):
            return "Error, request does not contain json"
        else:
            js = json.loads(request.form['json'])
            if not all (k in js for k in ['type', 'uname', 'pass', 'data']):
                return "Malformed json!"
            elif(users.get(js['uname']) == js['pass']):
                func = {
                    'newUser' : newUser,
                    'newProj' : newProj,
                    'newJudge' : newJudge,
                    'judge' : judge
                }.get(js['type'])
                if(func is not None):
                    return func(js['data'])
                else:
                    return "unsupported operation!"
            else:
                return "Invalid login!"
    elif(request.method=='GET'):
        return "Welcome to the Judging application!"

if __name__== '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="localhost", port=port, debug=True)
