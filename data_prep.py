# This script prepares the data set by:
#  1. partitioning cropped multi-rock image files into single rock image files. 
#  2. reducing the size of each rock image 
#  3. saving the resulting images and labels to data.pickle
#
# It is assumed that all the cropped multi-rock image files are of the same size, 
# resulting in individual images of size 722 x 469 pixels.  These rocks are then resized to 224 x 136.
#
# To run the script, execute "python data_prep.py" 

from scipy.misc import imread, imsave, imresize
import pickle
import numpy as np

rows = ['1', '2', '3', '4', '5']
cols = ['A', 'B', 'C', 'D', 'E']
R = len(rows)
C = len(cols)
T = R * C

images = ['IMG_3631']
I = len(images)

N = I * T   # number of samples

data_dir = '../data/'
images_dir = data_dir + 'images/'
data_file = data_dir + 'data.pickle'

datadict = {}

HH = 469   # height of rock image
WW = 722   # width of rock image

H = 136  # reduced height of rock image
W = 224  # reduced width of rock image

data = np.empty([N, H, W, 3])
labels = np.empty([N, 1])

for i in range(I):
  file_name = data_dir + images[i] + '_cropped.jpg'
  rocks = imread(file_name)

  assert(int(rocks.shape[0]/R) == HH)   # height of each rock
  assert(int(rocks.shape[1]/C) == WW)   # width of each rock

  for j in range(R):
    for k in range(C):
      rock = imresize(rocks[j*HH:j*HH+HH, k*WW:k*WW+WW,:], (H, W))
      file_name = images_dir + images[i] + '_' + rows[j] + cols[k] + '.jpg'
      imsave(file_name, rock)

      n = i*T +  j*R + k
      data[n] = rock
      labels[n] = [0]
     
datadict['data'] = data
datadict['labels'] = labels
pickle.dump(datadict, open(data_file, 'wb'))   