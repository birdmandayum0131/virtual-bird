using System.Text.RegularExpressions;
using UnityEngine;

public class Face_Synchronizer : MonoBehaviour, TcpReceiver.FaceDataHandler
{

    private Regex leftEyeRegex;
    private Regex rightEyeRegex;
    private Regex valueRegex;

    private Match left_match;
    private Match left_value;
    private Match right_match;
    private Match right_value;
    private Vector2 leftEyeGaze;
    private Vector2 rightEyeGaze;
    private EyeGaze _eyeGaze;
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
    public interface GazeHandler
    {
        void LookAt(EyeGaze gaze);
    }
    public struct EyeGaze
    {
        public EyeGaze(Vector2 leftEye, Vector2 rightEye)
        {
            this.leftEyeGaze = leftEye;
            this.rightEyeGaze = rightEye;
        }
        public Vector2 leftEyeGaze;
        public Vector2 rightEyeGaze;
    }
    public GazeHandler eyeController;



    private void GazeChanged()
    {
        eyeController.LookAt(this.eyeGaze);
    }
    // Start is called before the first frame update
    void Start()
    {
        InitPacketResolveInfo();
        this.GetComponent<TcpReceiver>().faceDataHandler = this;
    }
    // Update is called once per frame
    void Update() { }


    public void parseFaceData(string receiveData)
    {
        left_match = leftEyeRegex.Match(receiveData);
        right_match = rightEyeRegex.Match(receiveData);
        if (left_match.Value.Equals(string.Empty) || right_match.Value.Equals(string.Empty))
            return;
        left_value = valueRegex.Match(left_match.Groups["left"].Value);
        right_value = valueRegex.Match(right_match.Groups["right"].Value);
        leftEyeGaze = new Vector2(float.Parse(left_value.Groups[1].Value), float.Parse(left_value.Groups[2].Value));
        rightEyeGaze = new Vector2(float.Parse(right_value.Groups[1].Value), float.Parse(right_value.Groups[2].Value));
        this.eyeGaze = new EyeGaze(leftEyeGaze, rightEyeGaze);
    }
    void InitPacketResolveInfo()
    {
        leftEyeRegex = new Regex(@"(?<left>(?<='left': )'\(.*?\)')");
        rightEyeRegex = new Regex(@"(?<right>(?<='right': )'\(.*?\)')");
        valueRegex = new Regex(@"^'\((.*),(.*)\)'$");
    }
}
