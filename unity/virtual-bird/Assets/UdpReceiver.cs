using System;
using System.Collections;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;

public class UdpReceiver : MonoBehaviour
{
    public IFaceDataHandler faceDataHandler;
    private static UdpReceiver _singleton;
    public static UdpReceiver Singleton
    {
        get
        {
            if (_singleton == null)
            {
                _singleton = FindObjectOfType<UdpReceiver>();
            }
            return _singleton;
        }
    }
    private IPEndPoint iPEndPoint;
    private EndPoint serverEndPoint;
    private const int BUFFER_SIZE = 256;
    public bool connected = false;
    public string host = "127.0.0.1";
    public int port = 1208;
    private byte[] buffer;
    private Socket socket;
    private Thread recvThread;
    public string receive_data;
    // Start is called before the first frame update
    void Start()
    {
        this.socket = new Socket(AddressFamily.InterNetwork, SocketType.Dgram, ProtocolType.Udp);
        this.recvThread = new Thread(Receive);
        Connect();
    }
    // Update is called once per frame
    void Update() { }
    private void Connect()
    {
        this.iPEndPoint = new IPEndPoint(IPAddress.Parse(host), port);
        //Listen to any available port
        IPEndPoint endPoint = new IPEndPoint(IPAddress.Any, 0);
        this.serverEndPoint = (EndPoint)endPoint;
        this.connected = true;
        print("UDP Ready");
        this.recvThread.Start();
    }

    private void Receive()
    {
        while (this.connected)
        {
            buffer = new byte[BUFFER_SIZE];
            try
            {
                Send("UDP Data");
                int read = this.socket.ReceiveFrom(buffer, ref serverEndPoint);
                if (read > 0)
                {
                    receive_data = Encoding.UTF8.GetString(buffer);
                    faceDataHandler.parseFaceData(receive_data);
                }
            }
            catch (Exception e)
            {
                print(this.socket == null);
                print(e.Message);
                Thread.Sleep(1000);
            }
        }
    }

    private void Disconnect()
    {
        if (this.connected)
            this.connected = false;
        if (this.socket != null)
            this.socket.Close();
    }

    private void Send(string message)
    {
        if (!this.connected)
            return;
        byte[] msg = Encoding.UTF8.GetBytes(message);
        //sync
        this.socket.SendTo(msg, SocketFlags.None, this.iPEndPoint);
    }

    private void OnDisable()
    {
        Disconnect();
    }
}