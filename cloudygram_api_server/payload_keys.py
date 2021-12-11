from types import SimpleNamespace

telegram_keys = SimpleNamespace()
download_keys = SimpleNamespace()
file_keys= SimpleNamespace()

telegram_keys.phone_code_hash = "phoneCodeHash"
telegram_keys.phone_number = "phoneNumber"
telegram_keys.first_name = "firstName"
telegram_keys.last_name = "lastName"
telegram_keys.phone_code = "phoneCode"

file_keys.mime_type= "mimeType"
file_keys.path = "path"
file_keys.name = "file"
file_keys.filename = "filename"

download_keys.message = "message"
