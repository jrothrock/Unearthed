# -*- coding: utf-8 -*-
import os
import tensorflow as tf
import sys
import re
from PIL import Image
from multiprocessing.dummy import Pool as ThreadPool 

def get_image_paths(folder):
  return [os.path.join(folder,each) for each in os.listdir(folder) if each.endswith('.JPG')]

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

def splitImg(image_path):
    img = Image.open(image_path)
    rows = [1, 2, 3, 4, 5]
    cols = ['A', 'B', 'C', 'D', 'E']
    R = len(rows)
    C = len(cols)

    filename = img.filename.split("/")[-1] 
    if not os.path.exists(image_path.split('/')[-1].split('.')[0]):
        new_dir = os.makedirs(image_path.split('/')[-1].split('.')[0])
    img = Image.open(image_path)

    width, height = img.size


    rock_width = width / 5
    rock_height = height / 5   

    names = []
    print 'before loop'

    for j in range(R):
        for k in range(C):

            newSize = (rock_width * k, rock_height * j, rock_width * (k + 1), rock_height * (j + 1))

            rock = img.crop(newSize)
            print 'below rock'
            file_name = re.sub(r'.tiff|.jpg|.jpeg/', "", filename.lower()) + '_' + str(cols[k]) + str(rows[j]) + '.jpeg'
            print 'above rock'
            final_path = "./" + image_path.split('/')[-1].split('.')[0] + '/' + file_name
           
            rock.save(final_path, "JPEG", quality=100)
            names.append(final_path)

    
    
    print len(names)
    img.close()

    for name in names:
        runTensor(name)

    # pool = ThreadPool()
    # pool.map(runTensor, names)
    # pool.close() 
    # pool.join()


# change this as you see fit
# image_path = sys.argv[1]


images = get_image_paths(os.path.dirname(sys.argv[1]))
print images
print len(images)

for image in images:
    splitImg(image)
# pool = ThreadPool()
# pool.map(splitImg, images)
# pool.close() 
# pool.join()