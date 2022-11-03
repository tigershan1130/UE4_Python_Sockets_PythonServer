import socket
import time
import sys

from _thread import *
import threading


print_lock = threading.Lock()
# Host for hosting Python UDP

class TCPHandler(object):
    
    """description of class"""
    def __init__(self, host, port, RecieveMsgEvent, PlayerConnectedEvent, TickEvent, ClientFailedEvent):
        self.HOST = host
        self.PORT = port
        self.OnRecieveMessageEvent = RecieveMsgEvent
        self.OnPlayerConnected = PlayerConnectedEvent
        self.OnUpdate = TickEvent
        self.OnClientFailed = ClientFailedEvent

    def On_Client_Connected(self, clientConn, addr):
        
        self.OnPlayerConnected(clientConn)
        
        while True:        
            # data recieved from client
            try:
                msg = clientConn.recv(1024)
            except:
                continue

            # do some checks and if msg == someWeirdSignal: break:
            if not msg:
                print("Invalid Message, Disconnect User " + str(addr))
                print_lock.release()
                break

            decodeMsg = (msg.decode('UTF-8')).split()

            if decodeMsg[0] == '':
                print("Invalid Message, Disconnect User")
                print_lock.release()
                break
            else:
                self.OnRecieveMessageEvent(msg.decode('UTF-8'), clientConn)

        # we will never run into this until while true is done, only end of program.
        clientConn.close()

    def SendMsg(self, clientConn, message):  
        try:
            clientConn.send(message.encode('UTF-8'))
        except socket.error as err:
            clientConn.close()
            print("send message to client failed")
            self.OnClientFailed(clientConn)

    def StartHostServer(self):
        # Create UDP socket
        try: 
            # Here we made a socket instance and passed it two parameters.
            # The first parameter is AF_INET and the second one is SOCK_STREAM. 
            # AF_INET refers to the address family ipv4. 
            # The SOCK_STREAM means connection oriented TCP protocol. 
            # SOCK_DGRAM stands for connection for UDP protocol
            socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as err:
            print ("socket creation failed with error " + str(err))
            sys.exit()
    
        print ("Socket successfully Created")

        # bind local host and socket port
        try:
            socketServer.bind((self.HOST, self.PORT))
            # tells the socket library that we want it to queue up as many as 5 connect requests (the normal max) before refusing outside connections. 
            # If the rest of the code is written properly, that should be plenty.
            # it is better to refuse after so many connection against DDOS.
            # udpSocket.listen(5) 
        except socket.error as err:
            print("Bind failed" + str(err))
            # quit application
            sys.exit()

        print ("Socket succesfully binded")

        # for TCP, we ca just use socketServer.Listen, where UDP, we have to do below commented code time.sleep(1)
        socketServer.listen(5)
        print("Waiting for connection")

        # this loop will be continously running until end of the program.
        while True:
            #Estbalish a connection with client
            conn, addr = socketServer.accept()

            # lock acquired by client
            print_lock.acquire()

            # TODO: THis is wrong only accquire new thread when a client is created
            # we need to only use one thread for this, while pushing into a queue
            # since this is just a test, it's ok for this
            # we need to release thread when player disconnect which is not been done here.
            print('Connected to: ', addr[0],':', addr[1])
            
            start_new_thread(self.On_Client_Connected, (conn, addr,))
            print_lock.release()

        socketServer.close()