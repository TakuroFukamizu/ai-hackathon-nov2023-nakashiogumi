from bottle import route, run, request, post
import requests
import json
import libs

@route('/hello')
def hello():
    return "Hello World!"

@route('/challenger/<name>/', method='POST')
def speak_challenger(name):
    data = request.json  # JSONデータを取得
    text = data.get('text', '')
    # voicevoxに投げる
    ilbs.voicebox.vv_resuqest_speach(text)
    # TODO: M5Stackに投げる



run(host='localhost', port=8080, debug=True)