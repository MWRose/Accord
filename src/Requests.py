import json
from typing import Dict, List, Tuple

REQUEST_KIND_DIRECT_MESSAGE = "direct_message"
REQUEST_KIND_GROUP_MESSAGE = "group_message"
REQUEST_KIND_LOGIN = "login"
REQUEST_KIND_INITIATE_DIRECT_MESSAGE = "initiate_direct"
REQUEST_KIND_INITIATE_GROUP_CHAT = "initiate_group"
REQUEST_KIND_BROADCAST = "broadcast"

class Request:
    def __init__(self, data: Dict):
        self.data = data
    
    def is_valid(self) -> bool:
        return "kind" in self.data

    def __is_message(self) -> bool:
        # TODO Format the line
        return self.is_valid() and "sender" in self.data and  "message" in self.data and "iv" in self.data and "tag" in self.data

    def is_direct_message(self) -> bool:
        return self.__is_message() and self.data["kind"] == REQUEST_KIND_DIRECT_MESSAGE and "recipient" in self.data

    def is_group_message(self) -> bool:
        # TODO Format the line
        return self.__is_message() and self.data["kind"] == REQUEST_KIND_GROUP_MESSAGE and "members" in self.data

    def is_login(self) -> bool:
        return self.is_valid() and self.data["kind"] == REQUEST_KIND_LOGIN and "username" in self.data

    def __is_initate_chat(self) -> bool:
        return self.is_valid() and "requester" in self.data and "encrypted" in self.data and "signed" in self.data

    def is_initiate_direct_message(self) -> bool:
        # TODO Format the line
        return self.__is_initate_chat() and self.data["kind"] == REQUEST_KIND_INITIATE_DIRECT_MESSAGE and "recipient" in self.data 

    def is_initiate_group_chat(self) -> bool:
        # TODO Format the line
        return self.__is_initate_chat() and self.data["kind"] == REQUEST_KIND_INITIATE_GROUP_CHAT and "recipients" in self.data and "recipient" in self.data

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

def direct_message(sender: str, recipient: str, msg: str, iv: str, tag: bytes) -> bytes:
    values = [("sender", sender), ("recipient", recipient), ("message", msg), ("iv", iv), ("tag", tag)]
    return create_request(REQUEST_KIND_DIRECT_MESSAGE, values)

def group_message(sender: str, recipients: str, group_name: str, msg: str, iv: str, tag: bytes) -> bytes:
    values = [("sender", sender), ("members", recipients), ("group_name", group_name), ("message", msg), ("iv", iv), ("tag", tag)]
    return create_request(REQUEST_KIND_GROUP_MESSAGE, values)

def login(username: str) -> bytes:
    values = [("username", username)]
    return create_request(REQUEST_KIND_LOGIN, values)

def initiate_direct_message(requester: str, recipient: str, encrypted: bytes, signed: bytes) -> bytes:
    values = [("requester", requester), ("recipient", recipient), ("encrypted", encrypted), ("signed", signed)]
    return create_request(REQUEST_KIND_INITIATE_DIRECT_MESSAGE, values)

def initiate_group_chat(requester: str, recipient: str, recipients: str, encrypted: bytes, signed: bytes, group_name) -> bytes:
    values = [("requester", requester), ("recipient", recipient), ("recipients", recipients), ("encrypted", encrypted), ("signed", signed), ("group_name", group_name)]
    return create_request(REQUEST_KIND_INITIATE_GROUP_CHAT, values)

def broadcast(message: str) -> bytes:
    values = [("message", message)]
    return create_request(REQUEST_KIND_BROADCAST, values)

def parse_request(request: bytes) -> Request:
    try:
        data = json.loads(request.decode())
        return Request(data)
    except json.JSONDecodeError as e:
        return Request(dict())