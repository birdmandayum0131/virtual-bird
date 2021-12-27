# virtual-bird(Still in the developing)
  A repository for studying virtual characters technique.  
  Can not yet be made use of for smoothly real-time application now.  
  But it will!🐱‍🚀
## About The Project
  This project aims to apply different face/body alignment algorithm on virtual character synchronizing.  
  ~~And promote my coding level.~~
## Timeline
  - support OpenCV Head Pose Estimation `2021/12/26`
  - support OpenCV Gaze Tracking `2021/12/08`
  - support [1adrianb][1adrianb/face-alignment] facial landmarks detector `2021/12/08`
  - support [Ghost][Unity Technologies / Ghost] character `2021/12/08`
## Roadmap
  - Algorithm
    - Landmarks Detection
      - [x] [1adrianb / face-alignment][1adrianb/face-alignment]
      - [ ] [Dlib](http://dlib.net/)
    - Gaze Tracking
      - [x] OpenCV moments(simple)
    - Head Alignment
      - [x] OpenCV solvePnP
    - Face Expression Detection `Under Planning`
    - Pose Estimation `Under Planning`
    - Hand Tracking / Gesture Recognition `Under Planning`
  - Unity Model
    - 3D
      - [x] [Unity Technologies / Ghost][]
    - 2D `Under Planning`
  - Android Support `Under Planning`
  - iOS Support `Under Planning`
## Environment
  This project is developed on a old hardware, but these information may still be helpful for you :  
  |CPU     |GPU    |RAM   |VRAM   |Python  |CUDA   |cuDNN |PyTorch|
  |:------:|:-----:|:----:|:-----:|:------:|:-----:|:----:|:-----:|
  |FX-8320E|GTX 960| 8 Gb | 2 Gb  |  3.5   |  9.2  |7.6.5 |1.5.1  |
## Acknowledgement
  A part of the code is refer to following repositories. You can check their project for more related knowledge.  
  Thanks for their open resources!
  - [1adrianb/face-alignment][]
  - [antoinelame/GazeTracking][]
  - [kwea123/VTuber_Unity][]
  - [yinguobing/head-pose-estimation][]

[1adrianb/face-alignment]:          https://github.com/1adrianb/face-alignment          "1adrianb/face-alignment"
[antoinelame/GazeTracking]:         https://github.com/antoinelame/GazeTracking         "antoinelame/GazeTracking"
[kwea123/VTuber_Unity]:             https://github.com/kwea123/VTuber_Unity             "kwea123/VTuber_Unity"
[yinguobing/head-pose-estimation]:  https://github.com/yinguobing/head-pose-estimation  "yinguobing/head-pose-estimation"
[Unity Technologies / Ghost]:       https://assetstore.unity.com/packages/templates/tutorials/3d-beginner-tutorial-resources-143848
