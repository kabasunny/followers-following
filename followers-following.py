# followers-following\followers-following.py
import os
import csv
import requests
from dotenv import load_dotenv
from datetime import datetime

# 環境変数からトークンをロード
load_dotenv()
TOKEN = os.getenv("GITHUB_API_TOKEN")
BASE_URL = os.getenv("BASE_URL")
USERNAME = os.getenv("GITHUB_USER")

# フォローを外さないユーザーリスト
ALWAYS_FOLLOW_USERS = {"e-shiten-jp"}


def fetch_paginated_data(endpoint, headers):
    """GitHub APIエンドポイントからページング対応でデータを取得"""
    data = []
    page = 1
    while True:
        response = requests.get(f"{endpoint}?per_page=100&page={page}", headers=headers)
        response.raise_for_status()
        page_data = response.json()
        if not page_data:
            break
        data.extend(page_data)
        page += 1
    return data


def get_users(endpoint):
    """ユーザーリストを取得"""
    headers = {"Authorization": f"token {TOKEN}"}
    data = fetch_paginated_data(endpoint, headers)
    return {user["login"] for user in data}


def follow_user(username):
    """ユーザーをフォロー"""
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.put(f"{BASE_URL}/user/following/{username}", headers=headers)
    if response.status_code == 204:
        print(f"Followed: {username}")
        return True
    else:
        print(f"Failed to follow {username}: {response.text}")
        return False


def unfollow_user(username):
    """ユーザーのフォローを解除"""
    headers = {"Authorization": f"token {TOKEN}"}
    response = requests.delete(f"{BASE_URL}/user/following/{username}", headers=headers)
    if response.status_code == 204:
        print(f"Unfollowed: {username}")
        return True
    else:
        print(f"Failed to unfollow {username}: {response.text}")
        return False


def save_to_csv(filename, data, fieldnames):
    """CSVファイルにデータを保存"""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


# 現在の日時を取得し、フォーマット
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# フォロワーとフォローしているリストを取得
followers = get_users(f"{BASE_URL}/users/{USERNAME}/followers")
following_before = get_users(
    f"{BASE_URL}/users/{USERNAME}/following"
)  # 初期のフォローリストを保存

new_follows = []
unfollows = []

# フォローしていないフォロワーユーザーをフォロー
for user in (
    followers - following_before - ALWAYS_FOLLOW_USERS
):  # 初期のフォローリストと比較
    if follow_user(user):
        new_follows.append({"username": user})

# フォロー操作後の更新されたフォローリストを取得
following_after = get_users(
    f"{BASE_URL}/users/{USERNAME}/following"
)  # 更新されたフォローリストを取得

# フォロワーでなくなったユーザーをアンフォロー
for user in (
    following_before - followers
) - ALWAYS_FOLLOW_USERS:  # 初期のフォローリストを新しいフォロワーリストと比較
    if unfollow_user(user):
        unfollows.append({"username": user})

# ファイル名に作成日時を追加して保存
if new_follows:
    new_follows_file = f"new_follows_{timestamp}.csv"
    save_to_csv(new_follows_file, new_follows, fieldnames=["username"])
    print(f"New follows saved to '{new_follows_file}'")

if unfollows:
    unfollows_file = f"unfollows_{timestamp}.csv"
    save_to_csv(unfollows_file, unfollows, fieldnames=["username"])
    print(f"Unfollows saved to '{unfollows_file}'")
