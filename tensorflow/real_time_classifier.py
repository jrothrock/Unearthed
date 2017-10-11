# -*- coding: utf-8 -*-
import os
import tensorflow as tf
import sys
import re
from PIL import Image, ImageDraw, ImageFont
from multiprocessing.dummy import Pool as ThreadPool 
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import threading
from datetime import datetime
import numpy as np

def runTensor(image_file):
    image_data = tf.gfile.FastGFile(image_file , 'rb').read()

    # Loads label file, strips off carriage return
    label_lines = [line.rstrip() for line
                    in tf.gfile.GFile("./retrained_labels.txt")]

    # Unpersists graph from file
    with tf.gfile.FastGFile("./retrained_graph.pb", 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        
        predictions = sess.run(softmax_tensor, \
                {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        for node_id in top_k:
            human_string = label_lines[node_id]
            score = predictions[0][node_id]
    
            if(score >= 0.501):
                global is_ore
                if(human_string == 'waste'):
                    is_ore = False
                else:
                    is_ore = True
                print('img %s is a %s' % (image_file.split('/')[-1].split('.')[0], human_string))
                try:
                    file = open("rocks.txt", 'ab')
                except IOError:
                    file = open("rocks.txt", 'w')
                file.write('img %s is a %s \n' % (image_file.split('/')[-1].split('.')[0], human_string))
                file.close() 

def getImages(img_count):
    s, img = vc.read()
    cv2.imwrite("../img/sets/screenshot_{0}.jpg".format(img_count),img) #save image
    global is_ore
    is_ore = None
    runTensor("../img/sets/screenshot_{0}.jpg".format(img_count))

def blend_images(image_one, overlay_t_img):
    # Split out the transparency mask from the colour info
    overlay_img = overlay_t_img[:,:,:3] # Grab the BRG planes
    overlay_mask = overlay_t_img[:,:,3:]  # And the alpha plane

    # Again calculate the inverse mask
    background_mask = 255 - overlay_mask

    # Turn the masks into three channel, so we can use them as weights
    overlay_mask = cv2.cvtColor(overlay_mask, cv2.COLOR_GRAY2BGR)
    background_mask = cv2.cvtColor(background_mask, cv2.COLOR_GRAY2BGR)

    # Create a masked out face image, and masked out overlay
    # We convert the images to floating point in range 0.0 - 1.0
    face_part = (image_one * (1 / 255.0)) * (background_mask * (1 / 255.0))
    overlay_part = (overlay_img * (1 / 255.0)) * (overlay_mask * (1 / 255.0))

    # And finally just add them together, and rescale it back to an 8bit integer image    
    return np.uint8(cv2.addWeighted(face_part, 255.0, overlay_part, 255.0, 0.0))

def resize_images(file, width, height):
    # basically creates a transparent image that's the size of the web cam frame
    # and pastes the image - the green check and red x - in the middle
    image = Image.open(file, 'r')
    transparent_img = Image.new('RGBA', (width,height), (0, 0, 0, 0))
    transparent_img.paste(image, (width/2,height/2))
    name = '../' + file.split('.')[-2] + '-resize.png'
    transparent_img.save(name, format="png")

# Globl Variables
is_ore = None
img_count = 0

cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): 
    rval, frame = vc.read()
else:
    rval = False

time_old = datetime.now().replace(microsecond=0)
threads = []
height, width = frame.shape[:2]

## Have to resize images as numpy won't multiply different shape arrays
resize_images('../img/supporting/green-check.png',width,height)
resize_images('../img/supporting/red-x.png',width,height)

check_mark = cv2.imread("../img/supporting/green-check-resize.png", -1)
red_x = cv2.imread('../img/supporting/red-x-resize.png', -1)

while rval:
    if(is_ore):
        frame = blend_images(frame,check_mark)
    elif(is_ore == False):
        frame = blend_images(frame,red_x)
    cv2.imshow("preview", frame)
    rval, frame = vc.read()
    key = cv2.waitKey(20)
    new_time = datetime.now().replace(microsecond=0)
    if(int(str(new_time - time_old).split(':')[-1]) >=5):
        time_old = new_time
        img_count += 1
        t = threading.Thread(target=getImages, args=(img_count,))
        threads.append(t)
        t.start()
    if key == 27: # exit on ESC
        break