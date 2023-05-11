# 服务同名启动入口
import signal
import logging
import sys
from gevent.pywsgi import WSGIServer
import argparse
import config
from logger.logger import init
from server import server
wsgi_server = None
log = None


def signal_handler(sig, frame):
    if sig == signal.SIGTERM:
        log.info("Stopping df-web-service application...")
        wsgi_server.stop()
    elif sig == signal.SIGHUP:
        log.info("Reload config of df-web-service application...")
        config.config.is_valid()


if __name__ == '__main__':
    if not config.config.is_valid():
        logger.init(True)
        log = logging.getLogger(__name__)
        log.error("Config parser Error")
        sys.exit(1)

    logger.init(config.config.daemon)
    log = logging.getLogger(__name__)


    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-g", "--debug", help="run in debug mode", action="store_true")
    args = parser.parse_args()

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGHUP, signal_handler)

    try:
        if args.debug:
            log.info(
                '======== Debug starting service application listen ' +
                str(PORT) + '... ========')
            server.run(host=HOST, port=PORT, debug=True)
        else:
            log.info('========  Starting service application listen ' +
                     str(PORT) + '...========')
            wsgi_server = WSGIServer(('', PORT), server)
            wsgi_server.serve_forever()
    except KeyboardInterrupt:
        log.info("ctrl+c Stopping service application...")
