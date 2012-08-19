import requests

if __name__ == "__main__":
    c = 0
    tests = [
        "Vivamus scelerisque ornare ipsum",
        "lorem ipsum"
    ]
    for test in tests:
        data = dict(sentence=test)
        r = requests.post("http://localhost:5000/sentences", data=data)
        print r.content
    for test in tests:
        r = requests.get("http://localhost:5000/query/%s" % test)
        print r.content