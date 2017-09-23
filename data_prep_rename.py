def chopImage(excelSheets, img, output):
    width, height = img.size

    rows = [1, 2, 3, 4, 5]
    cols = ['A', 'B', 'C', 'D', 'E']
    R = len(rows)
    C = len(cols)

    print("in chopImage")

    rock_width = width / 5
    rock_height = height / 5

    filename = img.filename.split("/")[-1]

    for j in range(R):
        for k in range(C):
            rock = img.crop((rock_width * k, rock_height * j, rock_width, rock_height))
            file_name = filename.replace(".tiff", "") + '_' + cols[k] + str(rows[j]) + '.tiff'
            grid = "Grid " + file_name.split("_")[0]
            print("Grid=" + str(grid))
            print("cols=" + str(cols[k]))
            print("row=" + str(rows[j]))
            print('type=' + excelSheets[grid][cols[k]][rows[j]])
            final_file = output + '/' + excelSheets[grid][cols[k]][rows[j]] + '/' + file_name
            print('saving ' + final_file)
            rock.save(final_file)
        break
    img.close()
