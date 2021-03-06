import sys
import os
import signal
import atexit
import argparse

from HTTP_v1_1.server import HTTPServer


# Global variables
httpServer = None


# Shut down HTTP server on Ctrl+C or on exiting from application
def shutdown(signal=None, frame=None):
    if httpServer:
        httpServer.stop()
        sys.exit(1)
signal.signal(signal.SIGINT, shutdown)
atexit.register(shutdown)


def ServerApp(**args):
    global httpServer

    serverIP = args["hostname"]
    serverPort = args["port"]
    www = args["web_server_directory"]
    
    httpServer = HTTPServer(serverIP, serverPort, www=www)
    
    try:
        httpServer.start()
    except Exception as e:
        print("Unexpected exception in launching HTTP server!")
        print(e)
    finally:
        if httpServer:
            httpServer.stop()


if __name__ == "__main__":
    # Argument parser
    parser = argparse.ArgumentParser(description='HTTP Server Application',
                                     prog='python \
                                           ServerApp.py \
                                           -t <hostname> \
                                           -p <port> \
                                           -w <web_server_directory>')

    parser.add_argument("-t", "--hostname", type=str, default="127.0.0.1",
                        help="Server hostname, default: 127.0.0.1")
    parser.add_argument("-p", "--port", type=int, default=8080,
                        help="Server port, default: 8080")
    parser.add_argument("-w", "--web_server_directory", type=str, default=os.path.join(os.getcwd(), "data", "server"),
                        help="Web server directory, default: /<Current Working Directory>/data/server/")

    # Read user inputs
    args = vars(parser.parse_args())

    # Run Server Application
    ServerApp(**args)