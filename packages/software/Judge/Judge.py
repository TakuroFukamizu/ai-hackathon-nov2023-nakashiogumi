### キャラクター設定を付与された AI が、2つの回答のどちらが良いかを「判断」をする処理 ###

## Import Block ##
from langchain.chat_models import ChatOpenAI
from langchain.schema import (
    SystemMessage, # システムメッセージ 
    HumanMessage, # 人間の質問 
    AIMessage, # ChatGPTの返答
)

import openai
import json
import pprint
import dotenv
import os
import sys

### 変数設定 ###

## 基本設定 ##

# 環境変数 
dotenv.load_dotenv('.env')

# Project・Root Path
project_root = os.path.abspath("../../../")

# OPENAI_KEY を取得する
openai_api_key = dotenv.get_key(f'{project_root}/.env', 'OPENAI_KEY')

# ChatGPTの基本設定
llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    model="gpt-3.5-turbo",
    temperature=0.2,
)

## 人物設定 ##

# 提案者Aのキャラクター情報の取得
proposer_A_json = open(f'{project_root}/dataset/proposer/char.json', 'r', encoding="utf-8")
proposer_A_data = json.load(proposer_A_json)

# 回答者Aの名前 
proposer_A_name = f'{proposer_A_data["fullName"]}'

# 提案者Bのキャラクター情報の取得
proposer_B_json = open(f'{project_root}/dataset/proposer/giorno.json', 'r', encoding="utf-8")
proposer_B_data = json.load(proposer_B_json)

# 回答者Bの名前 
proposer_B_name = f'{proposer_B_data["fullName"]}'

# 回答者のキャラクター情報の取得
judgeman_json = open(f'{project_root}/dataset/judgment/hiroyuki.json', 'r', encoding="utf-8")
judgeman_data = json.load(judgeman_json)

# 回答者の名前 
judgeman_name = f'{judgeman_data["fullName"]}'

# 質問 
question_list = [
    f'{judgeman_name}のニックネームを考えて決定してください',
    f'{judgeman_name}とのデートプランを提案してください',
    f'{judgeman_name}に渡すプレゼントを提案してください',
    f'{judgeman_name}に告白してください',
    ]


### 判断をする処理関数 ###
def judgment(request):

    # 引数から回答を整理（）
    if request[0]['fromType'] == 'A':
        proposer_A_answer = request[0]['message']
        proposer_B_answer = request[1]['message']
    else: proposer_A_answer = request[1]['message']
    proposer_B_answer = request[0]['message']
    
    # llmに渡す際のsystem側の設定を整理
    #ベース設定
    chara_setting = f'''
    あなたは、Chatbotとして、{judgeman_name}のロールプレイを行います。
    あなたは{question_list[0]}という質問に対して{proposer_A_name}と{proposer_B_name}の2人から回答を受けています。
    \n\n{proposer_A_name}の回答：{proposer_A_answer}
    \n\n{proposer_B_name}の回答は{proposer_B_answer}
    あなたにとってどちらの回答が魅力的に映ったかを回答してください。
    以下の制約条件を厳密に守ってロールプレイを行ってください。 
    '''

    #判断1.のための制約条件
    restriction1 = f'''
            制約条件: 
            * あなたは2つの回答のうちどちらの回答が魅力的かを必ず回答する必要があります。
            * どちらの回答が良いか{proposer_A_name}または{proposer_B_name}だけを回答してください。
            '''

    #判断2.のための制約条件
    restriction2 = f'''
            制約条件: 
            * Chatbotの自身を示す一人称は、{judgeman_data['me']}です。 
            * あなたは、2つの回答のうちどちらの回答が魅力的だったかを絶対に回答する必要があります。
            * Chatbotの名前は、{judgeman_data['fullName']}です。 
            * このChatbotのプロフィールは、{judgeman_data['profile']} 
            * 一人称は{judgeman_data['me']}を使ってください。
            '''

    #ベース情報 + 制約条件で設定整理
    chara_setting1 = f'{chara_setting}\n {restriction1}'
    chara_setting2 = f'{chara_setting}\n {restriction2}'

    # 1.どちらが良い回答かを決定する → return 時の「result」に対応
    messages = [
        SystemMessage(content=chara_setting1), # System Message = AIの「キャラ設定」のようなもの 
        HumanMessage(content=f'{proposer_A_name}と{proposer_B_name}のどちらの回答が良いか決めて下さい。') #質問内容 
    ]

    # LLMの応答を取得
    response = llm(messages)
    print("response")
    print(response)

    if proposer_A_name in response:
        selected_proposer = proposer_A_name
        result = [True, False]
    else: selected_proposer = proposer_B_name
    result = [False, True]

    print("selected_proposer")
    print(selected_proposer)

    # 2.1.の回答の理由を決定する → return 時の「result_msg」に対応
    messages2 = [
        SystemMessage(content=chara_setting2), # System Message = AIの「キャラ設定」のようなもの 
        HumanMessage(content=f'あなたは{selected_proposer}の回答が良いと回答しました。より魅力的に感じた理由を教えて下さい。') #質問内容 
    ]

    if response:
        response2 = llm(messages2)
        print("response2.content")
        print(response2.content)
       
    if response and response2:
        return {
            'result': result, 
            'result_msg': response2.content,
            'current_step': request[0]['current_step'], 
        }

# main.pyから受け取る・DataSet Ver. Test
req =[
    {
        'message': '西村博之のニックネームは「ひろ」です。',
        'current_step': 0,
        'fromType': 'B' 
    },{
        'message': '西村博之のニックネームは「ハッキー」です。',
        'current_step': 0,
        'fromType': 'A' 
    }]

judgment_result = judgment(req)

print("judgment_result")
print(judgment_result)




