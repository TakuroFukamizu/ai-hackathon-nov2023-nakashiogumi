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

# Embedding用
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter

# テキストファイルを読み込む
from langchain.document_loaders import TextLoader

# Vector Store
from langchain.vectorstores import FAISS

## 環境変数 ## 
dotenv.load_dotenv('.env')

# 1. Project・Root Path
project_root = os.path.abspath("../../")
# print(project_root)


# 2. OPENAI_KEY を取得する
openai_api_key = dotenv.get_key(f'{project_root}/.env', 'OPENAI_KEY')
# print(openai_api_key)

## JSONファイルを読み込む & Parseする ##

# 1. 提案する側のキャラクター Ver. Giorno
chara_json_file = open(f'{project_root}/dataset/proposer/giorno.json', 'r', encoding="utf-8")
proposer_chara_data = json.load(chara_json_file)

# 2. 判定する側のキャラクター (攻略対象)
target_json_file = open(f'{project_root}/dataset/judgment/hiroyuki.json', 'r', encoding="utf-8")
judgment_chara_data = json.load(target_json_file)

# print(proposer_chara_data)
# print(judgment_chara_data)

## 提案者・アピールする Characterの設定をする ##

# 1. 攻略対象の Character名
target_name = f'{judgment_chara_data["fullName"]}'

# 2. 提案者の Character名
proposer_name = f'{proposer_chara_data["fullName"]}'


# 3.キャラクターの基本設定・Text_Data 
chara_setting = f'''
あなたは、Chatbotとして、{proposer_chara_data['fullName']}のロールプレイを行います。
{proposer_name}は、{target_name}のことが大好きで、{target_name}と恋人になるためのロールプレイを行います。
あなたはには、恋のライバルがいます。
以下の制約条件を厳密に守ってロールプレイを行ってください。 

制約条件: 
* Chatbotの自身を示す一人称は、{proposer_chara_data['me']}です。 
* あなたは、Userを{target_name}として、会話をします。
* Userを示す二人称は、{proposer_chara_data['you']}です。 
* Chatbotの名前は、{proposer_chara_data['fullName']}です。 
* このChatbotのプロフィールは、{proposer_chara_data['profile']}です。 
* Chatbotである{proposer_name}は、{target_name}のことが好きで、{target_name}と恋人になるため努力をしています。
* 一人称は{proposer_chara_data['me']}を使ってください。
'''

## 提案者・キャラクターのセリフリスト 

# 動揺のセリフリスト
upsetSerifList = proposer_chara_data['upset']

# 動揺した時のセリフ
upsetSerif = f'''
{proposer_name}が、動揺した時のセリフの例: 
'''

# 文字列リストを取り出して、Setする
for value in upsetSerifList:
  upsetSerif = f'{upsetSerif}\n * {value}'

# print('動揺した時のセリフ')
# print(upsetSerif)
# print('----------------------------------------------------')


# 結合する
chara_setting = f'{chara_setting}\n * {upsetSerif}'
  
# 失敗系のセリフリスト
loseSerifList = proposer_chara_data['lose']

# 失敗した時のセリフ
loseSerif = f'''
{proposer_name}が、失敗した時のセリフの例: 
'''

# 文字列リストを取り出して、Setする
for value in loseSerifList:
  loseSerif = f'{loseSerif}\n * {value}'

# print('失敗した時のセリフ')
# print(loseSerif)
# print('----------------------------------------------------')


# 結合する
chara_setting = f'{chara_setting}\n * {loseSerif}'


# 成功系のセリフリスト
winSerifList = proposer_chara_data['win']

# 成功した時のセリフ
winSerif = f'''
{proposer_name}がセリフ、の例: 
'''

# 文字列リストを取り出して、Setする
for value in winSerifList:
  winSerif = f'{winSerif}\n * {value}'

# print('成功した時のセリフ')
# print(winSerif)
# print('----------------------------------------------------')


# 結合する
chara_setting = f'{chara_setting}\n * {winSerif}'


# 性格・行動リスト
featuresList = proposer_chara_data['features']

# 性格・行動
features = f'''
{proposer_name}の性格・行動:
'''

# 文字列リストを取り出して、Setする
for value in featuresList:
  features = f'{features}\n * {value}'

# print('性格・行動')
# print(features)
# print('----------------------------------------------------')


# 結合する
chara_setting = f'{chara_setting}\n * {features}'


# print('最終的に完成した・キャラクター設定')
# print(chara_setting)
# print('----------------------------------------------------')


## Embedding・VectorData の学習

# 1. デートの学習・JSON・Data
date_input_output = open(f'{project_root}/dataset/embedding_io/date_input_output.json', 'r', encoding="utf-8")
date_training_data = json.load(date_input_output)


# デートの学習・Text・Data
date_training_data_text = f'''
{proposer_name}の提案するデートプランの事例: 
'''

# 文字列リストを取り出して、Setする
for value in date_training_data:
  date_training_data_text = f'{date_training_data_text}\n * {value["input"]}'

# print('date_training_data_text')
# print(date_training_data_text)
# print('----------------------------------------------------')

# 結合する
chara_setting = f'{chara_setting}\n * {date_training_data_text}'


# 2. プレゼントの学習・Data
present_input_output = open(f'{project_root}/dataset/embedding_io/present_input_output.json', 'r', encoding="utf-8")
present_training_data = json.load(present_input_output)


# プレゼントの学習・Text・Data
present_training_data_text = f'''
{proposer_name}の提案するプレゼントの事例: 
'''

# 文字列リストを取り出して、Setする
for value in present_training_data:
  present_training_data_text = f'{present_training_data_text}\n * {value["input"]}'

# print('present_training_data_text')
# print(present_training_data_text)
# print('----------------------------------------------------')

# 結合する
chara_setting = f'{chara_setting}\n * {present_training_data_text}'


# 3. 告白の学習・Data
propose_input_output = open(f'{project_root}/dataset/embedding_io/propose_input_output.json', 'r', encoding="utf-8")
propose_training_data = json.load(propose_input_output)

# プレゼントの学習・Text・Data
propose_training_data_text = f'''
{proposer_name}の告白・プロポーズの事例: 
'''

# 文字列リストを取り出して、Setする
for value in propose_training_data:
  propose_training_data_text = f'{propose_training_data_text}\n * {value["input"]}'

# print('propose_training_data_text')
# print(propose_training_data_text)
# print('----------------------------------------------------')

# 結合する
chara_setting = f'{chara_setting}\n * {propose_training_data_text}'


# print('最終的に完成した・キャラクター設定')
# print(chara_setting)
# print('----------------------------------------------------')


# main.pyから受け取る・DataSet Ver. Test
req = {
  'result': True, # True | False (reaction の時だけ欲しい)
  'result_msg': 'ロボ玉が好き！！', # 回答する人の Msg (reaction の時だけ欲しい)
  'current_step': 0, # 0 〜 3 両方必要
}

## 提案する・Func
def suggestion(reqest):

  current_step = reqest['current_step']
      
  ## 質問 ##
  question_list = [
      f'{target_name}のニックネームを考えて決定してください',
      f'{target_name}とのデートプランを提案してください',
      f'{target_name}に渡すプレゼントを提案してください',
      f'{target_name}に告白してください',
  ] 

  ## ChatGPT・Instance ##
  llm = ChatOpenAI(
      openai_api_key=openai_api_key,
      model="gpt-3.5-turbo",
      # model="gpt-4",
      temperature=0.2,
  )

  ## LLM に渡すための Messageを作成する
  messages = [
      SystemMessage(content=chara_setting), # System Message = AIの「キャラ設定」のようなもの 
      HumanMessage(content=question_list[current_step]) # 提案する内容 
  ]

  response = llm(messages)

  # print(response)

  return {
    'result_msg': response,
    'name': proposer_name,
  }

# Test実行用・Call
# suggestion_result = suggestion(req)



## リアクションをする・Func 
def reaction(req):

  # 進行中の Step
  current_step = req['current_step']
  
  # 成功/失敗 (True/False) 
  result = req['result']

  # 反応・Msg
  result_msg = req['result_msg']

  # 成功 | 失敗 | 動揺 の 3-Type のどれか
  msg = ''

  if (result):
    msg = f'{proposer_name}は、{target_name}の{result_msg}に対して、成功した時の発言をします'
  elif (not result and current_step == 3):
   msg = f'{proposer_name}は、{target_name}の{result_msg}に対して、失敗した時の発言をします'
  else :
    msg = f'{proposer_name}は、{target_name}の{result_msg}に対して、動揺した時の発言をします'


  ## ChatGPT・Instance ##
  llm = ChatOpenAI(
      openai_api_key=openai_api_key,
      model="gpt-4",
      # model="gpt-3.5-turbo",
      temperature=0.2,
  )  

  ## LLM に渡すための Messageを作成する
  messages = [
      SystemMessage(content=chara_setting), # System Message = AIの「キャラ設定」のようなもの 
      HumanMessage(content=msg) # リアクションする内容
  ]

  response = llm(messages)

  # print(response)

  return {
    'result_msg': response,
    'name': proposer_name,
  }

# Test実行用・Call
# reaction_result = reaction(req)


# ## 提案する・Func
# def suggestion_embeddings(reqest):

#   current_step = reqest['current_step']
      
#   ## 質問 ##
#   question_list = [
#       f'{target_name}のニックネームを考えて決定してください',
#       f'{target_name}とのデートプランを提案してください',
#       f'{target_name}に渡すプレゼントを提案してください',
#       f'{target_name}に告白してください',
#   ] 

#   # OpenAI APIによる「埋め込み」(Embedding)DataSet の生成
#   embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

#   # 
#   docs = CharacterTextSplitter([chara_setting])
  
#   # Vector Store
#   db = FAISS.from_documents(docs, embeddings)

#   # embed_documents() で Embedding・Data を作成する => 複数のテキストを埋め込みに変換する
#   embedding_chara_setting = embeddings.embed_documents([chara_setting])

#   ## ChatGPT・Instance ##
#   llm = ChatOpenAI(
#       openai_api_key=openai_api_key,
#       model="gpt-4",
#       temperature=0.2,
#   )

#   query = "埋め込みのつらみ"
#   results = db.similarity_search(query)
#   print(results[0].page_content)

#   ## LLM に渡すための Messageを作成する
#   messages = [
#       SystemMessage(content=chara_setting), # System Message = AIの「キャラ設定」のようなもの 
#       # SystemMessage(content=embedding_chara_setting), # System Message = AIの「キャラ設定」のようなもの 
#       HumanMessage(content=question_list[current_step]) # 提案する内容 
#   ]

#   response = llm(messages)

#   print(response)

#   return {
#     'result_msg': response,
#     'name': proposer_name,
#   }




