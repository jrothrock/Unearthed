import os

from PIL import Image

from data_prep_rename import chopImage
from excelReader_rename import readExcelFiles

inputDir = './img/sets/'
outputDir = './img/'

excelSheets = readExcelFiles()

for file in os.listdir(inputDir):
    if ".tiff" not in file:
        continue
    print('processing ' + file)
    img = Image.open(inputDir + file)
    chopImage(excelSheets, img, outputDir)
