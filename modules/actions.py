from datetime import datetime, timedelta
from modules import slack


def set_reminder(event: dict, delta: timedelta = timedelta(hours=1)):
    # calc timestamp
    event_ts = float(event["event_ts"])
    event_time: datetime = datetime.fromtimestamp(event_ts) + delta

    # get message URL
    message_url = slack.get_permalink(channel=event["channel"], message_ts=event["ts"])

    # set reminder
    response = slack.schedule_message(
        channel=event["channel"],
        text=f"""
読みましたか…？

{message_url}
""".strip(),
        post_at=int(event_time.timestamp())
    )
    return response


def react_by_emoji(event: dict):
    return slack.reactions_add(
        channel=event["channel"],
        emoji_name="eyes",
        timestamp=event["ts"]
    )
