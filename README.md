# Virtual Mouse Using Hand Gesture

A Python-based application that allows you to control your computer's mouse cursor and functions through hand movements. This project uses **OpenCV** and **MediaPipe** to track hand landmarks via your webcam and translate them into mouse actions.

## Features
- **Smooth Cursor Movement**: Control the pointer precisely using your index finger.
- **Click Actions**: Perform Left Click, Right Click, and Double Click with simple pinches.
- **Advanced Controls**: Support for Drag and Drop, Scrolling (Up/Down), and Screenshots.
- **Pause Mode**: Easily toggle the system on/off by making a fist.

## Built With
- [Python](https://python.org)
- [OpenCV](https://opencv.org) (Computer Vision)
- [MediaPipe](https://mediapipe.dev) (Hand Tracking)
- [PyAutoGUI](https://readthedocs.io) & [pynput](https://readthedocs.io) (Mouse Control)

## How to Use (Gestures)


| Action | Gesture |
| :--- | :--- |
| **Move Cursor** | Point with your Index finger |
| **Left Click** | Pinch Index finger and Thumb together |
| **Right Click** | Pinch Middle finger and Thumb together |
| **Double Click** | Pinch Index, Middle, and Thumb together |
| **Scroll** | Hold Index and Middle fingers up |
| **Screenshot** | Pinch Pinky finger and Thumb together |
| **Pause/Resume** | Make a full Fist |

## Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com
   cd Virtual-Mouse-Hand-Gesture

2. **Install dependencies**:
   Run this command to install the required libraries (OpenCV, MediaPipe, PyAutoGUI, etc.):
   ```bash
   pip install -r requirements.txt

3. **Run the Application**
    python main.py
