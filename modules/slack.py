import os
import json
from modules import requests


class SlackApiError(Exception):
    pass


HEADERS = {
    "Content-type": "application/json",
    "Authorization": f"Bearer {os.environ['SLACK_TOKEN']}"
}


def schedule_message(channel: str, text: str, post_at: int):
    url = "https://slack.com/api/chat.scheduleMessage"
    data = {
        "channel": channel,
        "text": text,
        "post_at": post_at,
    }
    response = requests.post(url, data, HEADERS)
    body = json.loads(response.body)
    if body["ok"] != True:
        raise SlackApiError(f"[schedule_message] failed. response={response}")


def reactions_add(channel: str, emoji_name: str, timestamp: str):
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
