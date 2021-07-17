from telegram.client import Telegram
from telegram.tdjson import TDJson
tdj = TDJson() #to use later
tg = Telegram(
        api_id=5558646,
        api_hash="30d3b4c9958fd165911d09254124d3bc",
        phone='+393421323295',
        database_encryption_key='changekey123',
        )
tg.login()
result = tg.get_chats()
result.wait()#wait for await completion
print(result.update)
tg.stop()
