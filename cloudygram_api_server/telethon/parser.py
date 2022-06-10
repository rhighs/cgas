from telethon.tl.types import MessageMediaDocument, Document, UpdateNewMessage, UpdateMessageID, Updates, PeerUser, Message
from base64 import encodebytes, decodebytes
from typing import Union
import json


def remove_buggy_chars(json_string: str) -> dict:
    if json_string[1:] == "\"":
        json_string = json_string[1:]
    if json_string [:-1] == "\"":
        json_string = json_string[:-1]
    json_string = json_string.replace("\\", "")
    return json.loads(json_string)

def document_from_dict(document_dict: dict) -> Document:
    if(document_dict["_"] != "Document"):
        raise Exception("Invalid document type, must provide Document")
    decoded_ref = decodebytes(document_dict["file_reference"].encode())
    return Document(
            id=             document_dict["id"],
            access_hash=    document_dict["access_hash"],
            file_reference= decoded_ref,
            date=           document_dict["date"],
            mime_type=      document_dict["mime_type"],
            size=           document_dict["size"],
            dc_id=          document_dict["dc_id"],
            attributes=     document_dict["attributes"],
            thumbs=         document_dict["thumbs"],
            video_thumbs=   document_dict["video_thumbs"]
            )

def parse_message_media(message_json: str) -> MessageMediaDocument:
    message_dict = remove_buggy_chars(message_json)
    if(message_dict["_"] != "MessageMediaDocument"):
        raise Exception("Invalid message type, must provide Document")
    document_dict = message_dict["document"]
    return MessageMediaDocument(
            document=       document_from_dict(document_dict),
            ttl_seconds=    message_dict["ttl_seconds"]
            )

def str_parse_updates(update_json: str) -> MessageMediaDocument:
    update_dict = remove_buggy_chars(update_json)
    media_dict = update_dict["updates"][1]["message"]["media"]
    return MessageMediaDocument(
            document=       document_from_dict(media_dict["document"]),
            ttl_seconds=    media_dict["ttl_seconds"]
            )

def parse_updates(update_json: Union[str, dict]) -> MessageMediaDocument:
    if type(update_json) is str:
        return str_parse_updates(update_json)
    media_dict = update_json["updates"][1]["message"]["media"]
    return MessageMediaDocument(
            document=       document_from_dict(media_dict["document"]),
            ttl_seconds=    media_dict["ttl_seconds"]
            )

def get_message_id(message_dict: dict) -> int:
    return message_dict["updates"][0]["id"]

def with_new_ref(message_dict: dict, ref: bytes) -> dict:
    message_dict["updates"][1]["message"]["media"]["document"]["file_reference"] = encodebytes(ref).decode()
    return message_dict


def __parse_updates(update_json) -> Updates:
    if type(update_json) is str:
        return str_parse_updates(update_json)

    update_dict: dict = update_json["udpates"][1]
    message_json = update_dict["message"]
    media_dict: dict = message_json["media"]

    up_msg_id  = UpdateMessageID(
            id = update_json["updates"][0]["id"],
            random_id = update_json["updates"][0]["random_id"],
    )

    msg_obj = Message(
            id =            up_msg_id.id,
            peer_id =       PeerUser(message_json["peer_id"]),
            date =          message_json["date"],
            message =       message_json["message"],
            out =           message_json["out"],
            mentioned =     message_json["mentioned"],
            media_unread =  message_json["media_unread"],
            silent =        message_json["silent"],
            post =          message_json["post"],
            from_scheduled =message_json["from_scheduled"],
            legacy =        message_json["legacy"],
            edit_hide =     message_json["edit_hide"],
            pinned =        message_json["pinned"],
            from_id =       message_json["from_id"],
            fwd_from =      message_json["fwd_from"],
            via_bot_id =    message_json["via_bot_id"],
            reply_to =      message_json["reply_to"],
            media =         MessageMediaDocument(
                                document=document_from_dict(media_dict["document"]),
                                ttl_seconds=media_dict["ttl_seconds"]
                                ),
            reply_markup = message_json["reply_markup"],
            entities =      [],
            views =         message_json["views"],
            forwards =      message_json["forwards"],
            replies =       message_json["replies"],
            edit_date =     message_json["edit_date"],
            post_author =   message_json["post_author"],
            grouped_id =    message_json["grouped_id"],
            restriction_reason = message_json["restriction_reason"],
            ttl_period =    message_json["ttl_perdiod"]
            )

    up_new_msg = UpdateNewMessage(
            message =       msg_obj,
            pts =           update_dict["pts"],
            pts_count=      update_dict["pts_count"],
            #others default to null
            )

    updates = [
            up_msg_id,
            up_new_msg,
            ]

    return Updates(
            updates,
            None,
            None,
            None,
            None
            )