import os
from slack_sdk import WebClient


class SlackLogger:
    client = WebClient(token=os.environ["SLACK_TOKEN"])
    LOG_OUTPUT_CHANNEL = 'C01F9H3DSCX'
    DEVELOPER_ID = 'URN112HRD'

    @classmethod
    def error(cls, func, error, traceback, channel=None, message_ts=None) -> None:
        url_info = f"URL: {cls.try_extract_url(channel, message_ts)}" if channel and message_ts else ""

        cls.client.chat_postMessage(
            channel=cls.LOG_OUTPUT_CHANNEL,
            text=f"""
<@{cls.DEVELOPER_ID}>
[ERROR] {func} - {error}

{url_info}

```
{traceback}
```
""".strip()
        )


    @classmethod
    def try_extract_url(cls, channel, message_ts):
        message_url = ""
        try:
            response = cls.client.chat_getPermalink(channel=channel, message_ts=message_ts)
            message_url = response.data.get("permalink")
        except Exception as e:
            print(f"[try_extract_url] {e}")
        return message_url
