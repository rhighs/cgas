import  logging
import  logging.handlers
import  os
import  time
from    datetime import timezone, datetime

class Logger:
    def __init__(self):
        self.success_string = lambda msg: "\x1b[6;30;42m" + msg + "\x1b[0m"

    def log(self, message: str):
        print(self.success_string(message))

    def error(self, message: str):
        print(message)

    def raised_ex(self, message, type, by, time):
        s = f"Exception thrown by {by} at [{int(time)} Unix time] [{datetime.now(tz=timezone.gmt)} GMT]\n\nMessage: {message}"
        print(s)