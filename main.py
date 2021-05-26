from pyrogram_api_server import ApiServer

app = ApiServer(api_id="", api_hash="", port=5000, host_ip="0.0.0.0")
app.run()