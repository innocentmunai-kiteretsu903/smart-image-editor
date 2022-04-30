import streamlit as st                       # For creating web app
import cv2                                   # Image processing
from PIL import Image, ImageEnhance          # Image processing
import numpy as np                           # To deal with arrays

from detections import detect_eyes, detect_faces, detect_smiles, detect_fullbody
from filters import sepia, temp, cartoon, cannize, pencil, inv

hide_streamlit_style = """
            <style>
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def main():
    st.title('Image Editor') #define title
    st.text("Edit your image in a fast and simple way") #subtitle


    #sidebar
    activities = ["Editing", "About"]  #sidebar options
    choice = st.sidebar.selectbox('Select Activity', activities) #create sidebar


    if choice == "About":  # About page
        st.subheader("About the developers")
        # can add website/social media.
        st.markdown("Built with streamlit by Bozen and Innocent")
        with open('about.txt') as file:
            st.text(file.read())

    #file uploader
    elif choice == "Editing": #Detection page
        image_file = st.file_uploader("Upload Image", type = ["jpg","png", "jpeg"])

        if image_file is not None: #if uploaded
            opened_image = Image.open(image_file) #open the image by Image function
            opened_image_array_original = np.array(opened_image.convert("RGB")) #!!!!!!
            st.text("Original Image")
            st.image(opened_image) #display the image

            #initialize sessionstate to store processed image
            if 'pimg' not in st.session_state:
                st.session_state['pimg'] = opened_image_array_original


            #create buttons of enhancing section
            enhanceoptions = ["Reset to Original", "Gray-scale", "Contrast", "Brightness", "Blurring", "Sharpness", "Auto Detail Enhance"]
            enhance_type = st.sidebar.radio("Enhance type", enhanceoptions) #options on sidebar


            #RESET TO ORIGINAL - OK
            if enhance_type == "Reset to Original": 
                st.image(opened_image_array_original)

                #save button
                if st.sidebar.button("Reset to original"):
                    st.session_state['pimg'] = opened_image_array_original
                    st.sidebar.success("Reset successfully!")


            #GRAY_SCALE - OK
            elif enhance_type == "Gray-scale": 
                if len(st.session_state['pimg'].shape) < 3: #if gray, do no change
                    preview = ' '
                    st.image(st.session_state['pimg'])
                elif len(st.session_state['pimg'].shape) == 3: #if color, convert
                    preview = cv2.cvtColor(st.session_state['pimg'], cv2.COLOR_BGR2GRAY)
                    st.image(preview)

                #save  button
                if st.sidebar.button("Save Gray-scale"):
                    if not preview == ' ': #if color, save change
                        st.session_state['pimg'] = preview
                        st.sidebar.success("Gray-scale saved!")
                    else: #if gray, alert
                        st.sidebar.error("Already Gray-scale!")


            #CONTRAST - OK
            elif enhance_type == "Contrast": 
                rate = st.sidebar.slider("Contrast", 0.1, 10.0, 1.0)
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
                rate = st.sidebar.slider("Brightness", 0.1, 2.0, 1.0)
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
                rate = st.sidebar.slider("Blurring", 0.0, 10.0, 0.0)
                preview = cv2.GaussianBlur(st.session_state['pimg'],(13,13),rate)
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


            
            #empty space
            for _ in range(2):
                st.sidebar.write('\n')



            #create selectbox "Filters"
            filters = ["Cartoon", "Cannize","Sepia", "Pencil Gray", "Pencil Color", "Invert", "Warm", "Cold"]
            feature_choice = st.sidebar.selectbox("Filters", filters)
            if st.sidebar.button("Apply the filter"):
                if feature_choice == "Cartoon":
                    result_img = cartoon(opened_image)
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
                elif feature_choice == "Warm":
                    result_img = temp(opened_image, 3500)
                    st.image(result_img)
                elif feature_choice == "Cold":
                    result_img = temp(opened_image, 10000)
                    st.image(result_img)
            
            #empty space
            for _ in range(2):
                st.sidebar.write('\n')


            #create selectbox "AI Detection"
            tasks = ["Faces", "Eyes", "Smile", "Full Body"]
            feature_choice = st.sidebar.selectbox("AI Detection", tasks)
            if st.sidebar.button("Start Detection"):
                if feature_choice == "Faces":
                    result_img, result_face = detect_faces(opened_image)
                    st.image(result_img)
                    st.info("Found {} faces".format(len(result_face)))
                elif feature_choice == "Eyes":
                    result_img, result_eye = detect_eyes(opened_image)
                    st.image(result_img)
                    st.info("Found {} eyes".format(len(result_eye)))
                elif feature_choice == "Smile":
                    result_smile = detect_smiles(opened_image)
                    if len(result_smile) > 0:
                        st.info("Found Smile")
                    elif len(result_smile) == 0:
                        st.error("No Smile")
                elif feature_choice == "Full Body":
                    result_body = detect_fullbody(opened_image)
                    if len(result_body) > 0:
                        st.info("Found Full Body")
                    elif len(result_body) == 0:
                        st.error("No Full Body")


if __name__ == '__main__':
    main()
