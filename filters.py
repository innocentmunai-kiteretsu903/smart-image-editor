import numpy as np
import cv2


def grayscale(opened_image):
    """This function takes an image object opened by Image.open as the input.
    It returns the gray-scale processed image.
    """
    img = np.array(opened_image.convert("RGB"))
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return gray_image


def sepia(opened_image):
    """This function takes an image object opened by Image.open as the input.
    It returns the sepia processed image.
    """
    new_img = np.array(opened_image.convert("RGB"))
    sepia_matrix = np.matrix([[0.393, 0.769, 0.189],
                              [0.349, 0.686, 0.168],
                              [0.272, 0.534, 0.131]])
    sepia_image = cv2.transform(new_img, sepia_matrix)
    return np.clip(sepia_image, 0, 255)


#kevin table for the purpose of changing picture's color temperature
kelvin_table = {
    1000: (255, 56, 0),
    1500: (255, 109, 0),
    2000: (255, 137, 18),
    2500: (255, 161, 72),
    3000: (255, 180, 107),
    3500: (255, 196, 137),
    4000: (255, 209, 163),
    4500: (255, 219, 186),
    5000: (255, 228, 206),
    5500: (255, 236, 224),
    6000: (255, 243, 239),
    6500: (255, 249, 253),
    7000: (245, 243, 255),
    7500: (235, 238, 255),
    8000: (227, 233, 255),
    8500: (220, 229, 255),
    9000: (214, 225, 255),
    9500: (208, 222, 255),
    10000: (204, 219, 255)}


def temp(opened_image, k):
    """This function takes an image object opened by Image.open and the expected 
    color temperature as the input.
    It returns the processed image with the expected color temperature.
    """
    new_img = np.array(opened_image.convert("RGB"))
    r, g, b = kelvin_table[k]
    temp_matrix = np.matrix([[r / 255, 0, 0],
                            [0, g / 255, 0],
                            [0, 0, b / 255]])
    temp_image = cv2.transform(new_img, temp_matrix)
    return temp_image


def paint(opened_image):
    """This function takes an image object opened by Image.open as the input.
    It returns two paint processed image: one without edge, another with edge.
    """
    new_img = np.array(opened_image.convert("RGB"))
    edge = cv2.bitwise_not(cv2.Canny(new_img, 200, 300))
    smooth = cv2.edgePreservingFilter(
        new_img, flags=2, sigma_s=60, sigma_r=0.3)
    paint_image = cv2.bitwise_and(smooth, smooth, mask=edge)
    return smooth, paint_image


def canny(opened_image):
    """This function takes an image object opened by Image.open as the input.
    It returns the canny image.
    """

    new_img = np.array(opened_image.convert("RGB"))
    canny_image = cv2.Canny(new_img, 100, 200)
    return canny_image


def pencil(opened_image):
    """This function takes an image object opened by Image.open as the input.
    It returns two pencil-processed images: one gray, another colored.
    """
    new_img = np.array(opened_image.convert("RGB"))
    pencil_gray, pencil_color = cv2.pencilSketch(
        new_img, sigma_s=60, sigma_r=0.08, shade_factor=0.07)
    return pencil_gray, pencil_color


def inv(opened_image):
    """This function takes an image object opened by Image.open as the input.
    It returns the color-inverted image.
    """
    new_img = np.array(opened_image.convert("RGB"))
    inv_image = cv2.bitwise_not(new_img)
    return inv_image
