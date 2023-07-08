from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
load_dotenv()

CID = os.getenv('yes')
SC = os.getenv('no')

def get_token():
    auth_string = CID + ':' + SC
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes),'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': 'Basic ' + auth_base64,
        'Content-Type': 'application/x-www-form-urlencoded'

    }
    data = {'grant_type' : 'client_credentials'}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token

def get_auth_headers(token):
    return {'Authorization': 'Bearer ' + token}

def search_artist(token, artist_name):
    url = 'https://api.spotify.com/v1/search'
    headers = get_auth_headers(token)
    query = f'?q={artist_name}&type=artist&limit=1'

    query_url = url + query
    result = get(query_url, headers = headers)
    json_result = json.loads(result.content)['artists']['items']
    if len(json_result)==0:
        print('This name does not exist!')
        return None
    else:
        return json_result[0]

def get_song(token,ID):
    url = f'https://api.spotify.com/v1/artists/{ID}/top-tracks?country=US'  

    headers = get_auth_headers(token)
    result = get(url, headers= headers)
    json_result = json.loads(result.content)['tracks']
    return json_result

def get_song_in_album(token, ID):
    url = f'https://api.spotify.com/v1/albums/{ID}/tracks'  
    headers = get_auth_headers(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return json_result

token = get_token()


result = search_artist(token, 'Keshi')
if result is not None:
    ID = result['id']

    # Get the top tracks of the artist
    top_tracks = get_song(token, ID)

    if len(top_tracks) > 0:
        # Get the top album of the artist
        top_album_id = top_tracks[0]['album']['id']

        # Get the tracks of the top album
        album_tracks = get_song_in_album(token, top_album_id)

        if len(album_tracks) > 0:
            print(f"Top Songs in the Top Album of {result['name']}:")

            # Iterate over the tracks and print their names
            for i, song in enumerate(album_tracks['items']):
                print(f"{i+1}. {song['name']}")


# ID = result['id']
# songohhh = get_song(token,ID)
# get_album_song= get_song_in_album(token,ID)
# print(get_album_song)
# print(songohhh)


# for i, song in enumerate(songohhh):
#     print(f'{i+1}.{song["name"]}')
