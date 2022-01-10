using UnityEngine;

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