import json
import re
import traceback
from datetime import datetime, timedelta
from modules import actions


def bot(event, context):
    """SlackのEvents APIを使ってメッセージを監視し、「あとでよむ」が入っていれば1時間後にリマインドする"""
    try:
        body = event.get("body")
        print(f"body: {body}")
        body = json.loads(body)

        if "challenge" in body:
            # Slack Events APIの通信確認用メソッドのためにchallengeを返す
            return {"statusCode": 200, "body": json.dumps({"challenge": body.get("challenge")})}

        event = body.get("event")
        if event.get("type") == "message":
            if re.match(r".*(あと|後)で(よ|読|み|見)", event["text"]) or re.match(r".*atode", event["text"]):
                ts = datetime.fromtimestamp(float(event["ts"]))
                now = datetime.utcnow()
                is_recent_message = (now - ts).seconds < 60
                if is_recent_message:
                    print("A target message has been detected")
                    actions.react_by_emoji(event)
                    actions.set_reminder(event)

        return {"statusCode": 200}
    except Exception as e:
        print(traceback.format_exc())
        return {"statusCode": 500, "body": "unexpected error"}
