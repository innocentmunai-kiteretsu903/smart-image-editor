'''
* Reference:
* We have learned the basic ideas of using Streamlit, OpenCv, Image, and Pillow modules
* from this Udemy course
* https://www.udemy.com/course/build-a-web-app-with-python-and-opencv-image-editing-app
*
* We have utilized the official documentations of the libraries used in this code.
* We have utilized various online resources to get inspiration and solve problems.
*
* Color design inspired by Nippon Colors (https://nipponcolors.com/)
*
* Cascade Classifiers are from OpenCV
* https://github.com/opencv/opencv/tree/master/data/haarcascades
'''

import streamlit as st                       # For creating web app
import cv2                                   # Image processing
from PIL import Image, ImageEnhance          # Image processing
import numpy as np                           # To deal with arrays

from detections import detect_eyes, detect_faces, detect_smiles, detect_fullbody
from filters import sepia, temp, paint, canny, pencil, inv


def change(): 
    """fallback function when uploading new image.
    When uploading new image, reset session state
    """
    st.session_state['pimg'] = [] 
    st.session_state['enhancing'] = "Reset to Original"

def main():
    st.title('Smart Image Editor') #title
    st.text("Edit your images with a single click!") #slogan

    # Sidebar
    activities = ["Start", "Enhance", "Filters", "AI Detection", "About"] 
    choice = st.sidebar.selectbox('Select Activity', activities) 

    # Uploader (callback to change() when uploading new image)
    ftype = ["jpg", "png", "jpeg", "bmp", "tif"]
    image_file = st.file_uploader("Image Uploader", type = ftype,\
         on_change=change)

    # Start page
    if choice == "Start":  
        with open('use.txt') as file:
            st.text(file.read())

            # Show image preview
            if image_file is not None: 
                opened_image = Image.open(image_file)
                st.image(opened_image)

    # About page
    elif choice == "About":
        st.subheader("About the developers")
        st.markdown("Built by Bozen and Innocent with Streamlit")
        st.markdown("Harvard's CS32 Final Project")
        

    # If image uploaded ...
    if image_file is not None:
        opened_image = Image.open(image_file) 
        opened_image_array_original = np.array(opened_image.convert("RGB")) 
    
        # Initialize sessionstate of image 
        # to store processed image & refresh when uploading new image
        if 'pimg' not in st.session_state or st.session_state['pimg'] == []: 
            st.session_state['pimg'] = opened_image_array_original

        # Enhance page
        if choice == "Enhance":

            # Initialize sessionstate of sidebar buttons of enhancing options 
            if 'enhancing' not in st.session_state: 
                st.session_state['enhancing'] = "Reset to Original"

            # Create buttons of enhancing section
            # Button status store in st.session_state['enhancing']
            enhanceoptions = ["Reset to Original", "Gray-scale", "Contrast", \
                "Brightness", "Blurring", "Sharpness", "Auto Detail Enhance"]
            enhance_type = st.sidebar.radio("Enhance type", enhanceoptions, \
                 key='enhancing') 
    
            # Reset to original
            if enhance_type == "Reset to Original": 
                preview = opened_image_array_original
                st.image(preview)

                # Save button
                if st.sidebar.button("Reset to original"):
                    st.session_state['pimg'] = preview
                    st.sidebar.success("Reset successfully!")

            # Gray-scale filter
            elif enhance_type == "Gray-scale": 

                # If gray, do no change
                if len(st.session_state['pimg'].shape) < 3: 
                    preview = ' '
                    st.image(st.session_state['pimg'])

                # If color, convert
                elif len(st.session_state['pimg'].shape) == 3:
                    preview = cv2.cvtColor(st.session_state['pimg'], \
                        cv2.COLOR_BGR2GRAY)
                    st.image(preview)

                # Save button
                if st.sidebar.button("Save Gray-scale"):

                    # If color, convert and save change
                    if not preview == ' ':
                        st.session_state['pimg'] = preview
                        st.sidebar.success("Gray-scale saved!")
                    
                     # If already gray, alert
                    else:
                        st.sidebar.error("Already Gray-scale!")

            # Contrast adjustment
            elif enhance_type == "Contrast": 
                rate = st.sidebar.slider("Contrast", 0.1, 5.0, 1.0)
                m_img = Image.fromarray(st.session_state['pimg'])
                enhancer = ImageEnhance.Contrast(m_img)
                preview = enhancer.enhance(rate) #take the rate selected
                st.image(preview)

                # Save  button
                if st.sidebar.button("Save Contrast"):
                    st.session_state['pimg'] = np.array(preview.convert("RGB"))
                    st.sidebar.success("Contrast saved!")

            # Brightness adjustment
            elif enhance_type == "Brightness": 
                rate = st.sidebar.slider("Brightness", 0.1, 2.5, 1.0)
                m_img = Image.fromarray(st.session_state['pimg'])
                enhancer = ImageEnhance.Brightness(m_img)
                preview = enhancer.enhance(rate) #take the rate selected
                st.image(preview)

                # Save  button
                if st.sidebar.button("Save Brightness"):
                    st.session_state['pimg'] = np.array(preview.convert("RGB"))
                    st.sidebar.success("Brightness saved!")


            # Blur filter
            elif enhance_type == "Blurring": 
                rate = st.sidebar.slider("Blurring", 1, 21, 1, 2)
                preview = cv2.GaussianBlur(st.session_state['pimg'], \
                    (rate, rate), 5.0)
                st.image(preview)

                # Save button
                if st.sidebar.button("Save Blur"):
                    st.session_state['pimg'] = preview
                    st.sidebar.success("Blur saved!")


            # Sharpness adjustment
            elif enhance_type == "Sharpness": 
                rate = st.sidebar.slider("Sharpness", 0.0, 10.0, 0.0)
                m_img = Image.fromarray(st.session_state['pimg'])
                enhancer = ImageEnhance.Sharpness(m_img)
                preview = enhancer.enhance(rate)
                st.image(preview)

                # Save  button
                if st.sidebar.button("Save Sharpness"):
                    st.session_state['pimg'] = np.array(preview.convert("RGB"))
                    st.sidebar.success("Sharpness saved!")


            # Auto Detail Enhance 
            elif enhance_type == "Auto Detail Enhance":

                # Gray image enhancing
                if len(st.session_state['pimg'].shape) < 3: 
                    preview = cv2.equalizeHist(st.session_state['pimg'])
                    st.image(preview)

                # Color image enhancing
                elif len(st.session_state['pimg'].shape) == 3: 
                    preview = cv2.detailEnhance(st.session_state['pimg'], \
                        sigma_s=3, sigma_r=0.1)
                    st.image(preview)

                # Save  button
                if st.sidebar.button("Save Auto Enhance"):
                    st.session_state['pimg'] = preview
                    st.sidebar.success("Auto Enhance saved!")

            st.sidebar.write('Right-click on the image and select "Save Image" \
                 to download it.')

        elif choice == "Filters":

            # Create selectbox "Filters"
            filters = ["Painting", "Oil Painting", "Canny", "Sepia", \
                "Pencil Gray", "Pencil Color", "Invert", "Autumn", "Cool Wind"]
            feature_choice = st.sidebar.selectbox("Filters", filters)
            if st.sidebar.button("Apply the filter"):
                if feature_choice == "Painting":
                    result_img = paint(opened_image)[1]
                    st.image(result_img)
                elif feature_choice == "Oil Painting":
                    result_img = paint(opened_image)[0]
                    st.image(result_img)
                elif feature_choice == "Canny":
                    result_img = canny(opened_image)
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
            
            st.sidebar.write('Right-click on the image and select "Save Image"\
                 to download it.')

        # AI Detection page
        elif choice == "AI Detection":

            # Create selectbox "AI Detection"
            tasks = ["Faces", "Eyes", "Smile", "Full Body"]
            feature_choice = st.sidebar.selectbox("AI Detection", tasks)
            if st.sidebar.button("Start Detection"):

                # Tell if faces exist and the numbe
                if feature_choice == "Faces":
                    result_img, result_face = detect_faces(opened_image)
                    if len(result_face) > 0:
                        st.success("Found {} faces".format(len(result_face)))
                    elif len(result_face) == 0:
                        st.error("No face found")
                    st.image(result_img)

                # Tell if eyes exist and the number
                elif feature_choice == "Eyes":
                    result_img, result_eye = detect_eyes(opened_image)
                    if len(result_eye) > 0:
                        st.success("Found {} eyes".format(len(result_eye)))
                    elif len(result_eye) == 0:
                        st.error("No eye found")
                    st.image(result_img)

                # Only tell if smile exists
                elif feature_choice == "Smile": 
                    result_smile = detect_smiles(opened_image)
                    if len(result_smile) > 0:
                        st.success("Found smile")
                    elif len(result_smile) == 0:
                        st.error("No smile found")
                    st.image(opened_image)

                # Only tell if full body exists
                elif feature_choice == "Full Body":
                    result_body = detect_fullbody(opened_image)
                    if len(result_body) > 0:
                        st.success("Found full body")
                    elif len(result_body) == 0:
                        st.error("No full body found")
                    st.image(opened_image)

            else:
                preview = opened_image_array_original
                st.image(preview)
                
            st.sidebar.write('Right-click on the image and select "Save Image"\
                 to download it.')


# Hide the footer and/or the menu icon
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
