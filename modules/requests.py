from typing import Any
from dataclasses import dataclass
import urllib.request
import json


@dataclass
class Response:
    status_code: int
    body: Any


def post(url: str, data: Any, headers: dict) -> Response:
    request = urllib.request.Request(url, json.dumps(data).encode(), headers)
    try:
        with urllib.request.urlopen(request) as res:
            body = res.read()
            body = body.decode() if type(body) == bytes else body
            status_code = 200
    except urllib.error.HTTPError as err:
        status_code = err.code
        body = None
    except urllib.error.URLError as err:
        status_code = None
        body = err.reason
    return Response(status_code, body)
