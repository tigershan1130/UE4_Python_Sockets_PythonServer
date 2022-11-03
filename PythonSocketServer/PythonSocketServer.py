###############################################################
# Socket server python that talks to UE4/Unity
# I use this for simple testing between Client and Python server
# for commercial, I would suggest using GO as server
################################################################

import socket
import time
import sys
from _thread import *
import threading


from TCPHandler import TCPHandler

# stores all player input information
playerInputData = {}

toRemoveClients = []

def OnPlayerConnected(clientInfo):
    if not (str(clientInfo) in playerInputData.keys()):
        print("Player Connected: " + str(clientInfo))

        # client can have unlimited number of list, we should check for array overflow here when it is bigger than max length
        # at OnRecieveMessage, this will be populated        
        playerInputData[clientInfo] = []
 

def OnRecieveMessage(msg, clientInfo):
    print(str(clientInfo) + " " + str(msg))


def OnClientDisconnected(clientInfo):
    print("Client not connected")
    toRemoveClients.append(clientInfo)

def OnTick():

    starttime = time.time()
    while True:
        #print("On Server Update...")
        
        #TODO: send proto message back to client.
        for playerConn in playerInputData.keys():
            socketHandle.SendMsg(playerConn, "ACK")

        for client in toRemoveClients:
            playerInputData.pop(client)

        toRemoveClients.clear()
        
        time.sleep(0.1 - ((time.time() - starttime) % 0.1))


if __name__ == '__main__':

    socketHandle = TCPHandler('127.0.0.1', 12345, OnRecieveMessage, OnPlayerConnected, OnTick, OnClientDisconnected)

    start_new_thread(OnTick)

    socketHandle.StartHostServer()




