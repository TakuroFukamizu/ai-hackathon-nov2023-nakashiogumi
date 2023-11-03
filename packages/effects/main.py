from bottle import route, run, request, post
import requests
import json
from .libs.voicebox import vv_resuqest_speach

@route('/hello')
def hello():
    return "Hello World!"

@route('/challenger/<name>/', method='POST')
def speak_challenger(name):
    data = json.load(request.json)
    text = data['text']
    # voicevoxに投げる
    vv_resuqest_speach(text)
    # TODO: M5Stackに投げる



run(host='localhost', port=8080, debug=True)