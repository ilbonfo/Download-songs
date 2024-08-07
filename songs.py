import requests
import base64
import yt_dlp
import re
import os

from tqdm import tqdm
from ID_SECRET import CLIENT_ID, CLIENT_SECRET
from mutagen.easyid3 import EasyID3

PATH = f"C:\\Users\\{os.getlogin()}\\Music\\"


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

    print(f"Downloaded: {title}.mp3")
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


def get_album_tracks(album_id, access_token):
    url = f'https://api.spotify.com/v1/albums/{album_id}/tracks'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        tracks = response.json()['items']
        tracks_info = []
        for track in tracks:
            tracks_info.append(get_track_info(track['id'], access_token))
    else:
        raise Exception(f"Failed to get track info: {response.status_code}")

    return tracks_info


def get_track_info(track_id, access_token):
    inv_char = ('\\', '|', '/', '*', '?', '"', '<', '>', ':')
    url = f'https://api.spotify.com/v1/tracks/{track_id}'
    headers = {
        'Authorization': 'Bearer ' + access_token
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        tracks_info = []
        data = response.json()
        # titolo = data['name']
        titolo = ''.join([char for char in data['name'] if char not in inv_char])
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
        if not os.path.exists(f'{PATH}{titolo}.mp3'):
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
    lista_link = [input("Link: ")]
    while lista_link[-1] != '':
        lista_link.append(input("Link: "))

    access_token = get_access_token(CLIENT_ID, CLIENT_SECRET)
    for link in tqdm(lista_link[:-1]):
        if 'playlist' in link:
            playlist_id = link.split('/')[-1].split('?si=')[0]
            info = get_playlist_tracks(playlist_id, access_token)
            for track in tqdm(info):
                info_mod(track[0])

        elif 'album' in link:
            album_id = link.split('/')[-1].split('?si=')[0]
            info = get_album_tracks(album_id, access_token)

        elif 'track' in link:
            track_id = link.split('/')[-1].split('?si=')[0]
            info = get_track_info(track_id, access_token)
            for track in tqdm(info):
                info_mod(track)
