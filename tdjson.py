from telegram.client import Telegram
from telegram.tdjson import TDJson

from ctypes import c_int, c_char_p, c_double, c_voidp, c_longlong
from typing import Any, Dict, Optional, Union
import pkg_resources

def locate_clib() -> str:
    import platform
    if platform.system().lower() != "darwin":
        lib_path = "/usr/lib/libtdjson.so"
    else:
        return None
    return pkg_resources.resource_filename("telegram", lib_path)

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
