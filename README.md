## Group members
 1. Bozen Peng
 2. Innocent Munai

## Introduction
We have made a smart photo editor with a user-friendly GUI.
This app is web-based, empowering cross-platform capability, and works well with both mouse and touch screen.

## Functionality
**Enhancing**  
Reset to Original, Gray-scale, Contrast, Brightness, Saturation, Blurring, Sharpness, Auto Detail Enhance

**Filter**  
Painting, Oil Painting, Canny, Sepia, Pencil Gray, Pencil Color, Invert, Autumn, Cool Wind

**AI Detection**  
Faces, Eyes, Smile, Full body

## The libraries used
1. Streamlit:  To create the web-based GUI.
2. Pillow: The library for basic adjustment of pictures
3. OpenCv: The library that provides the machine learning capability to process pictures
4. Numpy: The library that provides the computational capability to process the data extracted from pictures
5. os: handling system path

## Online demo
Link: https://smart-image-editor.herokuapp.com<br/>
Note: Due to the memory quota limitation of Heroku free version, uploading large image may cause crash. Thus, online version is currently only for demo purpose, and we recommend deploying this app locally.

## How to deploy locally
1. Download the code
2. Install all required libraries with requirement.txt
3. Move config.toml to ~/.streamlit/ to configure the streamlit theme properly
4. Start the program by terminal:
```console
streamlit run /whereyoudownload/image-editing-app.py
```
5. The browser should automatically pop up. Or, you may enter the local host address from the information printed on the terminal

## Preview
<img width="1126" alt="111" src="https://user-images.githubusercontent.com/42286547/166741404-0ba21334-8fe8-4b56-9872-1a1908698a92.png">
<br>
<img width="1139" alt="222" src="https://user-images.githubusercontent.com/42286547/166741402-c6754b33-8ab3-4616-a52a-0b2e48ec1bcd.png">

## Acknowledgement
* This is a final project of CS 32 instructed by Professor Michael D. Smith
* Course link: https://scholar.harvard.edu/mikesmith/classes/cs-32-computational-thinking-and-problem-solving
* Professor link: https://scholar.harvard.edu/mikesmith
* We have additionally learned the basic ideas of using Streamlit, OpenCv, Image, and Pillow modules from this Udemy course: https://www.udemy.com/course/build-a-web-app-with-python-and-opencv-image-editing-app 
* Instructor: Gasmi Haithem (https://www.udemy.com/user/gasmi-haithem-2/)
* We have utilized the official documentations of the libraries used in this code.
* We have utilized various online resources to get inspiration and solve problems.
* Color design inspired by Nippon Colors: https://nipponcolors.com/
* Cascade Classifiers are from OpenCV: https://github.com/opencv/opencv/tree/master/data/haarcascades