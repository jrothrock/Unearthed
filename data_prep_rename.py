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


def chopImage(excelSheets, file, width, height, output):
    rows = [1, 2, 3, 4, 5]
    cols = ['A', 'B', 'C', 'D', 'E']
    R = len(rows)
    C = len(cols)

    print("in chopImage")

    HH = width  # height of rock image
    WW = height  # width of rock image

    # max_size = int(literal_eval(sys.argv[1]))
    max_size = 224

    aspect_ratio = float(WW) / HH if HH > WW else float(HH) / WW

    aspect_height = max_size if HH > WW else int(round(max_size * aspect_ratio, 0))

    aspect_width = max_size if WW > HH else int(round(max_size * aspect_ratio, 0))

    image_size = (aspect_height, aspect_width,)

    print("aspect_rate = " + str(aspect_ratio))
    print("aspect_height = " + str(aspect_height))
    print("aspect_width = " + str(aspect_width))

    rocks = imread('./img/sets/' + file)

    for j in range(R):
        for k in range(C):
            rock = imresize(rocks[j * HH:j * HH + HH, k * WW:k * WW + WW, :], image_size)
            file_name = file.replace(".tiff", "") + '_' + str(rows[j]) + cols[k] + '.jpg'
            grid = "Grid " + file_name.split("_")[0]
            print("Grid=" + str(grid))
            print("cols=" + str(cols[k]))
            print("row=" + str(rows[j]))
            print('type=' + excelSheets[grid][cols[k]][rows[j]])
            final_file = output + '/' + excelSheets[grid][cols[k]][rows[j]] + '/' + file_name
            imsave(final_file, rock)
