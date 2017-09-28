# -*- coding: utf-8 -*-
import os
import tensorflow as tf
import sys
import re
from PIL import Image
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
    runTensor("../img/sets/screenshot_{0}.jpg".format(img_count))


# change this as you see fit
# image_path = sys.argv[1]

# Loads label file, strips off carriage return

img_count = 0
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened(): # try to get the first frame
    rval, frame = vc.read()
else:
    rval = False

time_old = datetime.now().replace(microsecond=0)
threads = []

while rval:
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
