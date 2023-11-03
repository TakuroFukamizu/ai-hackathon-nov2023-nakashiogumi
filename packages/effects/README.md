
## Requirements
Python3

## Setup
Install libs
```bash
yarn install
```

set configs to `.env` file
```bash
VOICEVOX_URL=http://192.168.122.230:50021 # address and port for VoiceVox hosted server
PORT=8080 # port for running effect service
SERIAL_PATH=/dev/cu.usbserial-xxxxxx # LED Controller
```

## Run
launch voicevox docker  
```bash
docker pull voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
docker run --rm --gpus all -p '50021:50021' voicevox/voicevox_engine:nvidia-ubuntu20.04-latest
```

launch server
```bash
yarn run start
```

## API

| Method |         Path          |                     Description                      |
| ------ | --------------------- | ---------------------------------------------------- |
| POST   | /challenger/:id/speak | チャレンジャーA,Bが発話する際に呼び出す              |
| POST   | /judge/speak          | ジャッジが発話する際に呼び出す                       |
| POST   | /judge/select/:id     | ジャッジがチャレンジャーAまたはBを選んだ際に呼び出す |
| POST   | /session/reset        | 演出をクリアする                                     |

### POST /challenger/:id/speak

- Path parameters
    - `id`: a または b
- Post Body(`Content-Type: application/x-www-form-urlencoded`)
    - `text`: 発話内容
    - `name`: チャレンジャー名

発話内容の音声データを生成して再生し、LED演出を行う。
再生が終わったらレスポンスする。

### POST /judge/speak

- Path parameters
    - 無し
- Post Body(`Content-Type: application/x-www-form-urlencoded`)
    - `text`: 発話内容

発話内容の音声データを生成して再生し、LED演出を行う。
再生が終わったらレスポンスする。

### POST /judge/select/:id

- Path parameters
    - `id`: a または b
- Post Body(`Content-Type: application/x-www-form-urlencoded`)
    - なし

チャレンジャー選択時のLED演出を行う。
LED演出は `/session/reset` を呼び出すまで継続する。

### POST /session/reset 

- Path parameters
    - なし
- Post Body(`Content-Type: application/x-www-form-urlencoded`)
    - なし

LED演出を終了する。


## Voicevox Style ID

|    キャラクター名    |     Style      | ID  |
| -------------------- | -------------- | --- |
| 四国めたん           | ノーマル       | 2   |
|                      | あまあま       | 0   |
|                      | ツンツン       | 6   |
|                      | セクシー       | 4   |
|                      | ささやき       | 36  |
|                      | ヒソヒソ       | 37  |
| ずんだもん           | ノーマル       | 3   |
|                      | あまあま       | 1   |
|                      | ツンツン       | 7   |
|                      | セクシー       | 5   |
|                      | ささやき       | 22  |
|                      | ヒソヒソ       | 38  |
| 春日部つむぎ         | ノーマル       | 8   |
| 雨晴はう             | ノーマル       | 10  |
| 波音リツ             | ノーマル       | 9   |
| 玄野武宏             | ノーマル       | 11  |
|                      | 喜び           | 39  |
|                      | ツンギレ       | 40  |
|                      | 悲しみ         | 41  |
| 白上虎太郎           | ふつう         | 12  |
|                      | わーい         | 32  |
|                      | びくびく       | 33  |
|                      | おこ           | 34  |
|                      | びえーん       | 35  |
| 青山龍星             | ノーマル       | 13  |
| 冥鳴ひまり           | ノーマル       | 14  |
| 九州そら             | ノーマル       | 16  |
|                      | あまあま       | 15  |
|                      | ツンツン       | 18  |
|                      | セクシー       | 17  |
|                      | ささやき       | 19  |
| もち子さん           | ノーマル       | 20  |
| 剣崎雌雄             | ノーマル       | 21  |
| WhiteCUL             | ノーマル       | 23  |
|                      | たのしい       | 24  |
|                      | かなしい       | 25  |
|                      | びえーん       | 26  |
| 後鬼                 | 人間ver.       | 27  |
|                      | ぬいぐるみver. | 28  |
| No.7                 | ノーマル       | 29  |
|                      | アナウンス     | 30  |
|                      | 読み聞かせ     | 31  |
| ちび式じい           | ノーマル       | 42  |
| 櫻歌ミコ             | ノーマル       | 43  |
|                      | 第二形態       | 44  |
|                      | ロリ           | 45  |
| 小夜/SAYO            | ノーマル       | 46  |
| ナースロボ＿タイプＴ | ノーマル       | 47  |
|                      | 楽々           | 48  |
|                      | 恐怖           | 49  |
|                      | 内緒話         | 50  |
