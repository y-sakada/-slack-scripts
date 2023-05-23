import csv
import requests

def get_user_display_name(user_id, token):
    url = "https://slack.com/api/users.profile.get"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    params = {
        "user": user_id,
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    display_name = ''

    if data["ok"]:
        display_name = data["profile"]["display_name"]
    
    return display_name

def get_user_open_channels(user_id, token):
    url = "https://slack.com/api/users.conversations?types=public_channel&user={user_id}"
    headers = {
        "Authorization": f"Bearer {token}",
    }

    params = {
        "user": user_id,
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    channels = []

    if data["ok"]:
        channels = data["channels"]
    
    return channels

def write_channels_to_csv(channels, display_name):
    filename = f"{display_name}_channels.csv"
    with open(filename, mode='w', newline='', encoding='utf-8-sig') as file:
        writer = csv.writer(file)
        writer.writerow(["Channel ID", "Channel Name"])  # CSV header
        for channel in channels:
            writer.writerow([channel["id"], channel["name"]])  # Write both channel id and name

# CSVファイルからユーザーIDを読み取る
user_ids = []
with open("user_ids.csv", newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        user_ids.extend(row)

# APIトークンを設定
token = 'TOKEN'

# 各ユーザーのオープンチャンネルの一覧を取得し、CSVに書き込む
for user_id in user_ids:
    display_name = get_user_display_name(user_id, token)
    channels = get_user_open_channels(user_id, token)
    write_channels_to_csv(channels, display_name)
