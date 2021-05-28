msg_dict: dict = {
    "NO_KEYS" : "--no-keys : dont ask for api keys from shell, you will need to provide them via http POST"
}

def composeHelp():
    string = ""
    for k, v in msg_dict.items():
        string += f"\n\t{v}"
    return f"{string}\n"
