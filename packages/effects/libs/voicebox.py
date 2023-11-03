import requests
import urllib.parse
# import simpleudio

url = "http://localhost:50021"

def vv_request_speech(text):
    endoced_text = urllib.parse.quote(text)
    query = requests.post(url + "/audio_query?speaker=3&text="+endoced_text) # get query json
    if query.status_code != 200:
        raise Exception(query.text)
    audio_data = requests.post(url + "/synthesis?speaker=3", data=query.text) # get audio data
    # wave_obj = simpleaudio.WaveObject(audio_data, 2, 2, 44100)
    # play_obj = wave_obj.play()
    # play_obj.wait_done()

# # 再生中か確認する
# if play_obj.is_playing():
#     print("still playing")