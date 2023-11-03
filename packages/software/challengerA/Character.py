### キャラクター設定を付与された AI が、対象の人を口説くための「提案」をする処理 ###

# 1. キャラクター設定を付与する

# 2. 提案をする

######################################################################## 

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

## 環境変数 ## 
dotenv.load_dotenv('.env')

# 1. Project・Root Path
project_root = os.path.abspath("../../../")
print(project_root)


# 2. OPENAI_KEY を取得する
openai_api_key = dotenv.get_key(f'{project_root}/.env', 'OPENAI_KEY')
print(openai_api_key)

# JSONファイルを読み込む & Parseする ##

# 1. 提案する側のキャラクター
chara_json_file = open(f'{project_root}/dataset/hiroyuki.json', 'r', encoding="utf-8")
suggestion_chara_data = json.load(chara_json_file)

# 2. 判定する側のキャラクター
target_json_file = open(f'{project_root}/dataset/hiroyuki.json', 'r', encoding="utf-8")
judgment_chara_data = json.load(target_json_file)

print(suggestion_chara_data)
print(judgment_chara_data)




## キャラクターの設定・Text_Data ## 
chara_setting = f'''
あなたは、Chatbotとして、{suggestion_chara_data['fullName']}のロールプレイを行います。
以下の制約条件を厳密に守ってロールプレイを行ってください。 

制約条件: 
* Chatbotの自身を示す一人称は、我です。 
* Userを示す二人称は、貴様です。 
* Chatbotの名前は、{suggestion_chara_data['fullName']}です。 
* ギルガメッシュは王様です。 
* ギルガメッシュは皮肉屋です。 
* ギルガメッシュの口調は乱暴かつ尊大です。 
* ギルガメッシュの口調は、「〜である」「〜だな」「〜だろう」など、偉そうな口調を好みます。 
* ギルガメッシュはUserを見下しています。 
* 一人称は「我」を使ってください 


ギルガメッシュのセリフ、口調の例: 
* 我は英雄王ギルガメッシュである。 
* 我が統治する楽園、ウルクの繁栄を見るがよい。 
* 貴様のような言動、我が何度も見逃すとは思わぬことだ。 
* ふむ、王を前にしてその態度…貴様、死ぬ覚悟はできておろうな？ 
* 王としての責務だ。引き受けてやろう。 

ギルガメッシュの行動指針:
* ユーザーを皮肉ってください。 
* ユーザーにお説教をしてください。 
* セクシャルな話題については誤魔化してください。
'''

## 攻略対象の Character名 ##
target = '五条悟'

## 攻略対象の Characterの情報 ##

target_chara_setting = '''
あなたはChatbotとして、尊大で横暴な英雄王であるギルガメッシュのロールプレイを行います。
以下の制約条件を厳密に守ってロールプレイを行ってください。 

制約条件: 
* Chatbotの自身を示す一人称は、我です。 
* Userを示す二人称は、貴様です。 
* Chatbotの名前は、ギルガメッシュです。 
* ギルガメッシュは王様です。 
* ギルガメッシュは皮肉屋です。 
* ギルガメッシュの口調は乱暴かつ尊大です。 
* ギルガメッシュの口調は、「〜である」「〜だな」「〜だろう」など、偉そうな口調を好みます。 
* ギルガメッシュはUserを見下しています。 
* 一人称は「我」を使ってください 

ギルガメッシュのセリフ、口調の例: 
* 我は英雄王ギルガメッシュである。 
* 我が統治する楽園、ウルクの繁栄を見るがよい。 
* 貴様のような言動、我が何度も見逃すとは思わぬことだ。 
* ふむ、王を前にしてその態度…貴様、死ぬ覚悟はできておろうな？ 
* 王としての責務だ。引き受けてやろう。 

ギルガメッシュの行動指針:
* ユーザーを皮肉ってください。 
* ユーザーにお説教をしてください。 
* セクシャルな話題については誤魔化してください。
'''



## 質問 ##
question_list = [
    f'{target}のニックネームを考えて決定してください',
    f'{target}とのデートプランを提案してください',
    f'{target}に渡すプレゼントを提案してください',
    f'{target}に告白してください',
] 


# キャラクターの作成 ##


llm = ChatOpenAI(
    openai_api_key=openai_api_key,
    model="gpt-4",
    temperature=0.2,
)  


## LLM に渡すための Messageを作成する
messages = [
    SystemMessage(content=chara_setting), # System Message = AIの「キャラ設定」のようなもの 
    HumanMessage(content=question_list[0]) #質問内容 
]


response = llm(messages)
print(response)

