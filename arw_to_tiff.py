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
    width, height = Image.open(inputDir + file).size
    chopImage(excelSheets, file, width, height, outputDir)
    break
