import sys
from pyrogram_api_server import composeHelp
from pyrogram_api_server import ApiServer

if(len(sys.argv) > 1):
    command = sys.argv[1]
    if(command == "--help"):
        print(composeHelp())
        exit(0)
    elif(command == "--no-keys"):
        app = ApiServer(port=5000, host_ip="0.0.0.0", mode="no-keys")
        app.run()
        exit(0)

api_id = input("Your api_id: ")
api_hash = input("Your api_hash: ")
app = ApiServer(api_id, api_hash, port=5000, host_ip="0.0.0.0")
app.run()