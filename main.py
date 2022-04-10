import sys
import json
from cloudygram_api_server import ApiServer
from os import path, makedirs

PATH = "keys.json"

def startup():
    if path.exists(PATH):
        with open(PATH, "r") as f:
            data = json.load(f)
    else:
        print("File keys.json: You must insert api_id!")
        exit(1)

    # Ensure sessions folder is created
    if not path.exists("./sessions"):
        makedirs("./sessions")

    app = ApiServer(data["api_id"], data["api_hash"], port=5000, host_ip="0.0.0.0")
    app.run()

if __name__ == "__main__":
    startup()
