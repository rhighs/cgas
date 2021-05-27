import logging
import logging.handlers
import os

class Loggeer:
    def __init__(self):
        self.success_string = lambda msg: "\x1b[6;30;42m" + msg + "\x1b[0m"

    def log(self, message: str):
        print(self.success_string(message))

    def error():

        pass

def print_format_table():
    for style in range(8):
        for fg in range(30,38):
            s1 = ''
            for bg in range(40,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')
         
print_format_table()
