import unittest
from modules.event_parser import EventParser


class TestStringMethods(unittest.TestCase):

    def test_parse_message(self):
        # message
        body = {
            "event": {
                "type": "message",
                "user": "USER_ID",
                "text": "<https://arxiv.org/abs/2211.16298>\nあとで読む",
                "ts": "1671764657.864739",
                "blocks": [],
                "channel": "CHANNEL_ID",
                "event_ts": "1671764657.864739",
                "channel_type": "channel"
            },
            "type": "event_callback",
            "event_id": "Ev04H4QMLQE4",
            "event_time": 1671764657,
        }
        ep = EventParser(body["event"])
        self.assertEqual(ep.user, body["event"]["user"])
        self.assertEqual(ep.channel, body["event"]["channel"])
        self.assertEqual(ep.message_ts, body["event"]["ts"])
        self.assertEqual(ep.text, body["event"]["text"])

    def test_parse_message_changed(self):
        # edited message
        body = {
            "event": {
                "type": "message",
                "subtype": "message_changed",
                "message": {
                    "type": "message",
                    "user": "USER_ID",
                    "text": "<https://arxiv.org/abs/2211.16298>\nあとで読む",
                    "blocks": [],
                    "attachments": [],
                    "ts": "1671716972.091629"
                },
                "previous_message": {},
                "channel": "CHANNEL_ID",
                "hidden": True,
                "ts": "1671716972.000200",
                "event_ts": "1671716972.000200",
                "channel_type": "channel"
            },
            "type": "event_callback",
            "event_time": 1671716972,
        }
        ep = EventParser(body["event"])
        self.assertEqual(ep.user, body["event"]["message"]["user"])
        self.assertEqual(ep.channel, body["event"]["channel"])
        self.assertEqual(ep.message_ts, body["event"]["message"]["ts"])
        self.assertEqual(ep.text, body["event"]["message"]["text"])

    def test_has_atode(self):
        self.assertEqual(
            EventParser._has_atode("<https://arxiv.org/abs/2211.16298>\nあとで読む"),
            True
        )
        self.assertEqual(
            EventParser._has_atode("あとで読む\n<https://arxiv.org/abs/2211.16298>"),
            True
        )


if __name__ == '__main__':
    unittest.main()
