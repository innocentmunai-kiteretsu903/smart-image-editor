'''
* Reference:
* We have learned the basic ideas of using streamlit, opencv, and Pillow modules
* from this Udemy course
* https://www.udemy.com/course/build-a-web-app-with-python-and-opencv-image-editing-app
*
* we have utilized the official documentations of the libraries used in this code
* we have utilized various online resources to solve error and warning information
*
* Cascade Classifiers are from OpenCV
* https://github.com/opencv/opencv/tree/master/data/haarcascades
'''

import streamlit as st                       # For creating web app
import cv2                                   # Image processing
from PIL import Image, ImageEnhance          # Image processing
import numpy as np                           # To deal with arrays

from detections import detect_eyes, detect_faces, detect_smiles, detect_fullbody
from filters import sepia, temp, paint, cannize, pencil, inv



# Hide the footer and/or the menu icon
hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def change(): #fallback function when uploading new image
    #st.snow()
    #when uploading new image, reset session state
    st.session_state['pimg'] = [] 
    st.session_state['enhancing'] = "Reset to Original"

def main():
    st.title('Smart Image Editor') #title
    st.text("Edit your images with a single click!") #slogan

    #sidebar
    activities = ["Start", "Enhance", "Filters", "AI Detection", "About"]  #sidebar options
    choice = st.sidebar.selectbox('Select Activity', activities) #create sidebar

    #Uploader (callback to change() when uploading new image)
    image_file = st.file_uploader("Image Uploader", type=["jpg", "png", "jpeg"], on_change=change)

    if choice == "Start":  # Start page
        with open('use.txt') as file:
            st.text(file.read())
            if image_file is not None: #show image preview
                opened_image = Image.open(image_file) #open the image into image object
                st.image(opened_image)

    elif choice == "About": # About page
        st.subheader("About the developers")
        st.markdown("Built by Bozen and Innocent with Streamlit")
        st.markdown("Harvard's CS32 Final Project")
        

    if image_file is not None: #behaviors if image uploaded
        opened_image = Image.open(image_file) #open the image into image object
        opened_image_array_original = np.array(opened_image.convert("RGB")) #convert the image into array
    
        #initialize sessionstate of image 
        #to store processed image & refresh when uploading new image
        if 'pimg' not in st.session_state or st.session_state['pimg'] == []: 
            st.session_state['pimg'] = opened_image_array_original

        if choice == "Enhance": #Enhance page
            #initialize sessionstate of sidebar buttons of enhancing options 
            if 'enhancing' not in st.session_state: 
                st.session_state['enhancing'] = "Reset to Original"

            #create buttons of enhancing section
            #button status store in st.session_state['enhancing']
            enhanceoptions = ["Reset to Original", "Gray-scale", "Contrast", "Brightness", "Blurring", "Sharpness", "Auto Detail Enhance"]
            enhance_type = st.sidebar.radio("Enhance type", enhanceoptions, key='enhancing') 
    
            #RESET TO ORIGINAL - OK
            if enhance_type == "Reset to Original": 
                preview = opened_image_array_original
                st.image(preview)

                #save button
                if st.sidebar.button("Reset to original"):
                    st.session_state['pimg'] = preview
                    st.sidebar.success("Reset successfully!")

            #GRAY_SCALE - OK
            elif enhance_type == "Gray-scale": 
                if len(st.session_state['pimg'].shape) < 3: #if gray, do no change
                    preview = ' '
                    st.image(st.session_state['pimg'])
                elif len(st.session_state['pimg'].shape) == 3: #if color, convert
                    preview = cv2.cvtColor(st.session_state['pimg'], cv2.COLOR_BGR2GRAY)
                    st.image(preview)

                #save button
                if st.sidebar.button("Save Gray-scale"):
                    if not preview == ' ': #if color, convert and save change
                        st.session_state['pimg'] = preview
                        st.sidebar.success("Gray-scale saved!")
                    else: #if already gray, alert
                        st.sidebar.error("Already Gray-scale!")

            #CONTRAST - OK
            elif enhance_type == "Contrast": 
                rate = st.sidebar.slider("Contrast", 0.1, 5.0, 1.0)
                m_img = Image.fromarray(st.session_state['pimg'])
                enhancer = ImageEnhance.Contrast(m_img)
                preview = enhancer.enhance(rate) #take the rate selected
                st.image(preview)

                #save  button
                if st.sidebar.button("Save Contrast"):
                    st.session_state['pimg'] = np.array(preview.convert("RGB"))
                    st.sidebar.success("Contrast saved!")

            #BRIGHTNESS - OK
            elif enhance_type == "Brightness": 
                rate = st.sidebar.slider("Brightness", 0.1, 2.5, 1.0)
                m_img = Image.fromarray(st.session_state['pimg'])
                enhancer = ImageEnhance.Brightness(m_img)
                preview = enhancer.enhance(rate) #take the rate selected
                st.image(preview)

                #save  button
                if st.sidebar.button("Save Brightness"):
                    st.session_state['pimg'] = np.array(preview.convert("RGB"))
                    st.sidebar.success("Brightness saved!")


            #BLUR - OK
            elif enhance_type == "Blurring": 
                rate = st.sidebar.slider("Blurring", 1, 21, 1, 2)
                preview = cv2.GaussianBlur(st.session_state['pimg'], (rate, rate), 5.0)
                st.image(preview)

                #save button
                if st.sidebar.button("Save Blur"):
                    st.session_state['pimg'] = preview
                    st.sidebar.success("Blur saved!")


            #Sharpness -OK
            elif enhance_type == "Sharpness": 
                rate = st.sidebar.slider("Sharpness", 0.0, 10.0, 0.0)
                m_img = Image.fromarray(st.session_state['pimg'])
                enhancer = ImageEnhance.Sharpness(m_img)
                preview = enhancer.enhance(rate) #take the rate selected
                st.image(preview)

                #save  button
                if st.sidebar.button("Save Sharpness"):
                    st.session_state['pimg'] = np.array(preview.convert("RGB"))
                    st.sidebar.success("Sharpness saved!")


            #Auto Detail Enhance - OK
            elif enhance_type == "Auto Detail Enhance": 
                if len(st.session_state['pimg'].shape) < 3: #gray image enhancing
                    preview = cv2.equalizeHist(st.session_state['pimg'])
                    st.image(preview)
                elif len(st.session_state['pimg'].shape) == 3: #color image enhancing
                    preview = cv2.detailEnhance(st.session_state['pimg'], sigma_s=3, sigma_r=0.1)
                    st.image(preview)

                #save  button
                if st.sidebar.button("Save Auto Enhance"):
                    st.session_state['pimg'] = preview
                    st.sidebar.success("Auto Enhance saved!")

            st.sidebar.write('Right-click on the image and select "Save Image" to download it.')

        elif choice == "Filters":

            #create selectbox "Filters"
            filters = ["Painting", "Cannize","Sepia", "Pencil Gray", "Pencil Color", "Invert", "Autumn", "Cool Wind"]
            feature_choice = st.sidebar.selectbox("Filters", filters)
            if st.sidebar.button("Apply the filter"):
                if feature_choice == "Painting":
                    result_img = paint(opened_image)
                    st.image(result_img)
                elif feature_choice == "Cannize":
                    result_img = cannize(opened_image)
                    st.image(result_img)
                elif feature_choice == "Sepia":
                    result_img = sepia(opened_image)
                    st.image(result_img)
                elif feature_choice == "Pencil Gray":
                    result_img = pencil(opened_image)
                    st.image(result_img[0])
                elif feature_choice == "Pencil Color":
                    result_img = pencil(opened_image)
                    st.image(result_img[1])
                elif feature_choice == "Invert":
                    result_img = inv(opened_image)
                    st.image(result_img)
                elif feature_choice == "Autumn":
                    result_img = temp(opened_image, 3500)
                    st.image(result_img)
                elif feature_choice == "Cool Wind":
                    result_img = temp(opened_image, 10000)
                    st.image(result_img)
            else:
                preview = opened_image_array_original
                st.image(preview)
            
            st.sidebar.write('Right-click on the image and select "Save Image" to download it.')


        elif choice == "AI Detection":
            #create selectbox "AI Detection"
            tasks = ["Faces", "Eyes", "Smile", "Full Body"]
            feature_choice = st.sidebar.selectbox("AI Detection", tasks)
            if st.sidebar.button("Start Detection"):
                if feature_choice == "Faces": #tell if faces exist and the number
                    result_img, result_face = detect_faces(opened_image)
                    if len(result_face) > 0:
                        st.success("Found {} faces".format(len(result_face)))
                    elif len(result_face) == 0:
                        st.error("No face found")
                    st.image(result_img)
                elif feature_choice == "Eyes": #tell if eyes exist and the number
                    result_img, result_eye = detect_eyes(opened_image)
                    if len(result_eye) > 0:
                        st.success("Found {} eyes".format(len(result_eye)))
                    elif len(result_eye) == 0:
                        st.error("No eye found")
                    st.image(result_img)
                elif feature_choice == "Smile": #only tell if smile exists
                    result_smile = detect_smiles(opened_image)
                    if len(result_smile) > 0:
                        st.success("Found smile")
                    elif len(result_smile) == 0:
                        st.error("No smile found")
                    st.image(opened_image)
                elif feature_choice == "Full Body": #only tell if full body exists
                    result_body = detect_fullbody(opened_image)
                    if len(result_body) > 0:
                        st.success("Found full body")
                    elif len(result_body) == 0:
                        st.error("No full body found")
                    st.image(opened_image)

            else:
                preview = opened_image_array_original
                st.image(preview)
                
            st.sidebar.write('Right-click on the image and select "Save Image" to download it.')

if __name__ == '__main__':
    main()
