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
        self.able_to_conn = threading.Event()
        self.able_to_recv = threading.Event()
        self.able_to_conn.set()
        self.able_to_recv.clear()
        self.dataDict = dict()
        self.dataSocket = None
        self.clientHost = None
        self.clientPort = None
        self.recvThread = None
        self.listenThread = None
        self._is_stop = False
    
    def stop(self):
        self._is_stop = True

    def start(self):
        self.server.listen(0)
        print('Socket Startup')
        self._listen_new_socket()
        self.recvThread = threading.Thread(target=self._waiting4request)
        self.recvThread.daemon = True
        self.recvThread.start()
    
    def _waiting4connect(self):
        while not self._is_stop:
            self.able_to_conn.wait()
            try:
                print("Start Listening...")
                self.dataSocket, (self.clientHost, self.clientPort) = self.server.accept()
                print("Connect to %s:%d" % (self.clientHost, self.clientPort))
                self.dataSocket.settimeout(3)
                self.able_to_conn.clear()
                self.able_to_recv.set()
            except Exception as e:
                print("Connected Failed, restart in 3 seconds.")
                time.sleep(3)

    def _waiting4request(self):
        while not self._is_stop:
            self.able_to_recv.wait()
            try:
                data = self.dataSocket.recv(128).decode()
                if data == "TCP Data":
                    self.dataSocket.send(str(self.dataDict).encode())
            except Exception as e:
                self._connect_error(e)

    def _connect_error(self, exception):
        print("Connected Error : \"%s\"\nClose data socket and listen for new Socket.\n"%(str(exception)))
        self.dataSocket.close() 
        self.dataSocket, self.clientHost, self.clientPort = None, None, None
        self.able_to_recv.clear()
        self.able_to_conn.set()
        

    def _listen_new_socket(self):
        self.listenThread = threading.Thread(target=self._waiting4connect)
        self.listenThread.daemon = True
        self.listenThread.start()
    
    
    # Overrided
    def transportFaceData(self, dataDict):
        self.dataDict = dataDict

class UdpServer(FaceDataTransportHandler, object):
    def __init__(self, host, port):
        self.serverHost = host
        self.serverPort = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind((self.serverHost, self.serverPort))
        self.dataDict = dict()
        self.dataSocket = None
        self.listenThread = None
        self._is_stop = False
    
    #Overrided
    def stop(self):
        self._is_stop = True

    #Overrided
    def start(self):
        print('Socket Startup')
        self.listenThread = threading.Thread(target=self._waiting4request)
        self.listenThread.daemon = True
        self.listenThread.start()    

    def _waiting4request(self):
        while not self._is_stop:
            try:
                data, addr = self.server.recvfrom(128)
                data = data.decode()
                if data == "UDP Data":
                    self._send_data_pack(addr)
            except Exception as e:
                print("Connected Error : \"%s\"\nClose data socket and listen for new Socket.\n"%(str(e)))

    def _send_data_pack(self, addr):
        self.server.sendto(str(self.dataDict).encode(), addr)
        
    # Overrided
    def transportFaceData(self, dataDict):
        self.dataDict = dataDict
