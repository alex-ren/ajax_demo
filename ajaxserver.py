#!/usr/bin/env python2.6
# -*- encoding: utf-8 -*- 

'''
ajaxServer is a simple proof-of-concept web server for serving AJAX pages and their contents.
'''

import BaseHTTPServer
import logging as log
import logging.handlers
import os
import re
import subprocess
import sys
import urllib2

import handler

from datetime import date

class AjaxServer(BaseHTTPServer.HTTPServer):

def __init__(self, serverAddress, requestHandlerClass, docRoot):
BaseHTTPServer.HTTPServer.__init__(self, serverAddress, requestHandlerClass)
self.docRoot = docRoot

# from python module doc
def run(server_class=BaseHTTPServer.HTTPServer,
handler_class=BaseHTTPServer.BaseHTTPRequestHandler,
root='root',
ip='', port=8000):

server_address = (ip, port)

httpd = server_class(server_address, handler_class, root)
log.info("ajaxserver: waiting for requests")
httpd.serve_forever()

if __name__ == '__main__':

log.basicConfig(level = log.DEBUG,
format = '%(asctime)s %(levelname)-8s %(message)s',
datefmt = '%a, %d %b %Y %H:%M:%S')

ip = '127.0.0.1'
port = 8000
docRoot = '../root'

try:

# start the server
log.info("ajaxserver: starting HTTP server on %s:%d" %(ip, port))
run(server_class=AjaxServer, handler_class=handler.Handler, ip=ip, port=port, root=docRoot)
log.info("ajaxserver: terminating")

except KeyboardInterrupt, k:
print "\r<<terminated by user, good bye!>>"
log.info("aborted by user, terminating")


