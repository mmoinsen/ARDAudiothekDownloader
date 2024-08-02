import urllib.request
import requests
from bs4 import BeautifulSoup
import json
import urllib
import os
from pathlib import Path



# url = 'https://www.ardaudiothek.de/sendung/example' Hier URL des Podcast einfügen

embedded_url = ""
ep_name = ""
raw_json =""

response_main = requests.get(url)
soup_main = BeautifulSoup(response_main.text, 'html.parser')
twt_tag = soup_main.find(attrs={"name":"twitter:player"})
embedded_url = twt_tag.get('content')
response_embedded = requests.get(embedded_url)
soup_embedded = BeautifulSoup(response_embedded.text,'html.parser')
embedded_script = soup_embedded.find('script', {'type':'application/json'})
filtered_script = []
for raw_json in embedded_script:
    if embedded_script.get('id') == '__NEXT_DATA__' and embedded_script.get('type') == 'application/json':
        continue 
    filtered_script.append(raw_json)

json_file = json.loads(raw_json)
file_extention = '.mp3'
episoden_titel = json_file['props']['pageProps']['initialData']['title']
download_url = json_file['props']['pageProps']['initialData']['audios'][0]['downloadUrl']
final_url = download_url.split("/")[-1]

mp3 = urllib.request.urlopen(download_url)
with open (final_url, 'wb') as output:
    output.write(mp3.read())

alter_pfad = os.path.basename(final_url)
neuer_name = episoden_titel.replace(":", "-").replace("\"", "").replace("/", "-")
neuer_name = ''.join(char for char in neuer_name if char.isalnum() or char in (' ', '-', '_')).rstrip()
neuer_name = f'{neuer_name}.mp3'

neuer_pfad = neuer_name

if os.path.exists(alter_pfad):
    os.rename(alter_pfad,neuer_pfad)


if twt_tag:
    print (episoden_titel)
    print(download_url)
    
else:
    print("Fehler, keine embedded URL gefunden!")

