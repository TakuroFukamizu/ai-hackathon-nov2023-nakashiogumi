# Router & Template_Render
from flask import  Blueprint, render_template

import traceback
# Post受信をするためにFlask_requestをimportする
from flask import request, jsonify

# import requests
import pprint

import pandas as pd

import asyncio
import aiohttp
from aiohttp import web
import json
import challengerA
import challengerB
import Judge

# PythonからPythonScriptを呼び出すためのモジュール！ => プログラム内でコマンド実行！
# import subprocess

# Generate Router Instance => Base_URLの設定はここ！
router = Blueprint('router', __name__ )


# ルート, Method: GET
@router.route('/', methods=['GET'])
def index():
    try :
        return 'Rootama-API'
    except Exception as error :
        error_msg:str = traceback.format_exc()

# Robotama_エンドポイント, Method: GET
@router.route('/robotama', methods=['GET'])
def robotama():
  return 'Robotamaなのだ！！'



def main():
  try:
      current_step = 0
      winner = None
      headers = {'Content-Type': 'application/x-www-form-urlencoded'}

      while current_step <= 3:
          if winner is not None:
              # 前のステップの勝者から始める
              winner_suggestion = challengerA.Character.suggestion if winner == 'A' else challengerB.Character.suggestion
              res = winner_suggestion({'current_step': current_step})
              # await vv_request_speech(res['result_msg'])
              json_payloadA= json.dumps({'text':res[0]['result_msg'], 'name':res[0]['name'] })
              json_payloadB= json.dumps({'text':res[1]['result_msg'], 'name':res[0]['name'] })
              if (winner == 'A'):
                  session.post(f'http://localhost:8080/challenger/{winner}/speak/', headers=headers, data=json_payloadA, timeout=aiohttp.ClientTimeout(total=180))    
              else:
                  session.post(f'http://localhost:8080/challenger/{winner}/speak/', headers=headers, data=json_payloadB, timeout=aiohttp.ClientTimeout(total=180))
          winner, current_step = handle_suggestion(current_step)
          if winner is None:
              # 両方のreactionを呼び出す
              
              handle_reaction('A', current_step),
              handle_reaction('B', current_step)

              break  # 反応後にループ終了
      
  except asyncio.TimeoutError:
      # Handle request timeout here
      print("Request timed out")
  except aiohttp.ClientError as e:
      # Handle other aiohttp-specific client errors here
      print(f"Client error: {e}")

  print("処理を終了します。")  # すべての処理が終わったことを出力
        

# Requestの後処理
@router.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response