using UnityEngine;

public interface IFaceDataHandler
{
    void parseFaceData(string receiveData);
}
public interface IGazeHandler
{
    void LookAt(EyeGaze gaze);
}
public interface IHeadHandler
{
    void RotateTo(Quaternion rotation);
}
/*
using System.Collections;
using System.Collections.Generic;
using UnityEngine;*/