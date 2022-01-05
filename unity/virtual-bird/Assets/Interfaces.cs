using UnityEngine;

public interface FaceDataHandler
{
    void parseFaceData(string receiveData);
}
public interface GazeHandler
{
    void LookAt(EyeGaze gaze);
}
public interface HeadHandler
{
    void RotateTo(Quaternion rotation);
}
/*
using System.Collections;
using System.Collections.Generic;
using UnityEngine;*/