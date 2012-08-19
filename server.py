from trippin.settings import INDEXING_ENGINE, SCORE_FUNCTION
from trippin.utils import load_object

from flask import Flask, request, abort
from store import Store

import json
import settings

index = load_object(INDEXING_ENGINE)()
scorer = load_object(SCORE_FUNCTION)
store = Store(index, scorer)
app = Flask(__name__)

@app.route("/sentences", methods=["POST"])
def api_insert():
    sentence = request.form.get('sentence', None)
    data = request.form.get('data', None)
    if not sentence:
        abort(403)
    if data:
        data = json.loads(data)
    wid = store.insert(sentence.strip(), data=data)
    return json.dumps(dict(wid=wid)) 

@app.route("/sentences/<wid>", methods=["GET", "DELETE"])
def api_get_or_delete(wid):
    if request.method == "GET":
        if wid not in store.sentence_map:
            abort(404)
        else:
            return store.sentence_map[wid]
    elif request.method == "DELETE":
        return "delete"

@app.route("/status", methods=["GET"])
def api_status():
    return json.dumps(store.status())

@app.route("/query/<query>", methods=["GET"])
def api_query(query):
    results = sorted(store.query(query), reverse=True)
    limit = request.args.get("limit", None)
    try:
        limit = int(limit)
    except:
        limit = None
    if limit is not None and limit >= 1:
        results = results[:limit]
    return json.dumps([dict(score=score, match=sentence)
        for score, sentence in results])

if __name__ == '__main__':
    app.run(debug=settings.DEBUG)