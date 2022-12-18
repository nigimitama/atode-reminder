import json
import re
import os
from base64 import b64decode
from urllib.parse import unquote
from datetime import datetime, timedelta
from slack_sdk import WebClient
from slack_sdk.web.slack_response import SlackResponse
TIME_DELTA = timedelta(hours=1)


def set_reminder(event: dict) -> SlackResponse:
    client = WebClient(token=os.environ["SLACK_TOKEN"])

    # calc timestamp
    event_ts = float(event["event_ts"])
    event_time: datetime = datetime.fromtimestamp(event_ts) + TIME_DELTA

    # get message URL
    response: SlackResponse = client.chat_getPermalink(channel=event["channel"], message_ts=event["ts"])
    message_url: str = response.data.get("permalink")

    # set reminder
    return client.chat_scheduleMessage(
        channel=event["channel"],
        text="",
        post_at=int(event_time.timestamp()),
        blocks=_gen_blocks(message_url)
    )


def react_by_emoji(event: dict) -> SlackResponse:
    client = WebClient(token=os.environ["SLACK_TOKEN"])
    return client.reactions_add(
        channel=event["channel"],
        name="eyes",
        timestamp=event["ts"]
    )


def handle_interaction(body: str) -> SlackResponse:
    client = WebClient(token=os.environ["SLACK_TOKEN"])
    body = _parse_interaction_payloads(body)
    print(f"body: {body}")
    print(f"actions: {body['actions']}")
    print(f"message: {body['message']}")

    action = body["actions"][-1]
    if action["value"] == "done":
        blocks = [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"> {buttons['done']}\nお疲れ様でした！",
            }
        }]
        return client.chat_update(
            channel=body["channel"]["id"],
            blocks=json.dumps(blocks),
            ts=body["message"]["ts"]
        )

    if action["value"] == "remind":
        # calc timestamp
        action_ts = float(action["action_ts"])
        action_time: datetime = datetime.fromtimestamp(action_ts) + TIME_DELTA

        # estimate url
        try:
            message_url = body["message"]["attachments"][0]["original_url"]
        except KeyError:
            message_url = re.search(r"<(?P<url>http.+)>", body["message"]["blocks"]["text"]["text"]).group("url")

        client.chat_scheduleMessage(
            channel=body["channel"]["id"],
            text="",
            post_at=int(action_time.timestamp()),
            blocks=_gen_blocks(message_url)
        )

        blocks = [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"> {buttons['remind']}\nまたリマインドします！",
            }
        }]
        return client.chat_update(
            channel=body["channel"]["id"],
            blocks=json.dumps(blocks),
            ts=body["message"]["ts"]
        )

def _parse_interaction_payloads(body: str) -> dict:
    # ボタンを押したときにPOSTされるデータはbase64のurlencodeなのでデコードしてパースする
    body = b64decode(body).decode("ascii")
    body = unquote(body)
    return json.loads(body.replace("payload=", ""))


buttons = {
    "done": "読んだ！",
    "remind": "また1時間後にリマインド"
}


def _gen_blocks(message_url: str) -> str:
    text=f"""
読みましたか…？

{message_url}
""".strip()
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text,
            }
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": buttons["done"],
                    },
                    "style": "primary",
                    "value": "done",
                    "action_id": "actionId-0"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": buttons["remind"],
                    },
                    "value": "remind",
                    "action_id": "actionId-1"
                }
            ]
        }
    ]
    return json.dumps(blocks)
