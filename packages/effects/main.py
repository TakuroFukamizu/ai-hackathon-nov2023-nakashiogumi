import asyncio
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

async def handle_suggestion(current_step):
    # 各キャラクターからの提案を並行して取得
    suggestion_results = await asyncio.gather(
        suggestionA({'current_step': current_step}),
        suggestionB({'current_step': current_step})
    )

    # 提案結果をhogehogeに送り判定を受け取る
    suggestions = [{'message': res['result_msg'], 'current_step': current_step, 'fromType': 'A' if i == 0 else 'B'}
                   for i, res in enumerate(suggestion_results)]
    judgement = hogehoge(suggestions)

    # 判定結果を音声出力
    await vv_request_speech(judgement['result_msg'])

    # 勝者の提案を次のステップに進める
    if True in judgement['result']:
        winner_index = judgement['result'].index(True)
        if winner_index == 0:
            return 'A', current_step + 1
        else:
            return 'B', current_step + 1
    else:
        # どちらも勝者がいない場合は次のステップに進まない
        return None, current_step

async def handle_reaction(character, current_step):
    if character == 'A':
        response = await reactionA({'current_step': current_step})
    else:
        response = await reactionB({'current_step': current_step})

    # 反応を音声出力
    await vv_request_speech(response['result_msg'])

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

if __name__ == '__main__':
    asyncio.run(main())
