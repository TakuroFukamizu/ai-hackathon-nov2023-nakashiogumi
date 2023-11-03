from aiohttp import web
import asyncio
from bottle import route, run, request, post
import requests
import json
import time, threading
import concurrent.futures
import challengerA
import challengerB
import Judge

# @route('/challenger/<name>/', method='POST')

# NOTE: 音声featch path param:特定キャラの名前、 body param:text
# NOTE: judgmentのfetch対象になる予定


async def handle_suggestion(current_step):
    # 各キャラクターからの提案を並行して取得
    suggestion_results = await asyncio.gather(
        suggestionA({'current_step': current_step}),
        suggestionB({'current_step': current_step})
    )

    # 提案結果をjudgmentに送り判定を受け取る
    suggestions = [{'message': res['result_msg'], 'current_step': current_step, 'fromType': 'A' if i == 0 else 'B'}
                   for i, res in enumerate(suggestion_results)]
    judgeResult = Judge.Judge.judgment(suggestions)

    # 判定結果を音声出力
    payload = {'text': judgeResult['result_msg']}
    # NOTE: 以下は参照にあたってeffects/libs直下を立ち上げておく必要あり。音声出力完了を待つため、timeoutは3分とする
    r = await requests.post("http://localhost:8080/challenger/", data=payload, timeout=180)
    # await vv_request_speech(judgeResult['result_msg'])
    print(r)

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
    if character == 'A':
        response = await challengerA.Character.reaction({'current_step': current_step})
    else:
        response = await challengerB.Character.reaction({'current_step': current_step})

    # 反応を音声出力
    # await vv_request_speech(response['result_msg'])

async def main():
    current_step = 0
    winner = None

    while current_step <= 3:
        if winner is not None:
            # 前のステップの勝者から始める
            winner_suggestion = suggestionA if winner == 'A' else suggestionB
            res = await winner_suggestion({'current_step': current_step})
            await vv_request_speech(res['result_msg'])
        winner, current_step = await handle_suggestion(current_step)
        if winner is None:
            # 両方のreactionを呼び出す
            await asyncio.gather(
                handle_reaction('A', current_step),
                handle_reaction('B', current_step)
            )
            break  # 反応後にループ終了

    print("処理を終了します。")  # すべての処理が終わったことを出力
    
    # TODO: M5Stackに投げる
    
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
    web.run_app(app, host='localhost', port=8080)
