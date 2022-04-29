import streamlit as st #for creating web app
import cv2 #image processing
from PIL import Image, ImageEnhance
import numpy as np #to deal with arrays
import os
from utilities import rgb2gray


face_cascade = cv2.CascadeClassifier('detectors/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('detectors/haarcascade_eye.xml')


kelvin_table = {
    1000: (255,56,0),
    1500: (255,109,0),
    2000: (255,137,18),
    2500: (255,161,72),
    3000: (255,180,107),
    3500: (255,196,137),
    4000: (255,209,163),
    4500: (255,219,186),
    5000: (255,228,206),
    5500: (255,236,224),
    6000: (255,243,239),
    6500: (255,249,253),
    7000: (245,243,255),
    7500: (235,238,255),
    8000: (227,233,255),
    8500: (220,229,255),
    9000: (214,225,255),
    9500: (208,222,255),
    10000: (204,219,255)}

def temp(opened_image, k):
    r, g, b = kelvin_table[k]
    temp_matrix = ( r / 255.0, 0.0, 0.0, 0.0,
               0.0, g / 255.0, 0.0, 0.0,
               0.0, 0.0, b / 255.0, 0.0 )
    temp_image = opened_image.convert('RGB', temp_matrix)
    return temp_image

def detect_faces(opened_image):
    #detect face
    new_img = np.array(opened_image.convert("RGB"))
    faces = face_cascade.detectMultiScale(new_img, 1.1, 6)

    #draw rectangles
    for (x, y, w, h) in faces: #4 corners
        cv2.rectangle(new_img, (x,y), (x+w, y+h), (255, 0, 0), 2) #2 border
    return new_img, faces


def detect_eyes(opened_image):
    new_img = np.array(opened_image.convert("RGB"))
    eyes = eye_cascade.detectMultiScale(new_img, 1.3, 5)

    #draw rectangles
    for (x, y, w, h) in eyes: #4 corners
        cv2.rectangle(new_img, (x,y), (x+w, y+h), (0, 255, 0), 2) #2 border
    return new_img, eyes

def cartoon(opened_image):
    new_img = np.array(opened_image.convert("RGB"))
    edge = cv2.bitwise_not(cv2.Canny(new_img, 200, 300))
    smooth = cv2.edgePreservingFilter(new_img, flags=2, sigma_s=64, sigma_r=0.3)
    cartoon_img = cv2.bitwise_and(smooth, smooth, mask = edge)
    return cartoon_img

def cannize(opened_image):
    new_img = np.array(opened_image.convert("RGB"))
    img = cv2.GaussianBlur(new_img, (15,15), 0)
    cannized_img = cv2.Canny(img, 100, 150)
    return cannized_img

def sepia(opened_image):
    new_img = np.array(opened_image.convert("RGB"), dtype=np.float64) 
    sepia_matrix = np.matrix([[0.390, 0.769, 0.189],
                              [0.349, 0.686, 0.168],
                              [0.272, 0.534, 0.131]])
    sepia_img = cv2.transform(new_img, sepia_matrix)
    sepia_img[np.where(sepia_img > 255)] = 255 
    sepia_img = np.array(sepia_img, dtype=np.uint8)
    return sepia_img

def pencil(opened_image):
    new_img = np.array(opened_image.convert("RGB"))
    sk_gray, sk_color = cv2.pencilSketch(new_img, sigma_s=60, sigma_r=0.07, shade_factor=0.1)
    return sk_gray, sk_color

def inv(opened_image):
    new_img = np.array(opened_image.convert("RGB"))
    inv_img = cv2.bitwise_not(new_img)
    return inv_img
    



def main():
    st.title('Image Editor') #define title
    st.text("Edit your image in a fast and simple way") #subtitle


    #sidebar
    activities = ["Editing", "About"]  #sidebar options
    choice = st.sidebar.selectbox('Select Activity', activities) #create sidebar


    #file uploader
    if choice == "Editing": #Detection page
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
                new_img = np.array(opened_image.convert("RGB"))
                autoe = cv2.detailEnhance(new_img, sigma_s=10, sigma_r=0.2)
                st.image(autoe)
        

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



            



    elif choice == "About": #About page
        st.subheader("About the developer")
        st.markdown("Built with streamlit by Bozen and Innocent") #can add website/social media.
        st.text("test...test")



if __name__ == '__main__':
    main()