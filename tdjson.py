from telegram.client import Telegram
from telegram.tdjson import TDJson
tdj = TDJson() #to use later
tg = Telegram(
        api_id=0,
        api_hash="",
        phone="",
        database_encryption_key="",
        )
tg.login()
result = tg.get_chats()
result.wait()#wait for await completion
print(result.update)
tg.stop()
