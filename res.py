import requests


n = 1
json  = {"user_id": "1073383604576591974",
    "channel_id": "1100148368996573265",
    "guild_id": "1077968892535775262",
    "query": "zoe azul"}
if n == 1:
    url = requests.post("https://ten-service.onrender.com/play-music", json=json)


print(url.text)
