# This script partitions cropped multi-rock image files into single rock image files.  
# To run the script, execute "python partition_image.py" 

from scipy.misc import imread, imsave

rows = ['1', '2', '3', '4', '5']
cols = ['A', 'B', 'C', 'D', 'E']
R = len(rows)
C = len(cols)

images = ['IMG_3631']

training_dir = '../data/training/'

for image in images:
  file_name = training_dir + image + '_cropped.jpg'
  rocks = imread(file_name)

  N = int(rocks.shape[0]/R)   # height of each rock
  M = int(rocks.shape[1]/C)   # width of each rock

  for i in range(R):
    for j in range(C):
      rock = rocks[i*N:i*N+N, j*M:j*M+M,:]
      file_name = training_dir + image + '_' + rows[i] + cols[j] + '.jpg'
      imsave(file_name, rock)
