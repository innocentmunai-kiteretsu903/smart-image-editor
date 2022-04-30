import numpy as np 
import cv2

face_cascade = cv2.CascadeClassifier('detectors/haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('detectors/haarcascade_eye.xml')
smile_cascade = cv2.CascadeClassifier('detectors/haarcascade_smile.xml')
fullbody_cascade = cv2.CascadeClassifier('detectors/haarcascade_fullbody.xml')



def detect_faces(opened_image):
    """
    ????
    """
    new_img = np.array(opened_image.convert("RGB"))
    faces = face_cascade.detectMultiScale(new_img, 1.2, 6)

    # Draw rectangles around the faces
    for (x, y, w, h) in faces:  # 4 corners
        cv2.rectangle(new_img, (x, y), (x+w, y+h), (255, 0, 0), 2)  # 2 border
    return new_img, faces


def detect_eyes(opened_image):
    """
    ????
    """
    new_img = np.array(opened_image.convert("RGB"))
    eyes = eye_cascade.detectMultiScale(new_img, 1.3, 5)

    # Draw rectangles around eyes
    for (x, y, w, h) in eyes:  # 4 corners
        cv2.rectangle(new_img, (x, y), (x+w, y+h), (0, 255, 0), 2)  # 2 border

    return new_img, eyes

def detect_smiles(opened_image):
    """
    ????
    """
    new_img = np.array(opened_image.convert("RGB")) 
    smile = smile_cascade.detectMultiScale(new_img, 1.3, 55)
    return smile

def detect_fullbody(opened_image):
    """
    ????
    """
    new_img = np.array(opened_image.convert("RGB"))
    fullbody = fullbody_cascade.detectMultiScale(new_img, 1.1, 6)
    return fullbody