from bottle import route, run, request, post
import requests
import json
import time, threading
from .libs.voicebox import vv_resuqest_speach
import concurrent.futures
from packages.software.challengerA.Character import suggestion as suggestionA #CharactorAの提案
from packages.software.challengerA.Character import reaction as reactionA #CharactorAのリアクション
from packages.software.challengerB.Character import suggestion as suggestionB #CharactorBの提案
from packages.software.challengerB.Character import reaction as reactionB #CharactorBのリアクション
from packages.software.fileC import hogehoge  # 判定結果とメッセージを返却するロジック

@route('/hello')
def hello():
    return "Hello World!"

@route('/challenger/<name>/', method='POST')

def vv_resuqest_speach(text):
    # ここに音声出力のコードを記述
    pass


def process_step(step, request):
    # STEPごとに処理を分ける
    if step == 0:
        # 呼び名・ニックネームの提案
        pass
    elif step == 1:
        # デートプランの提案
        pass
    elif step == 2:
        # プレゼントの提案
        pass
    elif step == 3:
        # 告白の処理
        pass
  
req = {
  'result': True, # True | False (reaction の時だけ欲しい)
  'result_msg': 'ロボ玉が好き！！', # reaction の時だけ欲しい
  'current_step': 0, # 0 〜 3 両方必要
}

def speak_challenger():
    steps = [0, 1, 2, 3]  # 処理するSTEP
    request = 'some_request'  # リクエストの詳細

    # スレッドオブジェクトの生成
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(suggestionA, request): 'A',
            executor.submit(suggestionB, request): 'B'
        }
        # ABそれぞれの処理を非同期実行するLoop
        for future in concurrent.futures.as_completed(futures):
            try:
                response = future.result()
                result_message = response.get('result_msg', '')
                # 結果を音声出力ファイルに渡す
                vv_resuqest_speach(result_message)
                # 結果を判定ロジックに渡す
                hogehoge(result_message)
                
                
            except Exception as exc:
                print(f'Generated an exception: {exc}')

    # 以下にreactionの処理を追加する
      
def speak_challenger(name):
    data = json.load(request.json)
    text = data['text']
    

    # LoopしてSTEP1-4を回す
    # STEP-0. 呼び名・ニックネームの提案
    # STEP-1. デートプランの提案
    # STEP-2. プレゼントの提案
    # STEP-3. 告白
    

    
    # voicevoxに投げる
    vv_resuqest_speach(text)
    # TODO: M5Stackに投げる
    
    
    # judgeからのresult:{step:0, status:'ok'|'ng', message}
    # suggestionからのresult: {step:0, [{challenger: {id:XX, name:XX, nickName: XX}, message},]
        # 提案をmainが受け取ったら2つの提案をjudgeに渡す

    # response返す
    # 受け取ったらmode resultを提案者に
    # thread分けない
    # httpで
    # 順番に分ける
    # challengerABの解答を考えるのを順番にやったら長すぎるから並列にする
    # 直列にしないと制御が増える


run(host='localhost', port=8080, debug=True)

# if __name__ == '__main__':
#     main()