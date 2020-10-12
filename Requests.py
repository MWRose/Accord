import json
from typing import Dict, List, Tuple

REQUEST_KIND_MESSAGE = "message"
REQUEST_KIND_LOGIN = "login"
REQUEST_KIND_INITIATE_CHAT = "initiate"
REQUEST_KIND_BROADCAST = "broadcast"

class Request:
    def __init__(self, data: Dict):
        self.data = data
    
    def is_valid(self) -> bool:
        return "kind" in self.data

    def is_message(self) -> bool:
        return self.is_valid() and self.data["kind"] == REQUEST_KIND_MESSAGE and "sender" in self.data and "recipient" in self.data and "message" in self.data and "iv" in self.data

    def is_login(self) -> bool:
        return self.is_valid() and self.data["kind"] == REQUEST_KIND_LOGIN and "username" in self.data

    def is_initiate_chat(self) -> bool:
        return self.is_valid() and self.data["kind"] == REQUEST_KIND_INITIATE_CHAT and "requester" in self.data and "recipient" in self.data

    def is_broadcast(self) -> bool:
        return self.is_valid() and self.data["kind"] == REQUEST_KIND_BROADCAST and "message" in self.data

def create_request(kind: str, values: List[Tuple[str, str]]) -> bytes:
    data = {
        "kind": kind
    }
    for value in values:
        data[value[0]] = value[1]
    json_data = json.dumps(data, sort_keys=False, indent=2)
    return json_data.encode()

def message(sender: str, recipient: str, msg: str, iv: str) -> bytes:
    values = [("sender", sender), ("recipient", recipient), ("message", msg), ("iv", iv)]
    return create_request(REQUEST_KIND_MESSAGE, values)

def login(username: str) -> bytes:
    values = [("username", username)]
    return create_request(REQUEST_KIND_LOGIN, values)

def initiate_chat(requester: str, recipient: str, encrypted: bytes, signed: bytes) -> bytes:
    values = [("requester", requester), ("recipient", recipient), ("encrypted", encrypted), ("signed", signed)]
    return create_request(REQUEST_KIND_INITIATE_CHAT, values)

def broadcast(message: str) -> bytes:
    values = [("message", message)]
    return create_request(REQUEST_KIND_BROADCAST, values)

def parse_request(request: bytes) -> Request:
    try:
        data = json.loads(request.decode())
        return Request(data)
    except json.JSONDecodeError as e:
        return Request(dict())