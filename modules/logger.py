import os
from slack_sdk import WebClient


class SlackLogger:
    client = WebClient(token=os.environ["SLACK_TOKEN"])
    LOG_OUTPUT_CHANNEL = 'C01F9H3DSCX'
    DEVELOPER_ID = 'URN112HRD'

    @classmethod
    def error(cls, func, error, traceback) -> None:
        cls.client.chat_postMessage(
            channel=cls.LOG_OUTPUT_CHANNEL,
            text=f"""
<@{cls.DEVELOPER_ID}>
[ERROR] {func} - {error}

```
{traceback}
```
""".strip()
        )
