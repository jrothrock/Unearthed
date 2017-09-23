import os

import imageio
import rawpy
from PIL import Image
from data_prep_rename import chopImage

inputDir = './img/raw/'
outputDir = './img/sets/'

for file in os.listdir(inputDir):
    # if ".ARW" not in file:
    #     continue
    print('processing ' + file)
    # raw = rawpy.imread(inputDir + file)
    # rgb = raw.postprocess(use_auto_wb=True)
    # newFile = outputDir + file.replace(".ARW", ".tiff")
    # print('writing ' + file)
    # imageio.imsave(newFile, rgb)
    # if "r" in file:
        # rotation = int(file.split('r')[1].split('.')[0])
        # print('rotating ' + file + ' ' + str(rotation) + 'degrees')
        # width,height = Image.open(newFile).rotate(rotation, resample=Image.BICUBIC, expand=True).save(newFile).size
    width,height = Image.open(inputDir + file).size
    chopImage(file,width,height,outputDir)
