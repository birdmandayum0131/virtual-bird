# virtual-bird(Still in the developing)
  ![kenyx-94670](https://user-images.githubusercontent.com/34616769/147909406-12864407-eb5b-4e3a-a076-afbd58a301f2.gif)  
  A repository for studying virtual characters technique.  
  Can not yet be made use of for smoothly real-time application now.  
  But it will!🐱‍🚀  
## About The Project
  This project aims to apply different face/body alignment algorithm on virtual character synchronizing.  
  ~~And promote my coding level.~~   
## Getting Started
The following steps will install required packages and run the demo program,  
and the tutorial is based on anaconda environment.
### Prerequisites
I use these packages to develop the project.
- [FAN][]
```
conda install -c 1adrianb face_alignment
```
- numpy
```
conda install -c anaconda numpy
```
- OpenCV
```
conda install -c conda-forge opencv
```
- Dlib  

**You can build cuda-supported dlib by yourself, and it may be faster.**
```
conda install -c conda-forge dlib
```
### Installation
You can just clone the repository.
```
git clone https://birdmandayum0131/virtual-bird.git
```
### Demo
Change directory to your project path and run demo.py
```
cd path/to/your/project/
python demo.py
```
  
If the camera window show sucessfully,  
you can use `l` `h` `a` commands to test **landmarks**、**head pose** and **head axis** features,  
and `q` to exist the program.  
  
  
If everything works normally, follow these steps to demo on unity.
1. create a unity project and add one of following supported 3D model prefab in your scene.  
2. copy the scripts in **unity-scripts** folder to your unity project in Unity Editor.
3. add these scripts as components to your 3D model prefab.
    - Tcp/Udp Receiver (choose one)
    - Face Synchronizer
    - All scripts in the folder which correspond to your prefab

If all done, play the sample scene.  (Sorry I didn't export it to .exe file now.🐱‍🚀)  

  
You can change default config to fit your environments in **config/config.py**  

## Timeline
  - support Dlib Face/Landmarks Detector `2022/01/03`
  - change development environment to newer version(~~Of course, not hardware~~😢) `2021/12/27`
  - support OpenCV Head Pose Estimation `2021/12/26`
  - support OpenCV Gaze Tracking `2021/12/08`
  - support [FAN][] facial landmarks detector `2021/12/08`
  - support [Ghost][] character `2021/12/08`
## Roadmap
  - Algorithm
    - Face Detection
      - [x] [SFD][FAN]
      - [x] [BlazeFace][FAN]
      - [x] [Dlib](http://dlib.net/)
    - Landmarks Detection
      - [x] [FAN][]
      - [x] [Dlib](http://dlib.net/)
    - Gaze Tracking
      - [x] OpenCV moments(simple)
    - Head Alignment
      - [x] OpenCV solvePnP
    - Face Expression Detection `Under Planning`
    - Pose Estimation `Under Planning`
    - Hand Tracking / Gesture Recognition `Under Planning`
  - Unity Model
    - 3D
      - [x] [Ghost][]
    - 2D `Under Planning`
  - Android Support `Under Planning`
  - iOS Support `Under Planning`
## Environment
  This project is developed on a old hardware, but these information may still be helpful for you :  
  |CPU     |GPU    |RAM   |VRAM   |Python  |CUDA   |cuDNN |PyTorch|Unity Editor|
  |:------:|:-----:|:----:|:-----:|:------:|:-----:|:----:|:-----:|:----------:|
  |FX-8320E|GTX 960| 8 Gb | 2 Gb  | 3.8.12 | 10.2  |8.3.0 |1.10.1 |2019.4.33f1 |
## Acknowledgement
  These repositories helps me in this project, You can check their repo for more related knowledge.  
  Thanks for their open resources!  
  
[![BSD-3-img]][BSD-3-link]
---
> [1adrianb/face-alignment][FAN]

[![MIT-img]][MIT-link]
---
> [antoinelame/GazeTracking][]  
> [kwea123/VTuber_Unity][]  
> [yinguobing/head-pose-estimation][]  
> [dbolya/yolact](https://github.com/dbolya/yolact)  

[FAN]:                              https://github.com/1adrianb/face-alignment                                                        "1adrianb/face-alignment"
[antoinelame/GazeTracking]:         https://github.com/antoinelame/GazeTracking                                                       "antoinelame/GazeTracking"
[kwea123/VTuber_Unity]:             https://github.com/kwea123/VTuber_Unity                                                           "kwea123/VTuber_Unity"
[yinguobing/head-pose-estimation]:  https://github.com/yinguobing/head-pose-estimation                                                "yinguobing/head-pose-estimation"
[Ghost]:                            https://assetstore.unity.com/packages/templates/tutorials/3d-beginner-tutorial-resources-143848   "Unity Technologies/Ghost"

[BSD-3-img]:                        https://img.shields.io/badge/License-BSD_3--Clause-blue.svg
[BSD-3-link]:                       https://opensource.org/licenses/BSD-3-Clause
[MIT-img]:                          https://img.shields.io/badge/License-MIT-yellow.svg
[MIT-link]:                         https://opensource.org/licenses/MIT

