import socket
import threading
import time
from .Abstract import FaceDataTransportHandler


class TcpServer(FaceDataTransportHandler, object):
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
        self.listenThread = None
    
    def startUpListen(self):
        if not self.listening:
            self.server.listen(0)
            print('Socket Startup')
            self.recvThread = threading.Thread(target=self._waiting4callBack)
            self.recvThread.daemon = True
            self._create_new_listener()
        else:
            print("TCP Server is already listen for connect")
            return
    
    def _waiting4connect(self):
        if not self.connected:
            try:
                self.dataSocket, (self.clientHost, self.clientPort) = self.server.accept()
                print("Connect to %s:%d" % (self.clientHost, self.clientPort))
                self.connected = True
                if self.recvThread.is_alive():
                    self.recvThread.start()
            except Exception as e:
                self._cnt_err(e)

    def _waiting4callBack(self):
        while self.connected:
            try:
                done = self.dataSocket.recv(128)
                done = done.decode()
                if done == "Done!":
                    self.recvDone = True
            except Exception as e:
                self._cnt_err(e)

    def _cnt_err(self, exception):
        print("Connected Error : \"%s\"\nClose data socket and listen for new Socket.\n"%(str(exception)))
        self.dataSocket.close()
        self.clientHost, self.clientPort = None, None
        self.connected = False
        self._create_new_listener()

    def _create_new_listener(self):
        self.listenThread = threading.Thread(target=self._waiting4connect)
        self.listenThread.daemon = True
        self.listenThread.start()
    
    
    # Overrided
    def transportFaceData(self, dataDict):
        if self.connected and self.recvDone:
            # Encode with UTF-8
            try:
                self.dataSocket.send(str(dataDict).encode())
            except Exception as e:
                self._cnt_err(e)
