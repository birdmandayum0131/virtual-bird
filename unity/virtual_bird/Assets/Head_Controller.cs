using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Head_Controller : MonoBehaviour, Face_Synchronizer.HeadHandler
{
    private GameObject target;
    public Quaternion targetRotation;
    public Quaternion head_stable;
    //public Vector2 maxEyeMoving;
    // Start is called before the first frame update
    [SerializeField] private float angle;
    private GameObject head;
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

        //this.eyeBall.transform.rotation = Quaternion.Euler(0, 70, 0);
        //this.maxEyeMoving = new Vector2(1f, 1f);
        this.head_stable = Quaternion.Euler(0, 0, -90);
        //this.targetPosition = new Vector3(0f, 0f, 0f) + this.eyeBall_offset;
        //this.LookAt(new Face_Synchronizer.EyeGaze(new Vector2(0f, 0f), new Vector2(0f, 0f)));
    }
    void LinkObjects()
    {
        this.head = this.transform.Find("Root/Spine/Spine2/Head").gameObject;
        this.target = GameObject.Find("targetBall");
        this.GetComponent<Face_Synchronizer>().headController = this;
    }

    private void Focus()
    {
        //this.head.transform.forward = Vector3.MoveTowards(this.head.transform.forward, this.target.transform.position.normalized, Time.deltaTime * this.followSpeed);
        this.head.transform.rotation = this.head_stable * targetRotation;
    }
    /*
    public void RotateTo(float roll, float pitch, float yaw)
    {
        
        //Vector2 position = -(gaze.leftEyeGaze + gaze.rightEyeGaze) / 2;
        //Vector2 eyeBallMovement = position * this.maxEyeMoving;
        //Vector3 target_position = new Vector3(eyeBallMovement.x, eyeBallMovement.y, 0.0f);
        //target_position += this.eyeBall_offset;
        //Align the ghost eyeball x, y, z axis
        
        //rolling the eyeball
    }
    */
    public void RotateTo(Quaternion rotation)
    {
        float _tmp = rotation.x;
        rotation.x = -rotation.y;
        rotation.y = _tmp;
        this.targetRotation = rotation;
    }
}
