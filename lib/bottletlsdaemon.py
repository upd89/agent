import os
import argparse
import signal
import daemon
import lockfile
import bottle
from contextlib import contextmanager

# https://raw.githubusercontent.com/jonathanhood/bottledaemon/master/bottledaemon/bottledaemon.py
# http://www.socouldanyone.com/2014/01/bottle-with-ssl.html


class SSLWSGIRefServer(bottle.ServerAdapter):

    def run(self, handler):
        from wsgiref.simple_server import make_server, WSGIRequestHandler
        import ssl
        if self.quiet:
            class QuietHandler(WSGIRequestHandler):

                def log_request(*args, **kw):
                    pass
            self.options['handler_class'] = QuietHandler
        srv = make_server(self.host, self.port, handler, **self.options)
        srv.socket = ssl.wrap_socket(
            srv.socket,
            certfile='/opt/upd89/agent/certs/server.pem',
            # path to certificate
            server_side=True)
        srv.serve_forever()


@contextmanager
def __locked_pidfile(filename):
    # Acquire the lockfile
    lock = lockfile.FileLock(filename)
    lock.acquire(-1)

    # Write out our pid
    realfile = open(filename, "w")
    realfile.write(str(os.getpid()))
    realfile.close()

    # Yield to the daemon
    yield

    # Cleanup after ourselves
    os.remove(filename)
    lock.release()


def daemon_run(host="localhost", port="8080", pidfile=None, logfile=None):
    """
    Get the bottle 'run' function running in the background as a daemonized
    process.

    :host: The host interface to listen for connections on. Enter 0.0.0.0
           to listen on all interfaces. Defaults to localhost.
    :port: The host port to listen on. Defaults to 8080.
    :pidfile: The file to use as the process id file. Defaults to "bottle.pid"
    :logfile: The file to log stdout and stderr from bottle to. Defaults to "bottle.log"

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["start", "stop"])
    args = parser.parse_args()

    if pidfile is None:
        pidfile = os.path.join(
            os.getcwd(),
            "bottle.pid"
        )

    if logfile is None:
        logfile = os.path.join(
            os.getcwd(),
            "bottle.log"
        )

    if args.action == "start":
        log = open(logfile, "w+")
        context = daemon.DaemonContext(
            pidfile=__locked_pidfile(pidfile),
            stdout=log,
            stderr=log
        )

        with context:
            # bottle.run(host=host, port=port)
            srv = SSLWSGIRefServer(host=host, port=port)
            bottle.run(server=srv)
    else:
        with open(pidfile, "r") as p:
            pid = int(p.read())
            os.kill(pid, signal.SIGTERM)
