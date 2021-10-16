"""
Use 2 threads to serve both websites in their own directories
seperately & simulatenously, using 2 http.server like instances
Websites : [Kamandprompt](https://github.com/KamandPrompt/kamandprompt.github.io)
           [Sys Admin & Infosec](https://github.com/KamandPrompt/SAIC-Website)
on ports 1025, 1026 respectively

These ports can be mapped to any others while running the docker container
"""

from http import server
import socketserver
import threading
import os
import sys

assert os.path.isdir('./kamandprompt.github.io')
assert os.path.isdir('./SAIC-Website')


# These classes serve 2 purposes -
# * Set the server root directory to the corresponding repo directory only
#   This prevents files from outside being served (normal function)
#   Necessary since the CWD is outside both
# * Override the log_message function to mention which website's log is
#   being displayed. Otherwise it is hard to tell.


class KP_Handler(server.SimpleHTTPRequestHandler) :
    def __init__(self, *args, **kwargs) :
        kwargs.pop('directory', '.')
        super().__init__(*args, directory='kamandprompt.github.io', **kwargs)

    def log_message(self, format, *args) :
        sys.stderr.write("KP  : %s - - [%s] %s\n" %
            (self.address_string(), self.log_date_time_string(), format%args))


class SAIC_Handler(server.SimpleHTTPRequestHandler) :
    def __init__(self, *args, **kwargs) :
        kwargs.pop('directory', '.')
        super().__init__(*args, directory='SAIC-Website', **kwargs)

    def log_message(self, format, *args) :
        sys.stderr.write("SAIC: %s - - [%s] %s\n" %
            (self.address_string(), self.log_date_time_string(), format%args))


# Targets for threads

def run_KP_website():
    PORT = 1025
    with socketserver.TCPServer(("", PORT), KP_Handler) as serv:
        print("KP website - serving at port", PORT)
        serv.serve_forever()

def run_SAIC_website():
    PORT = 1026
    with socketserver.TCPServer(("", PORT), SAIC_Handler) as serv:
        print("SAIC website - serving at port", PORT)
        serv.serve_forever()


t1 = threading.Thread(target=run_KP_website, name='KP-server')
t2 = threading.Thread(target=run_SAIC_website, name='SAIC-server')

t1.start()
t2.start()
