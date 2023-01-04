import json
import re
import traceback
from datetime import datetime
from modules import actions
from slack_sdk.errors import SlackApiError
from modules.logger import SlackLogger
from modules.event_parser import EventParser


def listen_event(event, context):
    """SlackのEvents APIを使ってメッセージを監視し、「あとでよむ」が入っていれば1時間後にリマインドする"""
    channel = None
    message_ts = None
    try:
        body = event.get("body")
        print(f"body: {body}")
        body = json.loads(body)

        if "challenge" in body:
            # Slack Events APIの通信確認用メソッドのためにchallengeを返す
            return {"statusCode": 200, "body": json.dumps({"challenge": body.get("challenge")})}

        event = body.get("event")
        if event:
            ep = EventParser(event)
            channel = ep.channel
            message_ts = ep.message_ts
            
            if ep.has_atode:
                ts = datetime.fromtimestamp(float(ep.message_ts))
                now = datetime.utcnow()
                is_recent_message = (now - ts).seconds < 60
                if is_recent_message:
                    print("A target message has been detected")
                    try:
                        actions.react_by_emoji(event)
                        actions.set_reminder(event)
                    except SlackApiError as e:
                        # (1) メッセージが送信される、 (2) そのメッセージのリンクがプレビュー表示される、で同じメッセージのEventが2回来ることがあるのでalready_reactedだったら無視する
                        print(f"Error catched: {e}")
                        if e.response.get("error") != "already_reacted":
                            raise e

        return {"statusCode": 200}
    except Exception as e:
        print(traceback.format_exc())
        SlackLogger.error(func="listen_event", error=e, traceback=traceback.format_exc(), channel=channel, message_ts=message_ts)
        return {"statusCode": 500, "body": "unexpected error"}


def listen_action(event, context):
    """リマインドに対するボタン操作に応じた処理を行う"""
    try:
        body = event.get("body")
        actions.handle_interaction(body)

        return {"statusCode": 200}
    except Exception as e:
        print(traceback.format_exc())
        SlackLogger.error(func="listen_action", error=e, traceback=traceback.format_exc())
        return {"statusCode": 500, "body": "unexpected error"}
