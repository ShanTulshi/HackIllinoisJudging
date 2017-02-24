import requests, json

while(True):
    try:
        s = input('json: ')
    except EOFError:
        print()
        break
    payload = {'json':'{"type":"newJudge", "uname":"def", "pass":"thepasswordisunicorns", "data":{"name":"FoodTinder"}}'}
    requests.post("http://localhost:5000/", data=payload)
