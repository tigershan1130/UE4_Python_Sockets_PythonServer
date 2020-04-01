class UDPHandler(object):
    """description of class"""


# for UDP:
# while 1:
#
#    # Receive data from client (data, addr)
#    d = socket.recvfrom(1024)
#    data = str(d[0], "utf-8") 
#    addr = d[1]
#
#    # Print to the server who made a connection.
#    print("{} wrote:".format(addr))
#    print(data)
#       
#    # Now have our UDP handler handle the data
#    myUDPHandler = UDPRequestHandler()
#    myResponse = myUDPHandler.handle(data)
#
#    # Respond back
#    print(myResponse)
#    socketServer.sendto(bytes(myResponse, 'utf-8'), addr)
#    
# socketServer.close()