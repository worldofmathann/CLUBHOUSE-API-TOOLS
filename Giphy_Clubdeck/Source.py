import requests
import json
import os
import time


path = os.getenv('Appdata')
filename = os.path.join(path, 'Clubdeck', 'profile.json')

isExisting = os.path.exists(filename)

if isExisting:
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        token = data.get('token')
        botname = data['user']['name']
        print(f'\nWelcome << {botname} >> is Syncing...')
else:
    print("Please login properly on Clubdeck.")

api = "https://www.clubhouseapi.com:443/api/"

def extract_user_id_and_channel_id(token):
    action = "get_feed_v3"
    url = api + action
    headers = {'Authorization': 'Token ' + token }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        channel_id = data['items'][1]['channel']['channel']
        return channel_id
    except requests.exceptions.RequestException as e:
        print("Error: Failed to retrieve channel ID.")
        return None

channel_id = extract_user_id_and_channel_id(token)

def send_gif_reaction(api, action, channel_id, giphy_id, token):
    url = api + action
    data = {
        "channel": channel_id,
        "giphy_id": giphy_id
    }
    headers = {'Authorization': 'Token ' + token}

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        print("Gif Reacted Successfully:", response)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def gif_play(action, giphy_id_file, token, channel_id):
    api = "https://www.clubhouseapi.com:443/api/"
    with open(giphy_id_file, 'r') as f:
        giphy_ids = f.read().splitlines()
    for giphy_id in giphy_ids:
        send_gif_reaction(api, action, channel_id, giphy_id, token)
        time.sleep(22)

action = "gif_reaction"
giphy_id_file = "giphy.txt"


while True:
    gif_play(action, giphy_id_file, token, channel_id)
