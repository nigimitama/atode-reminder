import json
import re
from base64 import b64decode
from urllib.parse import unquote
from datetime import datetime, timedelta
from modules import slack
TIME_DELTA = timedelta(hours=1)


def set_reminder(event: dict):
    # calc timestamp
    event_ts = float(event["event_ts"])
    event_time: datetime = datetime.fromtimestamp(event_ts) + TIME_DELTA

    # get message URL
    message_url = slack.get_permalink(channel=event["channel"], message_ts=event["ts"])

    # set reminder
    return slack.schedule_message(
        channel=event["channel"],
        text="",
        post_at=int(event_time.timestamp()),
        blocks=_gen_blocks(message_url)
    )


def react_by_emoji(event: dict):
    return slack.reactions_add(
        channel=event["channel"],
        emoji_name="eyes",
        timestamp=event["ts"]
    )


def handle_interaction(body: str):
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
                "text": "お疲れ様でした！",
            }
        }]
        return slack.update_message(
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

        slack.schedule_message(
            channel=body["channel"]["id"],
            text="",
            post_at=int(action_time.timestamp()),
            blocks=_gen_blocks(message_url)
        )

        blocks = [{
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "またリマインドします！",
            }
        }]
        return slack.update_message(
            channel=body["channel"]["id"],
            blocks=json.dumps(blocks),
            ts=body["message"]["ts"]
        )

def _parse_interaction_payloads(body: str) -> dict:
    # ボタンを押したときにPOSTされるデータはbase64のurlencodeなのでデコードしてパースする
    body = b64decode(body).decode("ascii")
    body = unquote(body)
    return json.loads(body.replace("payload=", ""))



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
                        "text": "読んだ！",
                    },
                    "style": "primary",
                    "value": "done",
                    "action_id": "actionId-0"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "また1時間後にリマインド",
                    },
                    "value": "remind",
                    "action_id": "actionId-1"
                }
            ]
        }
    ]
    return json.dumps(blocks)
