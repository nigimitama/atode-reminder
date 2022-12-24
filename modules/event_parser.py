import re


class EventParser:
    """SlackのEvent APIが送ってくるJSONをパースして「後で読む」のような文字列を探す"""
    def __init__(self, event: dict) -> None:
        self.user = None
        self.channel = None
        self.message_ts = None
        self.event = event
        self.has_atode = False
        self._parse(event)

    def _parse(self, event: dict) -> None:
        self.channel = event.get("channel")

        if event["type"] != "message":
            return None

        if event.get("subtype") == "message_changed":
            message = event.get("message")
        else:
            message = {key: event.get(key) for key in ["ts", "text", "user"]}

        self.user = message.get("user")
        self.message_ts = message.get("ts")
        self.text = message.get("text")
        self.has_atode = self._has_atode(self.text)

    @classmethod
    def _has_atode(self, text: str) -> bool:
        if re.match(r"(.|\n)*(あと|後)で(よ|読|み|見).*", text) or re.match(r".*atode", text):
            return True
        return False
