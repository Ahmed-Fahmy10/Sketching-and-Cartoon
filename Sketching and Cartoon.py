#import libraries
import numpy as np
import cv2
import matplotlib.pyplot as plt
import tkinter
from tkinter  import *
import tkinter.filedialog
from PIL import ImageTk, Image


win=Tk()

win.geometry("500x500")

win.title("Cartoon it")

def cartoon_it(img_dir):
    img_dir = img_dir


    def rgb_img(img_dir):
        # reads from a BGR image file to a RGB
        img = cv2.imread(img_dir)
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    def hsv_img(img_dir):
        # reads from a RGB image file to a HSV array
        hsv = cv2.imread(img_dir)
        return cv2.cvtColor(hsv, cv2.COLOR_RGB2HSV)

    def img_read(img_dir):
        # reads from a RGB image file to grayscale image array
        rgb = rgb_img(img_dir)
        hsv = hsv_img(img_dir)
        gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
        return rgb, hsv, gray

    # define your function
    josh_rgb, josh_hsv, josh_gray = img_read(img_dir)


   ######################################################################################################


    # scaling the image to quater of its actual size
    img_scale = cv2.resize(josh_rgb, (0, 0), fx=0.5, fy=0.5)
    img_scale = cv2.pyrDown(josh_rgb)

    num_iter = 5
    for _ in range(num_iter):
        img_scale = cv2.bilateralFilter(img_scale, d=9, sigmaColor=9, sigmaSpace=7)

    # restoring the image
    josh_blur = cv2.pyrUp(img_scale)


    # convert to grayscale and apply median blur
    img_gray = cv2.cvtColor(josh_rgb, cv2.COLOR_RGB2GRAY)
    img_blur = cv2.medianBlur(img_gray, 7)

    img_edge = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)
    plt.figure(figsize=(10, 10))
    plt.imshow(img_edge)

    def cartoon_filter(self, josh_rgb):
        numDownSamples = 2  # number of downscaling steps
        numBilateralFilters = 7  # number of bilateral filtering steps

        # first step
        # downsample image using Gaussian pyramid
        img_color = josh_rgb
        for _ in range(numDownSamples):
            img_color = cv2.pyrDown(img_color)

        # repeatedly apply small bilateral filter instead of applying
        # one large filter
        for _ in range(numBilateralFilters):
            img_color = cv2.bilateralFilter(img_color, 9, 9, 7)

        # upsample image to original size
        for _ in range(numDownSamples):
            img_color = cv2.pyrUp(img_color)

        # combine steps steps 2 & 3
        # convert to grayscale and apply median blur
        img_gray = cv2.cvtColor(josh_rgb, cv2.COLOR_RGB2GRAY)
        img_blur = cv2.medianBlur(img_gray, 7)

        # fourth step
        # detect and enhance edges
        img_edge = cv2.adaptiveThreshold(img_blur, 255,
                                         cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 2)

        # fifth step
        # convert back to color so that it can be bit-AND
        # with color image
        img_edge = cv2.cvtColor(img_edge, cv2.COLOR_GRAY2RGB)
        return cv2.bitwise_and(img_color, img_edge)

    josh = cartoon_filter(img_edge, josh_rgb)
    plt.figure(figsize=(10, 10))
    plt.imshow(josh)
    plt.show()

def choose_image():
    img_dir = tkinter.filedialog.askopenfilename()
    cartoon_it(img_dir)
    return img_dir



#buttons

b2=Button(win,text="choose image and catoon it", bd=5, width=50,command=choose_image).place(y = 50,x=50)

plt.show()
win.mainloop()