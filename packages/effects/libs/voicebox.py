import requests
import urllib.parse
import simpleaudio

url = "http://localhost:50021"

def vv_resuqest_speach(text):
    endoced_text = urllib.parse.quote(text)
    query = requests.post(url + "/audio_query?speaker=1&"+endoced_text) # get query json
    audio_data = requests.post(url + "/synthesis", data=query) # get audio data
    wave_obj = simpleaudio.WaveObject(audio_data, 2, 2, 44100)
    play_obj = wave_obj.play()
    # play_obj.wait_done()

# # 再生中か確認する
# if play_obj.is_playing():
#     print("still playing")