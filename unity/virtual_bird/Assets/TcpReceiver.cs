using UnityEngine;

using System.Net.Sockets;
using System;
using System.Text;
public class TcpReceiver : MonoBehaviour
{
    public interface FaceDataHandler
    {
        void parseFaceData(string receiveData);
    }
    public FaceDataHandler faceDataHandler;
    private static TcpReceiver _singleton;
    public static TcpReceiver Singleton
    {
        get
        {
            if (_singleton == null)
            {
                _singleton = FindObjectOfType<TcpReceiver>();
            }
            return _singleton;
        }
    }
    private const int BUFFER_SIZE = 256;
    public string host = "127.0.0.1";
    public int port = 1208;
    private byte[] buffer;
    private Socket socket;
    public string receive_data;
    // Start is called before the first frame update
    void Start()
    {
        this.socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
        Connect();
    }
    // Update is called once per frame
    void Update() { }
    private void Connect()
    {
        try
        {
            this.socket.Connect(host, port);
        }
        catch (Exception e)
        {
            print(e.Message);
        }

        if (this.socket.Connected)
        {
            print("Connected");
            this.Receive();
        }
    }

    private void Receive()
    {
        if (!this.socket.Connected)
            return;
        buffer = new byte[BUFFER_SIZE];
        try
        {
            this.socket.BeginReceive(buffer, 0, BUFFER_SIZE, SocketFlags.None, new AsyncCallback(Receive_Callback), socket);
        }
        catch (Exception e)
        {
            print(e.Message);
        }
    }

    private void Receive_Callback(IAsyncResult ar)
    {
        if (!this.socket.Connected)
            return;
        int read = this.socket.EndReceive(ar);
        if (read > 0)
        {
            receive_data = Encoding.UTF8.GetString(buffer);
            faceDataHandler.parseFaceData(receive_data);
            Send("Done!");
            Receive();
        }
    }
    private void Send(string message)
    {
        if (!socket.Connected)
            return;
        byte[] msg = Encoding.UTF8.GetBytes(message);
        //sync
        socket.Send(msg);
    }

    private void OnDisable()
    {
        if (socket.Connected)
        {
            this.socket.Shutdown(SocketShutdown.Both);
        }
    }
}

