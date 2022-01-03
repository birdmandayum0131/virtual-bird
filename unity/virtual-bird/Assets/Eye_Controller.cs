using UnityEngine;


public class Eye_Controller : MonoBehaviour, Face_Synchronizer.GazeHandler
{
    private GameObject target;
    public Vector3 targetPosition;
    public Vector3 eyeBall_offset;
    public Vector2 maxEyeMoving;
    // Start is called before the first frame update
    private GameObject eyeBall;
    public float followSpeed = 1f;
    //public float degreeStep = 45f;
    void Start()
    {
        LinkObjects();
    }

    // Update is called once per frame
    void Update()
    {
        Focus();
    }
    void Reset()
    {
        LinkObjects();
        this.eyeBall.transform.rotation = Quaternion.Euler(70, 0, 270);
        this.maxEyeMoving = new Vector2(2f, 2f);
        this.eyeBall_offset = new Vector3(0f, 0.7f, 2f);
        this.targetPosition = new Vector3(0f, 0f, 0f) + this.eyeBall_offset;
        this.LookAt(new Face_Synchronizer.EyeGaze(new Vector2(0f, 0f), new Vector2(0f, 0f)));
    }
    void LinkObjects()
    {
        this.eyeBall = this.transform.Find("Root/Spine/Spine2/Head/Eye").gameObject;
        this.target = GameObject.Find("targetBall");
        this.GetComponent<Face_Synchronizer>().eyeController = this;
    }

    private void Focus()
    {
        this.eyeBall.transform.right = Vector3.MoveTowards(this.eyeBall.transform.right, this.targetPosition.normalized, Time.deltaTime * this.followSpeed);
    }
    public void LookAt(Face_Synchronizer.EyeGaze gaze)
    {
        Vector2 position = -(gaze.leftEyeGaze + gaze.rightEyeGaze) / 2;
        Vector2 eyeBallMovement = position * this.maxEyeMoving;
        Vector3 target_position = new Vector3(eyeBallMovement.x, eyeBallMovement.y, 0.0f);
        target_position += this.eyeBall_offset;
        //Align the ghost eyeball x, y, z axis
        this.targetPosition = -(target_position);
        //rolling the eyeball
    }


}
