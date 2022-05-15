import sys
import json
import click
import uvicorn
from cloudygram_api_server import ApiServer
from os import path, makedirs

PATH = "keys.json"

@click.command()
@click.option("--asgi", is_flag=True)
def startup(asgi: bool):
    if path.exists(PATH):
        with open(PATH, "r") as f:
            data = json.load(f)
    else:
        print("File keys.json: You must insert api_id!")
        exit(1)

    # Ensure sessions folder is created
    if not path.exists("./sessions"):
        makedirs("./sessions")

    app = ApiServer(data["api_id"], data["api_hash"], port=5000, host_ip="127.0.0.1")

    if asgi:
        print("Starting ASGI server")
        uvicorn.run(app.create_asgi_app(), host="0.0.0.0", port=5000)
    else:
        print("Starting WSGI server")
        app.run()

if __name__ == "__main__":
    startup()
