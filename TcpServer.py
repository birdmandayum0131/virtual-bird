import socket
import threading


class FaceDataTransportInterface:
    def transportFaceData(self, dataDict: dict):
        raise NotImplementedError("Method:transportFaceData not implemented!")


class TcpSender(FaceDataTransportInterface, object):
    def __init__(self, host, port):
        self.serverHost = host
        self.serverPort = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.serverHost, self.serverPort))
        self.dataSocket = None
        self.clientHost = None
        self.clientPort = None
        self.listening = False
        self.connected = False
        self.recvDone = True
        self.recvThread = None

    def startUpListen(self):
        if not self.listening:
            self.server.listen(0)
            print('Socket Startup')
            self.recvThread = threading.Thread(target=self._waiting4callBack)
            self.recvThread.daemon = True
            listenThread = threading.Thread(target=self._waiting4connect)
            listenThread.daemon = True
            listenThread.start()
        else:
            print("TCP Sender is already listen for connect")
            return

    def _waiting4connect(self):
        while True:
            try:
                self.dataSocket, (self.clientHost,
                                  self.clientPort) = self.server.accept()
                print("Connect to %s:%d" % (self.clientHost, self.clientPort))
                self.connected = True
                self.recvThread.start()
            except Exception as e:
                print("Connected Error, close data socket")
                self.dataSocket.close()
                self.clientHost, self.clientPort = None, None
                self.connected = False

    def _waiting4callBack(self):
        while True:
            if self.connected:
                done = self.dataSocket.recv(128)
                done = done.decode()
                if done == "Done!":
                    self.recvDone = True

    # Overrided
    def transportFaceData(self, dataDict):
        if self.connected and self.recvDone:
            # Encode with UTF-8
            self.dataSocket.send(str(dataDict).encode())
