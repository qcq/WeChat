import logging
import web
import time

# to reponse the /log get with the logs

log_file = r'/home/chuanqin/WeChat/com/qcq/main/static/single_log.log'

class Log(object):
    def GET(self):
        web.header('Content-type', 'text/plain; charset=UTF-8')
        web.header('Transfer-Encoding', 'chunked')
        delay = 0.01
        with open(log_file, 'r') as f:
            for line in f:
                yield line
                time.sleep(delay)

