import os
import json
from typing import Optional
from modules import requests


class SlackApiError(Exception):
    pass


HEADERS = {
    "Content-type": "application/json",
    "Authorization": f"Bearer {os.environ['SLACK_TOKEN']}"
}


def schedule_message(channel: str, text: str, post_at: int, blocks: Optional[str] = None) -> None:
    url = "https://slack.com/api/chat.scheduleMessage"
    data = {
        "channel": channel,
        "text": text,
        "post_at": post_at,
    }
    if blocks:
        data["blocks"] = blocks

    response = requests.post(url, data, HEADERS)
    body = json.loads(response.body)
    if body["ok"] != True:
        raise SlackApiError(f"[schedule_message] failed. response={response}")


def reactions_add(channel: str, emoji_name: str, timestamp: str) -> None:
    url = "https://slack.com/api/reactions.add"
    data = {
        "channel": channel,
        "name": emoji_name,
        "timestamp": timestamp,
    }
    response = requests.post(url, data, HEADERS)
    body = json.loads(response.body)
    if body["ok"] != True:
        raise SlackApiError(f"[reactions_add] failed. response={response}")


def get_permalink(channel: str, message_ts: str) -> str:
    """メッセージのURLを取得する"""
    url = "https://slack.com/api/chat.getPermalink"
    data = {
        "channel": channel,
        "message_ts": message_ts,
    }
    response = requests.get(url, data, HEADERS)
    body = json.loads(response.body)
    if body["ok"] != True:
        raise SlackApiError(f"[get_permalink] failed. response={response}")

    return body["permalink"]


def update_message(channel: str, ts: str, blocks: Optional[str] = None) -> None:
    url = "https://slack.com/api/chat.update"
    data = {
        "channel": channel,
        "ts": ts
    }
    if blocks:
        data["blocks"] = blocks

    response = requests.post(url, data, HEADERS)
    body = json.loads(response.body)
    if body["ok"] != True:
        raise SlackApiError(f"[update_message] failed. response={response}")
