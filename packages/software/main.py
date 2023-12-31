import asyncio
import aiohttp
from aiohttp import web
import json
import challengerA
import challengerB
import Judge
import requests
import time

# @route('/challenger/<name>/', method='POST')

# NOTE: 音声featch path param:特定キャラの名前、 body param:text
# NOTE: judgmentのfetch対象になる予定
# 

def handle_suggestion(current_step):

    resultA = challengerA.Character.suggestion({'current_step': current_step})
    print('resultA')
    print(resultA)
    print('-------------------------------------------------------------------')
    
    resultB = challengerB.Character.suggestion({'current_step': current_step})
    print('resultB')
    print(resultB)
    print('-------------------------------------------------------------------')


    print('🌟🌟')
    # print(suggestion_results)
  
  
    # 提案結果をjudgmentに送り判定を受け取る
    suggestions = [
        {'message': resultA['result_msg'], 'current_step': current_step, 'fromType': resultA['fromType'], 'name': resultA['name']},
        {'message': resultB['result_msg'], 'current_step': current_step, 'fromType': resultB['fromType'], 'name': resultB['name']},
    ]

    print('🌟')
    print(suggestions)
    
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    json_payloadA= {'text':suggestions[0]['message'], 'name':suggestions[0]['name'] }
    json_payloadB= {'text':suggestions[1]['message'], 'name':suggestions[1]['name'] }
    # それぞれ提案する音声発話
    userA = suggestions[0]['fromType']
    userB = suggestions[1]['fromType']

    # それぞれ提案する音声発話
    userA = suggestions[0]['fromType']
    userB = suggestions[1]['fromType']
    requests.post(f'http://localhost:8080/challenger/{userA}/speak/', headers=headers, data=json_payloadA, timeout=None)

    time.sleep(10)

    requests.post(f'http://localhost:8080/challenger/{userB}/speak/', headers=headers, data=json_payloadB, timeout=None)
    
    # 判定者に提案内容を送る
    judgeResult = Judge.Judge.judgment(suggestions)
    # 選ばれた挑戦者
    wonChallenger = 'a' if judgeResult['result'][0] == True else 'b'

    # 判定結果を音声出力
    json_payload = {'text': judgeResult['result_msg']}
    
    # 判定結果発話　音声再生し、LED演出を行う。 再生が終わったらレスポンスする。


    if current_step < 3:
        requests.post( "http://localhost:8080/judge/speak/",  headers=headers, data=json_payload, timeout=None)
    else:

        r = requests.post(f'http://localhost:8080/judge/select/{wonChallenger}', headers=headers, data=json_payload, timeout=None)
        time.sleep(10)
        requests.post("http://localhost:8080/session/reset", headers=headers, timeout=None)

    # 勝者の提案を次のステップに進める
    if True in judgeResult['result']:
        winner_index = judgeResult['result'].index(True)
        if winner_index == 0:
            return 'a', current_step + 1
        else:
            return 'b', current_step + 1
    else:
        # どちらも勝者がいない場合は次のステップに進まない
        return None, current_step

# リアクション・ターン
def handle_reaction(character, current_step):
    try:
        if character == 'a':
            response = challengerA.Character.reaction({'current_step': current_step})
            time.sleep(10)
        else:
            response = challengerB.Character.reaction({'current_step': current_step})
            time.sleep(10)

        # 反応を音声出力
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        
        json_payloadA= {'text':response[0]['result_msg'], 'name':response[0]['name'] }
        json_payloadB= {'text':response[1]['result_msg'], 'name':response[1]['name'] }

        if character == 'a':
            requests.post(f'http://localhost:8080/challenger/{character}/speak/', headers=headers, data=json_payloadA,  timeout=None)
        else:
            requests.post(f'http://localhost:8080/challenger/{character}/speak/', headers=headers, data=json_payloadB,  timeout=None)
        
    except asyncio.TimeoutError:
        # Handle request timeout here
        print("Request timed out")
    except aiohttp.ClientError as e:
        # Handle other aiohttp-specific client errors here
        print(f"Client error: {e}")

def main():
    try:
        current_step = 0
        winner = None
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}

        # while current_step <= 3:
        while current_step == 0:
            winner, current_step = handle_suggestion(current_step)
            if winner is None:
                # 両方のreactionを呼び出す
                
                handle_reaction('a', current_step),
                handle_reaction('b', current_step)

                break  # 反応後にループ終了
        
    except asyncio.TimeoutError:
        # Handle request timeout here
        print("Request timed out")
    except aiohttp.ClientError as e:
        # Handle other aiohttp-specific client errors here
        print(f"Client error: {e}")

    print("処理を終了します。")  # すべての処理が終わったことを出力
        
    
async def start_background_tasks(app):
    app['main'] = asyncio.create_task(main())

async def cleanup_background_tasks(app):
    app['main'].cancel()
    await app['main']
    

app = web.Application()
app.add_routes([web.get('/', main)])
app.on_startup.append(start_background_tasks)
app.on_cleanup.append(cleanup_background_tasks)

if __name__ == '__main__':
    web.run_app(app, host='localhost', port=8081)
