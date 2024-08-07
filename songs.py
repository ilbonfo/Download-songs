import requests
import base64
import yt_dlp
import re

from tqdm import tqdm
from mutagen.easyid3 import EasyID3

# with open("ID SECRET", 'r') as f:
#     f = f.read().split(',')
#     CLIENT_ID = f[0]
#     CLIENT_SECRET = f[1]
CLIENT_ID = '8b6f403aa7014cb4999288d6c7fef893'
CLIENT_SECRET = '5335d5854d28453bbc818bf595da2acd'
PATH = "C:\\Users\\stebo\\Music\\"


def download_song(title, artist):
    query = f"{title} {artist}"
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{PATH}{title}.%(ext)s',
        'quiet': True,
        'ffmpeg_location': 'D:\\ffmpeg-2024-08-01-git-bcf08c1171-full_build\\bin'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([f"ytsearch1:{query}"])

    print(f"Downloaded and converted to MP3: {title} - {artist}.mp3")
    return f'{PATH}{title}.mp3'


def get_access_token(client_id, client_secret):
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + base64.b64encode((client_id + ':' + client_secret).encode()).decode()
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(url, headers=headers, data=data)
    return response.json()['access_token']


def get_playlist_tracks(playlist_id, access_token):
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        tracks = response.json()['items']
        tracks_info = []
        for track in tracks:
            track_info = track['track']
            tracks_info.append(get_track_info(track_info['id'], access_token))
    else:
        raise Exception(f"Failed to get track info: {response.status_code}")

    return tracks_info


def get_track_info(track_id, access_token):
    inv_char = re.compile(r'\|/*?"<>:')
    url = f'https://api.spotify.com/v1/tracks/{track_id}'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tracks_info = []
        data = response.json()
        titolo = data['name']
        titolo = inv_char.sub('', titolo)
        f = ""
        if len(data['artists']) > 1:
            artista = data['artists'][0]['name']
            feat = [artist['name'] for artist in data['artists'][1:]]
            for a in feat:
                f += a + ', '
            f = f.strip(', ')
        else:
            artista = data['artists'][0]['name']
        album = data['album']['name']
        tracks_info.append((titolo, artista, f, album))
    else:
        raise Exception(f"Failed to get track info: {response.status_code}")

    return tracks_info


def info_mod(info):
    try:
        titolo = info[0]
        artista = info[1]
        feat = info[2]
        album = info[3]
        file = download_song(titolo, artista)
        audio = EasyID3(file)
        audio['albumartist'] = artista
        audio['album'] = album
        audio['title'] = titolo
        audio['artist'] = feat
        audio.save()
    except Exception as e:
        print(e)


while True:
    # lista_link = [input("Link: ")]
    # while lista_link[-1] != '':
    #     lista_link.append(input("Link: "))
    lista_link = ["https://open.spotify.com/playlist/6cal66UTDBHGXtmELAfu76?si=3ed1f7e52fae4360",
                    "Link: https://open.spotify.com/playlist/6puoPusc1CRUDtMla2U80e?si=c7e6cf53806e467d",
                    "Link: https://open.spotify.com/playlist/37i9dQZF1Fa1IIVtEpGUcU?si=04cad88e2a3447ab",
                    "Link: https://open.spotify.com/playlist/37i9dQZF1EpeQIbBqhSG9q?si=43a22f4d7ca64516",
                    "Link: https://open.spotify.com/playlist/37i9dQZF1DZ06evO2sU4ED?si=636563d56d76465a",
                    "Link: https://open.spotify.com/playlist/1r1suTylUOXSUdNC2Ep6QX?si=db73baac24064d56",
                    "Link: https://open.spotify.com/playlist/2vt8lgocuLGSVEJSblEdQx?si=aa3f7566655c439f",
                    "Link: https://open.spotify.com/playlist/37i9dQZF1DZ06evO2zAbsY?si=14be2c67c30b4543",
                    "Link: https://open.spotify.com/playlist/37i9dQZF1DZ06evO0b6iPl?si=02605b3c55114536",
                    "Link: https://open.spotify.com/playlist/3GPi12hegeqHCedgOpLAaE?si=73ab05e2997549b4",
                    "Link: https://open.spotify.com/playlist/58AdN0tSbj5hlRZtqARaLk?si=906c890d78c242d4",
                    "Link: https://open.spotify.com/playlist/2AcAsf54X04oQuBPFqhCjp?si=a7d54a5edb4c48fd",
                    "Link: https://open.spotify.com/playlist/7l6FvVcTBvoLtt8JOAb8kB?si=1b0da6f4078945a7",
                    "Link: https://open.spotify.com/playlist/0ZBIxnLRxlTk7g197TtyAn?si=ee808e6d385049b0",
                    "Link: https://open.spotify.com/playlist/4UCCl8dmpKLRtRqRyBmCJR?si=4993058ad00648cb",
                    "Link: https://open.spotify.com/playlist/37i9dQZF1DZ06evO0Cqn9B?si=dcbb7f48a8874fe2",
                    "Link: https://open.spotify.com/playlist/37i9dQZF1DZ06evO1U2qlO?si=623e7538a1c444b4",
                    "Link: https://open.spotify.com/playlist/37i9dQZF1DZ06evO4qkT7M?si=5cd769fe8c9d44ea",
                    "Link: https://open.spotify.com/playlist/37i9dQZF1DZ06evO2cwh9e?si=b5bf4ab89f2e4b98"]

    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    for link in tqdm(lista_link):
        if 'playlist' in link:
            playlist_id = link.split('/')[-1].split('?si=')[0]
            info = get_playlist_tracks(playlist_id, access_token)
            for track in info:
                info_mod(track[0])
        elif 'track' in link:
            track_id = link.split('/')[-1].split('?si=')[0]
            info = get_track_info(track_id, access_token)
            for track in info:
                info_mod(track)
