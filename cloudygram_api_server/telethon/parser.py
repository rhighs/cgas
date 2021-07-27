import json
from telethon.tl.types import MessageMediaDocument, Document

def remove_buggy_chars(json_string):
    if json_string[1:] == "\"":
        json_string = json_string[1:]
    if json_string [:-1] == "\"":
        json_string = json_string[:-1]
    json_string = json_string.replace("\\", "")
    return json.loads(json_string)

def document_from_dict(document_dict):
    if(document_dict["_"] != "Document"):
        raise Exception("Invalid document type, must provide Document")
    return Document(
        id=             document_dict["id"],
        access_hash=    document_dict["access_hash"],
        file_reference= document_dict["file_reference"],
        date=           document_dict["date"],
        mime_type=      document_dict["mime_type"],
        size=           document_dict["size"],
        dc_id=          document_dict["dc_id"],
        attributes=     document_dict["attributes"],
        thumbs=         document_dict["thumbs"],
        video_thumbs=   document_dict["video_thumbs"]
    )

def parse_message_media(message_json):
    message_dict = remove_buggy_chars(message_json)
    if(message_dict["_"] != "MessageMediaDocument"):
        raise Exception("Invalid message type, must provide Document")
    document_dict = message_dict["document"]
    return MessageMediaDocument(
        document=document_from_dict(document_dict),
        ttl_seconds=message_dict["ttl_seconds"]
    )


def str_parse_updates(update_json):
    update_dict = remove_buggy_chars(update_json)
    media_dict = update_dict["updates"][1]["message"]["media"]
    return MessageMediaDocument(
        document=document_from_dict(media_dict["document"]),
        ttl_seconds=media_dict["ttl_seconds"]
    )

def parse_updates(update_json):
    if type(update_json) is str:
        return str_parse_updates(update_json)
    media_dict = update_json["updates"][1]["message"]["media"]
    return MessageMediaDocument(
        document=document_from_dict(media_dict["document"]),
        ttl_seconds=media_dict["ttl_seconds"]
    )
