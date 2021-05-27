import logging
import logging.handlers
import os

class Loggeer:
    def __init__(self):
        self.success_string = lambda msg: "\x1b[6;30;42m" + msg + "\x1b[0m"

    def log(self, message: str):
        print(self.success_string(message))

    def error(self, message: str):
        print(message)
