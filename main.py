from .pyrogram_api_server import PGApiServer

such = lambda empty: print("wow, such {emptyness} {cutemoji}".format(emptyness=empty, cutemoji=":3"))
such("empty")

app = PGApiServer(api_id="", api_has="", port=5000, host_ip="0.0.0.0")
