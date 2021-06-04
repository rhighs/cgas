import json
from telethon.tl.types import MessageMediaDocument, Document

def parse_message(message_json):
    if message_json[1:] == "\"":
        message_json = message_json[1:]
    if message_json[:-1] == "\"":
        message_json = message_json[:-1]
    message_json = message_json.replace("\\", "")
    message_dict = json.loads(s=message_json)
    if(message_dict["_"] != "MessageMediaDocument"):
        raise Exception("Invalid message type, must provide Document")
    document_dict: dict= json.loads(json.dumps(obj=message_dict["document"]))
    if(document_dict["_"] != "Document"):
        raise Exception("Invalid document type, must provide Document")
    document = Document(
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

    return MessageMediaDocument(document=document, ttl_seconds=message_dict["ttl_seconds"])