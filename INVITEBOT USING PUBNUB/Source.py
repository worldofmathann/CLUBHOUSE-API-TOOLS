import os
import json
import time
import requests
import random
from colorama import Fore, Style, init
init()

header = [
    r"  .___ ___________   ____._________________________ __________ ___________________ ________     _______   ",
    r" |   |\      \   \ /   /|   \__    ___/\_   _____/ \______   \\_____  \__    ___/ \_____  \    \   _  \  ",
    r" |   |/   |   \   Y   / |   | |    |    |    __)_   |    |  _/ /   |   \|    |     /  ____/    /  /_\  \ ",
    r" |   /    |    \     /  |   | |    |    |        \  |    |   \/    |    \    |    /       \    \  \_/   \ ",
    r" |___\____|__  /\___/   |___| |____|   /_______  /  |______  /\_______  /____|    \_______ \ /\ \_____  / ",
    r"             \/                                \/          \/         \/                  \/ \/       \/  ",

    r"<><><><><><><><><><><><<><><><><><><><><><><><><><><><><<><><><><><><><><><><><><><><><><<><><><><><><>",
    r"                 HIGHSPEED INVITE BOT BOT ULTIMATE EDITION WITH AUTOUPDATE FEATURE V2.0",
    r"       CH Username: @_worldofmathan                           Telegram Username: @worldofmathan",
    r"                         Telegram Group Link : https://t.me/clubhouseapps",
    r"<><><><><><><><><><><><<><><><><><><><><><><><><><><><><<><><><><><><><><><><><><><><><><<><><><><><><>"

]

print(f"{Fore.RED}{header[0]}")
print(f"{Fore.GREEN}{header[1]}")
print(f"{Fore.YELLOW}{header[2]}")
print(f"{Fore.BLUE}{header[3]}")
print(f"{Fore.MAGENTA}{header[4]}")
print(f"{Fore.CYAN}{header[5]}")
print(f"{Fore.LIGHTBLUE_EX}{header[6]}")
print(f"{Fore.LIGHTCYAN_EX}{header[7]}")
print(f"{Fore.LIGHTCYAN_EX}{header[8]}")
print(f"{Fore.LIGHTCYAN_EX}{header[9]}")
print(f"{Fore.LIGHTBLUE_EX}{header[10]}")
print(Style.RESET_ALL)


URL_JOIN_CHANNEL = "https://www.clubhouseapi.com/api/join_channel"
URL_SEND_MESSAGE = "https://www.clubhouseapi.com/api/send_channel_message"
URL_INV = "https://www.clubhouseapi.com/api/invite_speaker"

HEAD1 = {'Authorization': 'Token <HELPER TOKEN HERE>'}
HEAD2 = {'Authorization': 'Token <HELPER TOKEN HERE>'}


EMOJI_CONFIG_PATH = os.path.join(os.getcwd(), "Emoji_Config")
PICKUPLINE_CONFIG_PATH = os.path.join(os.getcwd(), "Pickuplines_Config")

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} not found, creating it...")
        os.makedirs(folder_path)

def create_file_if_not_exists(file_path, default_content=""):
    if not os.path.exists(file_path):
        print(f"File {file_path} not found, creating it...")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(default_content)

create_folder_if_not_exists(EMOJI_CONFIG_PATH)
create_folder_if_not_exists(PICKUPLINE_CONFIG_PATH)

emoji1_file = os.path.join(EMOJI_CONFIG_PATH, "Emoji1.txt")
emoji2_file = os.path.join(EMOJI_CONFIG_PATH, "Emoji2.txt")
pline1_file = os.path.join(PICKUPLINE_CONFIG_PATH, "PLine1.txt")
pline2_file = os.path.join(PICKUPLINE_CONFIG_PATH, "PLine2.txt")

create_file_if_not_exists(emoji1_file, "😊\n😎\n😂\n🥺\n💀")
create_file_if_not_exists(emoji2_file, "😍\n🥰\n🤩\n😅\n🤡")
create_file_if_not_exists(pline1_file, "Are you a magician?\nDo you have a map?\nIs your name Google?")
create_file_if_not_exists(pline2_file, "Because when I look at you, I see magic.\nBecause I keep getting lost in your eyes.\nBecause you’ve got everything I’m searching for.")

path = os.getenv('Appdata')
filename = os.path.join(path, 'Clubdeck', 'profile.json')
is_existing = os.path.exists(filename)

if is_existing:
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
        usertoken = data.get('token')
        user_idcd = data.get('userId')
else:
    print("Please login properly on Clubdeck.")
    exit()

exclusion_list = [user_idcd]
processed_users = set()

def extract_social_club_id_and_get_channel(usertoken):
    url = "https://www.clubhouseapi.com/api/get_feed_v3"
    headers = {'Authorization': 'Token ' + usertoken}
    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['items'][0]['channel']['channel']
    except requests.exceptions.RequestException as e:
        print(f"Error getting channel: {e}")
        return None

def invite_speaker(profile_user_id, name, channel_id, usertoken):
    headers = {'Authorization': 'Token ' + usertoken}
    data = {"channel": channel_id, "user_id": profile_user_id}
    response = requests.post(URL_INV, headers=headers, json=data)
    if response.status_code == 200:
        print(f"* {name} ({profile_user_id}) Successfully Invited.")
        send_channel_message(usertoken, channel_id, message_type, name)
    else:
        print(f"Failed to send invitation to user {name} ({profile_user_id}). Status code: {response.status_code}")

def send_channel_message(usertoken, channel_id, message_type, name):
    """Send a message to the channel with user details."""
    headers = {'Authorization': 'Token ' + usertoken}
    if message_type == "emoji":
        try:
            with open(emoji1_file, "r", encoding="utf-8") as file1, \
                    open(emoji2_file, "r", encoding="utf-8") as file2:
                emojis1 = file1.read().splitlines()
                emojis2 = file2.read().splitlines()
                emoji1 = random.choice(emojis1)
                emoji2 = random.choice(emojis2)
                message = f" {emoji1} {name} {emoji2} "
        except FileNotFoundError as e:
            print(f"Error: {e}")
            message = f"Sorry, no emojis available for {name}."

    elif message_type == "pickup_line":
        try:
            with open(pline1_file, "r", encoding="utf-8") as file1, \
                    open(pline2_file, "r", encoding="utf-8") as file2:
                pline1 = file1.read().splitlines()
                pline2 = file2.read().splitlines()
                message = f"{random.choice(pline1)} {name} {random.choice(pline2)}"
        except FileNotFoundError as e:
            print(f"Error: {e}")
            message = f"Sorry, no pickup lines available for {name}."

    data = {
        "channel": channel_id,
        "message": message
    }
    response = requests.post(URL_SEND_MESSAGE, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Message sent: {message}")
    else:
        handle_rate_limit(response, data)

def handle_rate_limit(response, data):
    if response.status_code == 429:
        print('Joining the helper bot-1....')
        join_bot1 = requests.post(URL_JOIN_CHANNEL, data=data, headers=HEAD1)
        print('Helper bot-1 Status:', join_bot1.status_code)

        response2 = requests.post(URL_SEND_MESSAGE, data=data, headers=HEAD1)
        if response2.status_code == 200:
            print('Helper Bot-1 Message status:', response2.text)
        elif response2.status_code == 429:
            print('Joining the helper bot-2....')
            join_bot2 = requests.post(URL_JOIN_CHANNEL, data=data, headers=HEAD2)
            print('Helper bot-2 Status:', join_bot2.status_code)

            response3 = requests.post(URL_SEND_MESSAGE, data=data, headers=HEAD2)
            if response3.status_code == 200:
                print('Helper Bot-2 Message Status:', response3.text)
            else:
                time.sleep(1)
        else:
            time.sleep(1)
    else:
        print('Invite Failed due to too many users, pausing application for 5 seconds')
        time.sleep(5)
def handle_pubnub_response(response_json, usertoken, channel_id):
    try:
        if 'm' in response_json and response_json['m']:
            filtered_data = response_json['m'][0].get('d', {})
            action = filtered_data.get('action')
            user_id = filtered_data.get('user_id')
            if action == 'join_channel':
                user_profile = filtered_data.get('user_profile', {})
                name = user_profile.get('name')
                profile_user_id = user_profile.get('user_id')
                is_speaker = user_profile.get('is_speaker', False)
                is_invited_as_speaker = user_profile.get('is_invited_as_speaker', False)
                if not is_speaker and not is_invited_as_speaker and profile_user_id not in processed_users:
                    processed_users.add(profile_user_id)
                    invite_speaker(profile_user_id, name, channel_id, usertoken)

    except KeyError as e:
        print(f"Key error: {e} not found in the response.")
    except Exception as e:
        print(f"An error occurred: {e}")

def pubnub_loop(channel_id, pubnub_token, headers):
    """Manage continuous listening for PubNub messages based on the user's choice."""
    tt = 0
    while True:
        pubnub_url = f"https://clubhouse.pubnubapi.com/v2/subscribe/sub-c-a4abea84-9ca3-11ea-8e71-f2b83ac9263d/channel_all.{channel_id}/0?heartbeat=300&tt={tt}&tr=31&uuid=877267097&pnsdk=PubNub-JS-Web%2F7.3.0&auth={pubnub_token}"
        try:
            pubnub_response = requests.get(pubnub_url, headers=headers)
            pubnub_response.raise_for_status()
            response_json = pubnub_response.json()
            handle_pubnub_response(response_json, usertoken, channel_id)
            tt = response_json.get("t", {}).get("t", tt)
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"Error in PubNub loop: {e}")
            break
        time.sleep(0)

def join_channel(channel_id):
    headers = {'Authorization': 'Token ' + usertoken}
    if not usertoken:
        print("Unable to join the channel. Please check your login.")
        return
    try:
        data = {"channel": channel_id}
        response = requests.post(URL_JOIN_CHANNEL, headers=headers, json=data)
        response.raise_for_status()
        response_json = response.json()

        pubnub_token = response_json.get('pubnub_token')
        if pubnub_token:
            pubnub_loop(channel_id, pubnub_token, headers)
        else:
            print("Failed to retrieve PubNub token.")
    except requests.exceptions.RequestException as e:
        print(f"Error joining channel: {e}")

if __name__ == "__main__":
    print("Choose a mode:\n1. Invite Only\n2. Room Chat Only\n3. Invite and Room Chat")
    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        mode = "invite_only"
        print(f"User selected: {mode}")
    elif choice == "2":
        mode = "roomchat_only"
        print(f"User selected: {mode}")
    elif choice == "3":
        mode = "invite_and_roomchat"
        print(f"User selected: {mode}")
    else:
        print("Invalid choice. Exiting...")
        exit()

    print("Choose message type:\n1. Emoji mode\n2. Pickup line mode")
    message_choice = input("Enter your choice (1/2): ")

    if message_choice == "1":
        message_type = "emoji"
        print(f"User selected: {message_type}")
    elif message_choice == "2":
        message_type = "pickup_line"
        print(f"User selected: {message_type}")
    else:
        print("Invalid choice for message type.")
        exit()
    print("Please leave and rejoin the channel to run this application")
    channel_id = extract_social_club_id_and_get_channel(usertoken)
    if channel_id:
        join_channel(channel_id)
