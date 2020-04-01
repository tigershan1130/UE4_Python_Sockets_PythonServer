##################################################
## Socket server python that talks to UE4
##################################################

import socket
import time
import sys

from TCPHandler import TCPHandler


def OnConnectedEvent(msg):
    print( str(msg))


if __name__ == '__main__':

    socketHandle = TCPHandler('127.0.0.1', 12345)

    socketHandle.StartHostServer()



