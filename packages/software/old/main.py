import asyncio
import aiohttp
from aiohttp import web
import json
import challengerA
import challengerB
import Judge
import threading

# @route('/challenger/<name>/', method='POST')

# NOTE: 音声featch path param:特定キャラの名前、 body param:text
# NOTE: judgmentのfetch対象になる予定
# 


    
async def handle_suggestion(current_step):
    async with aiohttp.ClientSession() as session:
        try:
            # 各キャラクターからの提案を並行して取得
            suggestion_results = await asyncio.gather(
                asyncio.create_task(challengerA.Character.suggestion({'current_step': current_step})),
                asyncio.create_task(challengerB.Character.suggestion({'current_step': current_step}))
            )
            print('🌟🌟')
            print(suggestion_results)
            
            # 提案結果をjudgmentに送り判定を受け取る
            suggestions = [{'message': res['result_msg'], 'current_step': current_step, 'fromType': res['fromType'],}
                        for i, res in enumerate(suggestion_results)]
            print('🌟')
            print(suggestions)
            
            
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            json_payloadA= json.dumps({'text':suggestions[0]['result_msg'], 'name':suggestions[0]['name'] })
            json_payloadB= json.dumps({'text':suggestions[1]['result_msg'], 'name':suggestions[1]['name'] })
            # それぞれ提案する音声発話
            userA = suggestions[0]['fromType']
            userB = suggestions[1]['fromType']
            await session.post(f'http://localhost:8080/challenger/{userA}/speak/', headers=headers, data=json_payloadA, timeout=180)
            await session.post(f'http://localhost:8080/challenger/{userB}/speak/', headers=headers, data=json_payloadB, timeout=180)
            
            # 判定者に提案内容を送る
            judgeResult = Judge.Judge.judgment(suggestions)
            # 選ばれた挑戦者
            wonChallenger = 'a' if judgeResult['result'][0] == True else 'b'

            # 判定結果を音声出力
            json_payload = json.dumps({'text': judgeResult['result_msg']})
            
            # 判定結果発話　音声再生し、LED演出を行う。 再生が終わったらレスポンスする。
            # NOTE: 音声出力完了を待つため、timeoutは3分とする
            if current_step < 3:
                r = await session.post(
                    "http://localhost:8080/judge/speak/", 
                    headers=headers, 
                    data=json_payload, 
                    timeout=aiohttp.ClientTimeout(total=180))
            else:
                r  = await session.post(f'http://localhost:8080/judge/select/{wonChallenger}', headers=headers, data=json_payload, timeout=180)
                session.post("http://localhost:8080/session/reset", headers=headers, timeout=aiohttp.ClientTimeout(total=180))
            # r = await asyncio.gather(
            #     requests.post("http://localhost:8080/judge/speak/", data=payload, timeout=180),
            #     requests.post("http://localhost:8080/judge/speak/", data=payload, timeout=180)
            # )
            # await vv_request_speech(judgeResult['result_msg'])
            print(r)
            if r.status == 200:
                # Read the response body if needed
                # response_body = await response.text()
                pass
        except asyncio.TimeoutError:
            # Handle request timeout here
            print("Request timed out")
        except aiohttp.ClientError as e:
            # Handle other aiohttp-specific client errors here
            print(f"Client error: {e}")

        # 勝者の提案を次のステップに進める
        if True in judgeResult['result']:
            winner_index = judgeResult['result'].index(True)
            if winner_index == 0:
                return 'A', current_step + 1
            else:
                return 'B', current_step + 1
        else:
            # どちらも勝者がいない場合は次のステップに進まない
            return None, current_step


async def handle_reaction(character, current_step):
    async with aiohttp.ClientSession() as session:
        try:
            if character == 'A':
                response = await challengerA.Character.reaction({'current_step': current_step})
            else:
                response = await challengerB.Character.reaction({'current_step': current_step})

            # 反応を音声出力
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            await session.post("http://localhost:8080/judge/speak/", headers={headers}, timeout=aiohttp.ClientTimeout(total=180))
            
            json_payloadA= json.dumps({'text':response[0]['result_msg'], 'name':response[0]['name'] })
            json_payloadB= json.dumps({'text':response[1]['result_msg'], 'name':response[0]['name'] })
            if character == 'A':
                await session.post(f'http://localhost:8080/challenger/{character}/speak/', headers=headers, data=json_payloadA, timeout=aiohttp.ClientTimeout(total=180))    
            else:
                await session.post(f'http://localhost:8080/challenger/{character}/speak/', headers=headers, data=json_payloadB, timeout=aiohttp.ClientTimeout(total=180))    
            # await vv_request_speech(response['result_msg'])
        except asyncio.TimeoutError:
            # Handle request timeout here
            print("Request timed out")
        except aiohttp.ClientError as e:
            # Handle other aiohttp-specific client errors here
            print(f"Client error: {e}")

async def main():
    async with aiohttp.ClientSession() as session:
        try:
            current_step = 0
            winner = None
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}

            print('Main Python Call')

            while current_step <= 3:
                if winner is not None:
                    # 前のステップの勝者から始める
                    winner_suggestion = challengerA.Character.suggestion if winner == 'A' else challengerB.Character.suggestion

                    res = await winner_suggestion({'current_step': current_step})
                    # await vv_request_speech(res['result_msg'])
                    json_payloadA= json.dumps({'text':res[0]['result_msg'], 'name':res[0]['name'] })
                    json_payloadB= json.dumps({'text':res[1]['result_msg'], 'name':res[0]['name'] })
                    if (winner == 'A'):
                        await session.post(f'http://localhost:8080/challenger/{winner}/speak/', headers=headers, data=json_payloadA, timeout=aiohttp.ClientTimeout(total=180))    
                    else:
                        await session.post(f'http://localhost:8080/challenger/{winner}/speak/', headers=headers, data=json_payloadB, timeout=aiohttp.ClientTimeout(total=180))
                winner, current_step = await handle_suggestion(current_step)
                print('winner', winner)
                print('current_step', current_step)
                print('------------------------------------------------------------------')
                if winner is None:
                    # 両方のreactionを呼び出す
                    await asyncio.gather(
                        handle_reaction('A', current_step),
                        handle_reaction('B', current_step)
                    )
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
