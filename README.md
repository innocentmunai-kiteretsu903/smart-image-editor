## Group members
 1. Bozen Peng
 2. Innocent Munai

## Introduction
We have made a smart photo editor with a user-friendly GUI.

## Functionality
**Enhancing**  
Reset to Original, Gray-scale, Contrast, Brightness, Blurring, Sharpness, Auto Detail Enhance

**Filter**  
Painting, Cannize, Sepia, Pencil Gray, Pencil Color, Invert, Autumn, Cool Wind

**AI Detection**  
Faces, Eyes, Smile, Full body

## The libries needed
1. Streamlit:  To create the web-based GUI.
2. Pillow: The library for basic adjustment of pictures
3. OpenCv: The library that provides the machine learning capability to process pictures
4. Numpy: The library that provides the computational capability to process the data extracted from pictures
5. os: handling system path

## Online demo
Link: https://smart-image-editor.herokuapp.com
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
<img width="1410" alt="preview" src="https://user-images.githubusercontent.com/42286547/166344942-1c88969f-925b-406e-a2d2-322761b9e3e6.png">
