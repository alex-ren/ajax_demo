#!/usr/bin/env python2.6
# -*- encoding: utf-8 -*- 

'''
handler.Handler is the HTTP handler for ajaxserver
'''

import BaseHTTPServer
import logging as log
import os
import subprocess

try:
import simplejson as json
except ImportError:
import json

from datetime import datetime

class Handler(BaseHTTPServer.BaseHTTPRequestHandler):

def logRequest(s):
log.debug("%s: %s/%s" %(s.client_address, s.command, s.path))

def do_GET(self):
self.logRequest()

path = self.path

if 'Content-type' in self.headers:
contentType = self.headers['Content-type']
else:
contentType = 'text/html'

log.debug("ajaxserver.GET: Path %s" % path)
log.debug("ajaxserver.GET: Content-type %s" % contentType)

if contentType.startswith('text/html'):
(respCode, respContent, respContentType) = self.do_GET_HTML()
elif contentType.startswith('application/json'):
(respCode, respContent, respContentType) = self.do_GET_JSON()

self.send_response(respCode, "thank you")
self.send_header('Content-type', respContentType)
self.send_header('Content-length', len(respContent))
self.end_headers()

self.wfile.write(respContent)

def do_POST(self):
self.logRequest()

path = self.path
contentType = self.headers['Content-type']

log.debug("ajaxserver.POST: Path %s" % path)
log.debug("ajaxserver.POST: Content-type %s" % contentType)

if not contentType.startswith('application/json'):
self.send_response(404, "oh, shiny!")
self.send_header('Content-type', 'application/json')
self.end_headers()
self.wfile.write(json.dumps({ "error": "only accepting application/json" }))
return

contentLength = int(self.headers['Content-length'])
content = self.rfile.read(contentLength)

log.debug("ajaxserver.POST: Content-length %d" % contentLength)
log.debug("ajaxserver.POST: Content: %s" % content)

data = json.loads(content)
if 'input' not in data:
log.debug("ajaxserver.POST: missing input parameter: %s" % content)
self.send_response(404, "oh, shiny!")
self.send_header('Content-type', 'application/json')
self.end_headers()
self.wfile.write(json.dumps({ "error": "missing input parameter" }))
return

self.send_response(200, "oh, shiny!")
self.send_header('Content-type', 'application/json')
self.end_headers()
self.wfile.write(json.dumps({ "processed": len(data['input'])}))

return

def do_GET_HTML(self):

docRoot = self.server.docRoot
docPath = "%s%s" % (docRoot, self.path)
errorPath = "%s/not-found.html" % docRoot

if self.path.startswith('../'):
log.debug('ajaxserver.GET(HTML): "%s" trying to escape from the sandbox' % self.path)
docFile = open(errorPath, 'r')
code = 404
elif docPath.endswith('/') and os.path.exists("%sindex.html" % docPath):
log.debug('ajaxserver.GET(HTML): serving %sindex.html for %s' % (docPath, self.path))
docFile = open("%sindex.html" % docPath, 'r')
code = 200
elif os.path.exists(docPath):
log.debug('ajaxserver.GET(HTML): serving %s for %s' % (docPath, self.path))
docFile = open(docPath, 'r')
code = 200
else:
log.debug('ajaxserver.GET(HTML): no document found for %s' % self.path)
docFile = open(errorPath, 'r')
code = 404

doc = docFile.read()
docFile.close()

return (code, doc, 'text/html')

def utilProcessCount(self):
psCmd = subprocess.Popen(["ps", "ax"], stdout=subprocess.PIPE)
wcCmd = subprocess.Popen(["wc", "-l"], stdin=psCmd.stdout, stdout=subprocess.PIPE)
count = wcCmd.communicate()[0]

return json.dumps({ 'processcount': int(count) - 1 })

def do_GET_JSON(self):

if self.path.startswith('/ajax/time'):
return (200, '{ "time": "%s" }' % datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC'), 'application/json')

if self.path.startswith('/ajax/processcount'):
return (200, self.utilProcessCount(), 'application/json')

return (200, '{ "resp": "bark!" }', 'application/json')

