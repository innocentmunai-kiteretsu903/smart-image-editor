import streamlit as st                       # For creating web app
import cv2                                   # Image processing
from PIL import Image, ImageEnhance          # Image processing
import numpy as np                           # To deal with arrays

from detections import detect_eyes, detect_faces
from filters import sepia, temp, cartoon, cannize, pencil, inv, auto_enhance


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
        st.text("test...test")

    #file uploader
    elif choice == "Editing": #Detection page
        image_file = st.file_uploader("Upload Image", type = ["jpg","png", "jpeg"])

        if image_file is not None: #if uploaded
            opened_image = Image.open(image_file) #open the image by Image function
            st.text("Original Image")
            st.image(opened_image) #display the image

            #create buttons
            enhanceoptions = ["Original", "Gray-scale", "Contrast", "Brightness", "Blurring", "Sharpness", "Auto Detail Enhance"]
            enhance_type = st.sidebar.radio("Enhance type", enhanceoptions) #options on sidebar


            #GRAY_SCALE
            if enhance_type == "Gray-scale": 
                img = np.array(opened_image.convert("RGB"))
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                st.text("Gray-scale image")
                st.image(gray)

            #CONTRAST
            elif enhance_type == "Contrast": 
                rate = st.sidebar.slider("Contrast", 0.1, 10.0, 1.0)
                enhancer = ImageEnhance.Contrast(opened_image)
                contrast_img = enhancer.enhance(rate) #take the rate selected
                st.image(contrast_img)

            #BRIGHTNESS
            elif enhance_type == "Brightness": 
                rate = st.sidebar.slider("Brightness", 0.1, 10.0, 1.0)
                enhancer = ImageEnhance.Brightness(opened_image)
                brightness_img = enhancer.enhance(rate) #take the rate selected
                st.image(brightness_img)

            #BLUR
            elif enhance_type == "Blurring": 
                rate = st.sidebar.slider("Blurring", 0.0, 10.0, 0.0)
                blurred_image = cv2.GaussianBlur(np.array(opened_image),(13,13),rate)#13 size of kernel (filter, odd number)
                st.image(blurred_image)

            #Sharpness
            elif enhance_type == "Sharpness": 
                rate = st.sidebar.slider("Sharpness", 0.0, 10.0, 0.0)
                enhancer = ImageEnhance.Sharpness(opened_image)
                sharpness_img = enhancer.enhance(rate) #take the rate selected
                st.image(sharpness_img)

            #Auto Detail Enhance
            elif enhance_type == "Auto Detail Enhance": 
                #new_img = np.array(opened_image.convert("RGB"))
                #autoe = cv2.detailEnhance(new_img, sigma_s=10, sigma_r=0.2)
                #st.image(autoe)

                st.image(auto_enhance(opened_image))
        

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
        

        #create selectbox "AI Detection"
        tasks = ["Faces", "Eyes"]
        feature_choice = st.sidebar.selectbox("AI Detection", tasks)
        if st.sidebar.button("Start Detection"):
            if feature_choice == "Faces":
                result_img, result_face = detect_faces(opened_image)
                st.image(result_img)
                st.success("Found {} faces".format(len(result_face)))
            elif feature_choice == "Eyes":
                result_img, result_eye = detect_eyes(opened_image)
                st.image(result_img)
                st.success("Found {} eyes".format(len(result_eye)))




if __name__ == '__main__':
    main()
