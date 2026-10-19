import requests
import time
import re
import json
import re
import sys
import os

token = ""

url = 'https://www.clubhouseapi.com/api/'

headers = {'Authorization': f'Token {token}'}

def social_club_id(token):
    try:
        url = 'https://www.clubhouseapi.com:443/api/get_social_club'
        response = requests.post(url, headers=headers, json=json)
        data = response.json()
        clubid = data['social_club']['social_club_id']
        club_name = data['social_club']['name']
        members_count = data['social_club']['num_members']
        founder_name = data['social_club']['founder_name']
        print(f'House Name: {club_name}')
        print(f'Members Count: {members_count}')
        print(f'House Founder Name: {founder_name}')
        return (clubid, club_name)
    except Exception as e:
        print(f'Error occurred: {e}')
        time.sleep(1)


def create_channel(token, clubid, topic):
     payload = {
        'is_social_mode': False,
        'is_private': False,
        "privacy_level": "house",
        'user_ids': [],
        'club_id': None,
        'social_club_id': clubid,
        'chat_id': None,
        'topic': topic,
        'game_id': None,
        'is_replay_enabled': is_replay_enabled,
        'is_public_club_room': True,
        'language': 'en',
        'handraise_permission': 1,
        'topic_ids': [],
        'is_chat_enabled': True,
        'link': None,
        'source': 49
    }
    api_url = url + 'create_channel'
    resp = requests.request('POST', api_url, json=payload, headers=headers)
    response_json = resp.json()
    return response_json['channel']

def active_ping(token, channel_id):
    payload = {'channel': channel_id}
    api_url = url + 'active_ping'
    resp = requests.request('POST', api_url, json=payload, headers=headers)
    print(resp.text)

profile_URL = input("Enter House link (or 'exit' to quit): ")
if profile_URL.lower() == 'exit':
    sys.exit()
link = profile_URL
club_id = re.search('/house/(.+)$', link).group(1)
json = {'social_club_slug': f'{club_id}'}
clubid, name = social_club_id(token)
topic1 = input('Enter room Title-1: ')
topic2 = input('Enter room Title-2: ')
topic3 = input('Enter room Title-3: ')
topic4 = input('Enter room Title-4: ')
topic5 = input('Enter room Title-5: ')
channel1 = create_channel(token, clubid, topic1)
channel2 = create_channel(token, clubid, topic2)
channel3 = create_channel(token, clubid, topic3)
channel4 = create_channel(token, clubid, topic4)
channel5 = create_channel(token, clubid, topic5)

while True:
    print('Channels Created Successfully............')
    active_ping(token, channel1)
    active_ping(token, channel2)
    active_ping(token, channel3)
    active_ping(token, channel4)
    active_ping(token, channel5)
    print('Please Join the channels with Clubdeck and close the Script............')
    time.sleep(15)
