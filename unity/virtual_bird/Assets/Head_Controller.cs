using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Head_Controller : MonoBehaviour, Face_Synchronizer.HeadHandler
{
    private GameObject body;
    private Quaternion bodyRotation;
    public Quaternion targetRotation, headRotation, head_stable, body_stable;
    //public Vector2 maxEyeMoving;
    // Start is called before the first frame update
    public float angle;
    private GameObject head;
    public float followSpeed = 180f;
    void Start()
    {
        LinkObjects();
    }

    // Update is called once per frame
    void Update()
    {
        Track();
        this.head.transform.rotation = this.head_stable * this.headRotation;
        this.body.transform.rotation = this.body_stable * this.bodyRotation;
    }
    void Reset()
    {
        LinkObjects();
        this.head_stable = Quaternion.Euler(0, 0, -90);
        this.body_stable = Quaternion.Euler(0, 0, -90);
        this.headRotation = Quaternion.identity;
        this.targetRotation = Quaternion.identity;
        this.head.transform.rotation = this.head_stable * this.headRotation;
    }
    void LinkObjects()
    {
        this.head = this.transform.Find("Root/Spine/Spine2/Head").gameObject;
        this.body = this.transform.Find("Root/Spine").gameObject;
        this.GetComponent<Face_Synchronizer>().headController = this;
    }

    private void Track()
    {
        this.angle = Quaternion.Angle(this.headRotation, this.targetRotation);
        float maxAngle = Time.deltaTime * this.followSpeed;
        this.bodyRotation = Quaternion.Euler(this.headRotation.eulerAngles);
        if (this.angle < maxAngle)
            this.headRotation = Quaternion.Euler(this.targetRotation.eulerAngles);
        else
            this.headRotation = Quaternion.RotateTowards(this.headRotation, this.targetRotation, maxAngle);
        this.bodyRotation = Quaternion.RotateTowards(Quaternion.identity, this.headRotation, 0.5f * Quaternion.Angle(Quaternion.identity, this.headRotation));
    }
    public void RotateTo(Quaternion rotation)
    {
        this.targetRotation = Quaternion.Euler(-rotation.eulerAngles[2], rotation.eulerAngles[1], rotation.eulerAngles[0]);
    }
}
