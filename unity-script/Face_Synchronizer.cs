using System.Text.RegularExpressions;
using UnityEngine;

public class Face_Synchronizer : MonoBehaviour, IFaceDataHandler
{

    private EyeGaze _eyeGaze;
    private Quaternion _headRotation;
    private Vector2 _leftEyeGaze, _rightEyeGaze;
    private Match _left_match, _left_value, _right_match, _right_value, _head_match, _head_value;
    private Regex leftEyeRegex, rightEyeRegex, headRegex, twoValRegex, fourValRegex;
    public EyeGaze eyeGaze
    {
        get
        {
            return _eyeGaze;
        }
        set
        {
            _eyeGaze = value;
            GazeChanged();
        }
    }
    public Quaternion headRotation
    {
        get
        {
            return _headRotation;
        }
        set
        {
            _headRotation = value;
            HeadChanged();
        }
    }



    public IGazeHandler eyeController;
    public IHeadHandler headController;



    private void GazeChanged()
    {
        eyeController.LookAt(this.eyeGaze);
    }
    private void HeadChanged()
    {
        headController.RotateTo(this.headRotation);
    }
    // Start is called before the first frame update
    void Start()
    {
        InitPacketResolveInfo();
        this.GetComponent<TcpReceiver>().faceDataHandler = this;
        this.GetComponent<UdpReceiver>().faceDataHandler = this;
    }
    // Update is called once per frame
    void Update() { }


    public void parseFaceData(string receiveData)
    {
        _left_match = leftEyeRegex.Match(receiveData);
        _right_match = rightEyeRegex.Match(receiveData);
        _head_match = headRegex.Match(receiveData);
        if (_left_match.Value.Equals(string.Empty) || _right_match.Value.Equals(string.Empty) || _head_match.Value.Equals(string.Empty))
            return;
        _left_value = twoValRegex.Match(_left_match.Groups["left"].Value);
        _right_value = twoValRegex.Match(_right_match.Groups["right"].Value);
        _head_value = fourValRegex.Match(_head_match.Groups["head"].Value);
        _leftEyeGaze = new Vector2(float.Parse(_left_value.Groups[1].Value), float.Parse(_left_value.Groups[2].Value));
        _rightEyeGaze = new Vector2(float.Parse(_right_value.Groups[1].Value), float.Parse(_right_value.Groups[2].Value));
        this.eyeGaze = new EyeGaze(_leftEyeGaze, _rightEyeGaze);
        this.headRotation = reviseHeadPose(float.Parse(_head_value.Groups[1].Value), float.Parse(_head_value.Groups[2].Value), float.Parse(_head_value.Groups[3].Value), bool.Parse(_head_value.Groups[4].Value));
    }

    private Quaternion reviseHeadPose(float roll, float pitch, float yaw, bool revise)
    {
        if (revise)
            return new Quaternion(1, 0, 0, 0) * Quaternion.Euler(roll, -pitch, yaw);
        else
            return Quaternion.Euler(roll, pitch, yaw);
    }

    void InitPacketResolveInfo()
    {
        leftEyeRegex = new Regex(@"(?<left>(?<='left': )'\(.*?\)')");
        rightEyeRegex = new Regex(@"(?<right>(?<='right': )'\(.*?\)')");
        headRegex = new Regex(@"(?<head>(?<='head': )'\(.*?\)')");
        twoValRegex = new Regex(@"^'\((.*),(.*)\)'$");
        fourValRegex = new Regex(@"^'\((.*),(.*),(.*),(.*)\)'$");
    }
}
