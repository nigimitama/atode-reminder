import json
import re
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
            if re.match(r".*(あと|後)で(よむ|読む|みる|見る)", event["text"]):
                actions.react_by_emoji(event)
                actions.set_reminder(event)
                return {"statusCode": 200}
        
        return {"statusCode": 200}
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": "unexpected error"}
